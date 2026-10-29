@echo off
title Alibaba & Multi-Marketplace Manager - PT Indo Sukses Semesta
color 0b

echo ===================================================================
echo   ALIBABA & MULTI-MARKETPLACE CATALOG MANAGER (2026)
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
echo  - Database Terpadu: Database\alibaba_master.db (SQLite)
echo  - Marketplace Terhubung: Lazada, Blibli, Tokopedia, Shopee
echo  - Matriks B2B: Alibaba 800 Listing Matrix (10 Industry Angles)
echo  - Fitur: 1-Click Sync, Smart Image Deduplicator, Keyword Bot
echo  - Tekan tombol Ctrl + C di jendela ini untuk mematikan aplikasi.
echo ===================================================================
echo.

python App\alibaba_manager_app.py

pause
