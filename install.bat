@echo off
echo Visual Studio Project Generator - Windows Setup
echo ==============================================

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo Failed to install dependencies
    echo Try running as administrator or check your internet connection
    pause
    exit /b 1
)

echo Setup completed successfully!
echo.
echo How to run:
echo   GUI Version: python GUIprojBuilder.py
echo   CLI Version: python CLIprojBuilder.py
echo.
pause
