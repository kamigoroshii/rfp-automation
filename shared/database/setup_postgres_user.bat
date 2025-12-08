@echo off
REM PostgreSQL User Setup Script for Windows
REM This script creates the rfp_user in PostgreSQL

echo ============================================================
echo PostgreSQL User Setup for RFP Automation System
echo ============================================================
echo.

REM Check if PostgreSQL is in PATH
where psql >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: psql command not found!
    echo.
    echo Please add PostgreSQL bin directory to your PATH, or run:
    echo   "C:\Program Files\PostgreSQL\XX\bin\psql" -U postgres
    echo.
    echo Replace XX with your PostgreSQL version number
    pause
    exit /b 1
)

echo This will create a PostgreSQL user 'rfp_user'
echo.
echo You will be prompted for:
echo   1. PostgreSQL superuser (postgres) password
echo   2. Password for the new rfp_user
echo.
echo IMPORTANT: Remember the password you set for rfp_user!
echo You'll need to update it in your .env file as DB_PASSWORD
echo.
pause

REM Run the SQL script
psql -U postgres -f "%~dp0create_user.sql"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo SUCCESS! User created successfully
    echo ============================================================
    echo.
    echo Next steps:
    echo   1. Update your .env file with:
    echo      DB_USER=rfp_user
    echo      DB_PASSWORD=^<password you just set^>
    echo.
    echo   2. Run: python shared/database/init_db.py
    echo ============================================================
) else (
    echo.
    echo ERROR: Failed to create user
    echo Please check the error messages above
)

pause
