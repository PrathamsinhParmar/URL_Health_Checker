@echo off
TITLE DownAlert URL Checker Loop

echo =======================================
echo    Background URL Checker Started
echo =======================================
echo The checks will run automatically every 5 minutes.
echo Keep this terminal window open to keep them running!
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment "venv" not found!
    echo Please make sure you have set up the project.
    pause
    exit /b 1
)

:: Activate the virtual environment
call venv\Scripts\activate.bat

:loop
echo =======================================
echo [%date% %time%] Running URL Checks...
python manage.py check_urls

echo.
echo Check complete. Waiting 5 minutes until next check...
timeout /t 300 /nobreak >nul
goto loop
