@echo off
setlocal

cd /d "%~dp0"
set REQ_DIR=runtime\forward\supervisor
if not exist "%REQ_DIR%" mkdir "%REQ_DIR%"

echo Requesting QuantForge Unified Forward Supervisor to stop...
echo shutdown > "%REQ_DIR%\shutdown.req.tmp"
ren "%REQ_DIR%\shutdown.req.tmp" shutdown.req

echo Shutdown request sent. Supervisor will exit cleanly on next tick.
