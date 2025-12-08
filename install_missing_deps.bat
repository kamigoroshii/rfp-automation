@echo off
REM Install missing dependencies for RFP Automation System

echo ============================================================
echo Installing Missing Dependencies
echo ============================================================
echo.

REM Activate virtual environment if not already active
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo Installing google-generativeai...
pip install google-generativeai==0.3.2

echo.
echo ============================================================
echo Verifying installation...
echo ============================================================
python -c "import google.generativeai as genai; print('✅ google-generativeai installed successfully')"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo SUCCESS! All dependencies installed
    echo ============================================================
    echo.
    echo You can now run:
    echo   uvicorn orchestrator.api.main:app --reload --port 8000
    echo.
) else (
    echo.
    echo ❌ Installation verification failed
    echo Please check the error messages above
)

pause
