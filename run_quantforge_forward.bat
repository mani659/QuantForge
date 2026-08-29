@echo off
setlocal

cd /d "%~dp0"
set PYTHONPATH=%~dp0
set LOG_DIR=runtime\forward\supervisor
set LOCK_FILE=%LOG_DIR%\supervisor.lock
set MT5_PATH=C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe

echo.
echo ========================================
echo  QUANTFORGE FORWARD RUNNER
echo ========================================
echo.

:: ── Step 0: Verify Python is available ──
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo  FORWARD START BLOCKED
    echo  Reason: Python not found
    echo ========================================
    echo.
    echo Python is required to run the supervisor.
    echo Please install Python 3.11+ and re-run this BAT.
    echo.
    pause >nul
    exit /b 1
)

:: ── Step 1: Detect actual supervisor via PowerShell ──
:: Queries Win32_Process for command lines containing our supervisor script.
:: Excludes the PowerShell process itself by filtering on Name='python*'.
set "ACTUAL_PID="
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*quantforge_forward_supervisor.py*' -and $_.Name -like 'python*' } | Select-Object -First 1 -ExpandProperty ProcessId" 2^>nul`) do (
    set "ACTUAL_PID=%%i"
)

:: Verify the PID is actually alive
set "SUPERVISOR_CONFIRMED=0"
if defined ACTUAL_PID (
    tasklist /FI "PID eq %ACTUAL_PID%" 2>nul | find /I "python" >nul
    if %ERRORLEVEL% EQU 0 (
        set "SUPERVISOR_CONFIRMED=1"
    )
)

if "%SUPERVISOR_CONFIRMED%"=="1" (
    echo.
    echo ========================================
    echo  QUANTFORGE FORWARD RUNNER
    echo ========================================
    echo.
    echo  SUPERVISOR ALREADY RUNNING
    echo.
    echo  PID: %ACTUAL_PID%
    echo.
    echo  Use status_quantforge_forward.bat
    echo  to inspect the live system.
    echo.
    echo  Use stop_quantforge_forward.bat
    echo  to stop it.
    echo.
    pause >nul
    exit /b 0
)

:: ── Step 2: No real supervisor found ──
:: Clean up stale lock if present
if exist "%LOCK_FILE%" (
    echo STALE SUPERVISOR LOCK DETECTED
    echo Removing stale lock...
    del "%LOCK_FILE%" 2>nul
    echo.
)

:: Clean up stale shutdown request if present
if exist "%LOG_DIR%\shutdown.req" (
    echo Removing stale shutdown request...
    del "%LOG_DIR%\shutdown.req" 2>nul
    echo.
)

:: ── Step 3: Ensure MT5 terminal is running ──
echo Checking MT5 terminal...
tasklist /FI "IMAGENAME eq terminal64.exe" 2>nul | find /I "terminal64.exe" >nul
if %ERRORLEVEL% NEQ 0 (
    echo MT5 terminal not running.
    echo Starting Exness MT5...
    if exist "%MT5_PATH%" (
        start "" "%MT5_PATH%"
        echo Waiting for MT5 to initialize...
        timeout /t 8 /nobreak >nul
    ) else (
        echo.
        echo ========================================
        echo  FORWARD START BLOCKED
        echo  Reason: MT5 terminal not found
        echo.
        echo  Expected:
        echo  %MT5_PATH%
        echo ========================================
        echo.
        echo Please install MetaTrader 5 Exness and re-run this BAT.
        echo.
        pause >nul
        exit /b 1
    )
) else (
    echo MT5 terminal already running.
)

:: Set MT5 terminal path for Python supervisor
set QF_MT5_TERMINAL_PATH=%MT5_PATH%

:: Ensure runtime directory exists
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo.
echo Starting QuantForge Forward Supervisor...
echo CAND-015 + CAND-024 + CAND-035
echo.
echo Press Ctrl+C to stop, or use stop_quantforge_forward.bat
echo.

:: Run Python supervisor in foreground (command window stays open)
:: No start /b, no hidden window, no detached process.
python -u scripts\forward\quantforge_forward_supervisor.py --mode forward

:: If Python exits, keep window visible
echo.
echo Supervisor process has exited.
pause
