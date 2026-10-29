@echo off
title Update Produk Alibaba - PT Indo Sukses Semesta
color 0b

echo ===================================================================
echo       UPDATE DATA PRODUK ALIBABA (XLSX / CSV) - 2026
echo             PT Indo Sukses Semesta - AP Boots
echo ===================================================================
echo.
echo [1/2] Memeriksa Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak terdeteksi! Pastikan Python telah terinstall.
    pause
    exit /b
)

echo [2/2] Menjalankan pemilih file data produk (XLSX / CSV)...
echo.

python App\product_data_loader.py %1

echo.
pause
