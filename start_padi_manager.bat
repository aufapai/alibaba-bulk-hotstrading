@echo off
title PaDi UMKM Listing Manager - PT Indo Sukses Semesta
color 0a

echo ===================================================================
echo       PADI UMKM B2B LISTING MANAGER & PREVIEW EDITOR (2026)
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

echo [2/3] Membuka antarmuka Web UI di browser (http://localhost:8889)...
start http://localhost:8889

echo [3/3] Menjalankan server aplikasi lokal PaDi UMKM...
echo.
echo ===================================================================
echo  Aplikasi sedang berjalan! 
echo  - Live Preview & Link Editor: http://localhost:8889
echo  - Database: Database\padi_umkm_master.db (SQLite)
echo  - Folder Output Batch: Output_PadiUMKM/
echo  - Tekan tombol Ctrl + C di jendela ini untuk mematikan aplikasi.
echo ===================================================================
echo.

python App\padi_manager_app.py

pause
