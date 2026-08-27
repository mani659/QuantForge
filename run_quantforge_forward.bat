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

:: Check if supervisor is already running
if exist "%LOCK_FILE%" (
    echo Supervisor already running.
    echo.
    type "%LOCK_FILE%"
    echo.
    echo.
    echo Use status_quantforge_forward.bat to check status.
    echo Use stop_quantforge_forward.bat to stop.
    exit /b 0
)

:: Ensure MT5 terminal is running
echo Checking MT5 terminal...
tasklist /FI "IMAGENAME eq terminal64.exe" 2>nul | find /I "terminal64.exe" >nul
if %ERRORLEVEL% NEQ 0 (
    echo MT5 terminal not running. Starting Exness MT5...
    if exist "%MT5_PATH%" (
        start "" "%MT5_PATH%"
        echo Waiting for MT5 to initialize...
        timeout /t 5 /nobreak >nul
    ) else (
        echo WARNING: MT5 terminal not found at: %MT5_PATH%
        echo Please start MetaTrader 5 manually and re-run this BAT.
        exit /b 1
    )
) else (
    echo MT5 terminal already running.
)

:: Set MT5 terminal path for Python supervisor
set QF_MT5_TERMINAL_PATH=%MT5_PATH%

:: Ensure runtime directory exists
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:: Remove stale shutdown request if present
if exist "%LOG_DIR%\shutdown.req" del "%LOG_DIR%\shutdown.req"

echo.
echo Starting QuantForge Forward Supervisor...
echo CAND-015 + CAND-024 + CAND-035
echo.
echo Press Ctrl+C to stop, or use stop_quantforge_forward.bat
echo.

:: Run Python supervisor in foreground (command window stays open)
python -u scripts\forward\quantforge_forward_supervisor.py --mode forward
