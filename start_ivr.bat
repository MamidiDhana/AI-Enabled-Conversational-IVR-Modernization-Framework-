@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start_ivr.ps1"
if errorlevel 1 (
	echo.
	echo Launch failed. Check the error above.
	pause
)
