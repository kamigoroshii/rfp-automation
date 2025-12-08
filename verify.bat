@echo off
echo.
echo ============================================================
echo   RFP AUTOMATION SYSTEM VERIFICATION
echo ============================================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running verification script...
python verify_system.py

echo.
echo Press any key to exit...
pause >nul
