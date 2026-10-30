@echo off
title Alibaba & Photobank Manager - PT Indo Sukses Semesta
color 0b

echo ===================================================================
echo   ALIBABA & PHOTOBANK CATALOG MANAGER (2026)
echo             PT Indo Sukses Semesta - AP Boots
echo ===================================================================
echo.
echo [1/3] Memeriksa instalasi Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak terdeteksi! Pastikan Python telah terinstall.
    pause
    exit /b
)

echo [2/3] Membuka antarmuka Web GUI di browser (http://localhost:8888)...
start http://localhost:8888

echo [3/3] Menjalankan server aplikasi lokal & database SQLite...
echo.
echo ===================================================================
echo  Aplikasi Web GUI sedang berjalan!
echo  - Web Dashboard: http://localhost:8888
echo  - Shopee Official Studio: http://localhost:8888 (Tab Shopee Studio)
echo  - Photobank 4-Slot Studio: Native Standalone Engine (Tanpa MCP)
echo  - Database Terpadu: Database\alibaba_master.db (SQLite)
echo  - Fitur: Bulk Selection, Custom Slot Gen, Auto Upscale 85%% Frame
echo  - Tekan tombol Ctrl + C di jendela ini untuk mematikan aplikasi.
echo ===================================================================
echo.

python App\alibaba_manager_app.py

pause

