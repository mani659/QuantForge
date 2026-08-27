@echo off
setlocal

cd /d "%~dp0"
set PYTHONPATH=%~dp0
set LOG_DIR=runtime\forward\supervisor
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:: Check if supervisor is already running
set LOCK_FILE=%LOG_DIR%\supervisor.lock
if exist "%LOCK_FILE%" (
    echo Supervisor may already be running.
    echo Check with: status_quantforge_forward.bat
    exit /b 1
)

echo Starting QuantForge Unified Forward Supervisor (detached)...
start "" /b python -u scripts\forward\quantforge_forward_supervisor.py --mode forward >> "%LOG_DIR%\supervisor.log" 2>&1

:: Brief pause to let the process start and write lock file
timeout /t 2 /nobreak >nul

if exist "%LOCK_FILE%" (
    echo Supervisor started successfully.
    echo Check status: status_quantforge_forward.bat
    echo Stop: stop_quantforge_forward.bat
) else (
    echo WARNING: Supervisor may have failed to start.
    echo Check log: %LOG_DIR%\supervisor.log
)
