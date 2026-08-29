@echo off
setlocal

cd /d "%~dp0"
set REQ_DIR=runtime\forward\supervisor
if not exist "%REQ_DIR%" mkdir "%REQ_DIR%"

:: ── Detect actual supervisor via PowerShell ──
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

if "%SUPERVISOR_CONFIRMED%"=="0" (
    echo Supervisor not running.
    echo.
    echo If status.json shows RUNNING, that record is stale.
    echo The actual process is not alive.
    echo.
    pause >nul
    exit /b 0
)

:: ── Send graceful shutdown request ──
echo Requesting QuantForge Forward Supervisor to stop...
echo Shutdown target PID: %ACTUAL_PID%
echo shutdown > "%REQ_DIR%\shutdown.req.tmp"
ren "%REQ_DIR%\shutdown.req.tmp" shutdown.req

echo Shutdown request sent. Supervisor will exit cleanly on next tick.
echo.

:: ── Wait for clean exit ──
echo Waiting for supervisor to stop...
set "WAIT_COUNT=0"
:WAIT_LOOP
timeout /t 2 /nobreak >nul
set /a WAIT_COUNT+=2

:: Check if process still exists
set "STILL_RUNNING=0"
tasklist /FI "PID eq %ACTUAL_PID%" 2>nul | find /I "python" >nul
if %ERRORLEVEL% EQU 0 (
    set "STILL_RUNNING=1"
)

if "%STILL_RUNNING%"=="1" (
    if %WAIT_COUNT% LSS 30 (
        echo   Waiting... (%WAIT_COUNT%s)
        goto WAIT_LOOP
    ) else (
        echo.
        echo WARNING: Supervisor did not exit within 30 seconds.
        echo You may need to forcefully terminate PID %ACTUAL_PID%.
        echo.
        pause >nul
        exit /b 1
    )
)

echo Supervisor stopped successfully.
echo.
pause >nul
exit /b 0
