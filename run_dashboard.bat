@echo off
echo ========================================================
echo   Launching AI Road Guardian Dashboard (Streamlit)
echo ========================================================
cd /d "%~dp0"
.\.venv311\Scripts\python.exe -m streamlit run dashboard.py
pause
