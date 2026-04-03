@echo off
echo Starting E-Commerce Application...
echo.

echo Starting Backend Server...
start cmd /k "cd /d %~dp0 && uvicorn src.main:app --reload"

timeout /t 5 /nobreak > nul

echo Starting Frontend...
start cmd /k "cd /d %~dp0frontend && streamlit run app.py"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo API Docs: http://localhost:8000/docs
pause
