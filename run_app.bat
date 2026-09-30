@echo off
echo ========================================================
echo   Launching AI Road Guardian (Voice Assistant)
echo ========================================================
cd /d "%~dp0"
.\.venv311\Scripts\python.exe app_voice.py
pause
