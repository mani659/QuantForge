@echo off
setlocal

:: QUANTFORGE - CAND-015 AUTONOMOUS FORWARD RUNNER
:: Usage: run_cand015_forward.bat <duration_hours>
:: Example: run_cand015_forward.bat 12

set DURATION=%1
if "%DURATION%"=="" set DURATION=12

echo Starting CAND-015 Forward Runner for %DURATION% hours...
echo Log will be written to the session directory's runner.log

:: Ensure we are in the QuantForge repository root (assuming script is in root)
cd /d "%~dp0"

:: Launch the standalone runner in the background (or foreground)
:: Windows safe detachment is typically handled by the user just minimizing this cmd window,
:: but if they want to detach they can run it via pythonw or start /b
python -m research.g6_forward.run_long_observation --duration-hours %DURATION%

set EXIT_CODE=%ERRORLEVEL%
if %EXIT_CODE% NEQ 0 (
    echo [FATAL ERROR] Runner terminated with exit code %EXIT_CODE%
) else (
    echo Runner terminated successfully.
)

exit /b %EXIT_CODE%
