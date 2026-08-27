@echo off
setlocal

cd /d "%~dp0"

echo Installing QuantForge Forward Supervisor scheduled task...
echo This task will run under the CURRENT USER context to ensure access to the local MT5 installation.
echo.

schtasks /create /tn "QuantForgeForwardSupervisor" /tr "cmd.exe /c \"\"%~dp0run_quantforge_forward.bat\"\"" /sc onstart /ru "%USERNAME%" /F

echo.
echo Task installed. To start it now, you can run: run_quantforge_forward.bat
echo Or use Task Scheduler (taskschd.msc) to run/enable it.
