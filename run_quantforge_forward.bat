@echo off
setlocal

cd /d "%~dp0"
set PYTHONPATH=%~dp0
set LOG_DIR=runtime\forward\supervisor
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo Starting QuantForge Unified Forward Supervisor...
python -u scripts\forward\quantforge_forward_supervisor.py --mode forward >> "%LOG_DIR%\supervisor.log" 2>&1
