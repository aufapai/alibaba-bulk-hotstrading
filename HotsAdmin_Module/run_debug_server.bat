@echo off
title HOTS Admin Module - Local Debug Server
color 0B
echo ================================================================
echo    HOTS TRADING - B2B EXPORT MODULE LOCAL DEBUG LAUNCHER
echo ================================================================
echo.

set PHP_EXE=php
where php >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    if exist "C:\php-8.5.1-nts-Win32-vs17-x64\php.exe" (
        set PHP_EXE=C:\php-8.5.1-nts-Win32-vs17-x64\php.exe
    )
)

"%PHP_EXE%" -v >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] PHP detected: %PHP_EXE%
    echo Starting PHP Built-in Web Server at http://localhost:8000 ...
    echo.
    echo Press Ctrl+C to stop the server.
    echo.
    start http://localhost:8000
    "%PHP_EXE%" -S localhost:8000 -t "%~dp0"
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] PHP CLI is not in system PATH.
    echo Running automated diagnostics via Python...
    echo.
    python "%~dp0scripts\test_module_connection.py"
    echo.
    echo Tip: To test the web UI locally, please transfer this folder to
    echo your cPanel public_html or run with a local PHP server (XAMPP/Laragon).
    pause
    goto end
)

echo [WARN] Neither PHP nor Python was detected in PATH.
pause

:end
