@echo off
chcp 65001 >nul
title Google Flow 10-Product Batch Studio - HOTS Trading
cls
echo ======================================================================
echo    🚀 GOOGLE FLOW 10-PRODUCT BATCH STUDIO (ALWAYS APPROVE)
echo    PT Indo Sukses Semesta / PT Waru Gunung - AP Boots & Petrova
echo ======================================================================
echo.
echo [INFO] Akun Google Flow : aufahots@gmail.com
echo [INFO] Target Project   : https://flow.google.com/project/5a88c3fd-477c-4eed-a126-f812ccfb079c
echo [INFO] Total Produk     : 10 Produk Teratas (40 Foto WebP + JSON)
echo.
echo Pilihan Eksekusi:
echo  [1] Buka Google Flow Project di Browser
echo  [2] Jalankan Auto-Generate 10 Produk (Always Approve) & Buat Paket ZIP
echo  [3] Keluar
echo.
set /p choice="Masukkan pilihan [1/2/3]: "

if "%choice%"=="1" (
    echo.
    echo Membuka Google Flow Project di browser...
    start https://flow.google.com/project/5a88c3fd-477c-4eed-a126-f812ccfb079c
    echo Browser dibuka.
    pause
    exit /b
)

if "%choice%"=="2" (
    echo.
    echo Menjalankan proses batching 10 produk...
    python scripts\generate_flow_10_batch.py
    echo.
    echo Paket ZIP 10 Produk telah disimpan di: Output\Flow_10_Products_Assets_HOTS.zip
    pause
    exit /b
)

exit /b

