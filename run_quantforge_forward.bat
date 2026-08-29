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

:: ── Step 1: Verify whether supervisor is ACTUALLY running ──
:: Do NOT trust stale lock file or status.json.
:: Scan for the real process first.
set "ACTUAL_PID="

:: Use wmic to find the real supervisor process
for /f "tokens=2 delims==" %%i in ('wmic process where "CommandLine like '%%quantforge_forward_supervisor.py%%'" get ProcessId /FORMAT:LIST 2^>nul ^| find "ProcessId="') do (
    set "ACTUAL_PID=%%i"
)

:: Trim whitespace from ACTUAL_PID
if defined ACTUAL_PID (
    for /f "tokens=*" %%a in ("%ACTUAL_PID%") do set "ACTUAL_PID=%%a"
)

:: Verify the PID is actually alive and belongs to our supervisor
set "SUPERVISOR_CONFIRMED=0"
if defined ACTUAL_PID (
    tasklist /FI "PID eq %ACTUAL_PID%" 2>nul | find /I "python" >nul
    if %ERRORLEVEL% EQU 0 (
        set "SUPERVISOR_CONFIRMED=1"
    )
)

if "%SUPERVISOR_CONFIRMED%"=="1" (
    echo Supervisor already running.
    echo PID: %ACTUAL_PID%
    echo.
    echo Use status_quantforge_forward.bat to check status.
    echo Use stop_quantforge_forward.bat to stop.
    exit /b 0
)

:: ── Step 2: No real supervisor found ──
:: Clean up stale lock if present
if exist "%LOCK_FILE%" (
    echo STALE LOCK DETECTED — cleaning up...
    del "%LOCK_FILE%" 2>nul
)

:: Clean up stale shutdown request if present
if exist "%LOG_DIR%\shutdown.req" del "%LOG_DIR%\shutdown.req" 2>nul

:: ── Step 3: Ensure MT5 terminal is running ──
echo Checking MT5 terminal...
tasklist /FI "IMAGENAME eq terminal64.exe" 2>nul | find /I "terminal64.exe" >nul
if %ERRORLEVEL% NEQ 0 (
    echo MT5 terminal not running. Starting Exness MT5...
    if exist "%MT5_PATH%" (
        start "" "%MT5_PATH%"
        echo Waiting for MT5 to initialize...
        timeout /t 8 /nobreak >nul
    ) else (
        echo.
        echo ========================================
        echo  FORWARD START BLOCKED
        echo  Reason: MT5 terminal not found
        echo  Expected: %MT5_PATH%
        echo ========================================
        echo.
        echo Please install MetaTrader 5 Exness and re-run this BAT.
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
echo.
echo Press Ctrl+C to stop, or use stop_quantforge_forward.bat
echo.

:: Run Python supervisor in foreground (command window stays open)
python -u scripts\forward\quantforge_forward_supervisor.py --mode forward
