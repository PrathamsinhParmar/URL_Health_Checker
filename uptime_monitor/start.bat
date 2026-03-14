@echo off
TITLE DownAlert Server

echo =======================================
echo     Starting DownAlert Server
echo =======================================
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

:: Open the default browser to the project URL
echo Opening homepage in your default browser...
start http://127.0.0.1:8000/

:: Start the Django server
echo Starting the Django development server...
echo Press Ctrl+C to stop the server anytime.
echo.
python manage.py runserver

pause
