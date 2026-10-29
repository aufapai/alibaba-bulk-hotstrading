@echo off
title Alibaba November 2026 Batch Generator - PT Indo Sukses Semesta
color 0b

echo ===================================================================
echo     GENERATOR BATCH ALIBABA NOVEMBER 2026 + PHOTOBANK WEBP
echo            PT Indo Sukses Semesta - AP Boots Indonesia
echo ===================================================================
echo.
echo [1/3] Memeriksa Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak terdeteksi! Pastikan Python telah terinstall.
    pause
    exit /b
)

echo.
echo [2/3] Mengonversi gambar di Image Flow ke WebP Photobank...
python App\convert_photobank_webp.py
if errorlevel 1 (
    echo [ERROR] Gagal mengonversi gambar ke WebP!
    pause
    exit /b
)

echo.
echo [3/3] Memperbarui Database & Membuat Excel Batch November 2026...
python App\build_alibaba_photobank_batch.py
if errorlevel 1 (
    echo [ERROR] Gagal membuat file batch November!
    pause
    exit /b
)

echo.
echo ===================================================================
echo  Proses selesai!
echo  - File Excel : Output\Alibaba_Bulk_Upload_November_2026.xlsx
echo  - WebP Folder: Output\Photobank_WebP\
echo  - Upload Link: https://admin.hotstrading.com/photo-bank
echo ===================================================================
echo.
pause
