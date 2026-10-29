@echo off
title Nano Banana AI Product Image Generator - AP Boots
color 0b

echo ===================================================================
echo     NANO BANANA AI PRODUCT IMAGE GENERATION (ALIBABA SOP)
echo            PT Indo Sukses Semesta - AP Boots
echo ===================================================================
echo.
echo [1/3] Memeriksa Python & Environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak terdeteksi! Pastikan Python telah terinstall.
    pause
    exit /b
)

echo [2/3] Memperbarui daftar produk dari database (products.csv)...
python App\prepare_products_csv.py

echo.
echo [3/3] Menjalankan automasi generate gambar Nano Banana...
echo.
python run_nanobanana.py

echo.
echo ===================================================================
echo  Proses selesai! Silakan periksa folder output_images/
echo ===================================================================
echo.
pause
