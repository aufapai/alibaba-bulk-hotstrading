@echo off
chcp 65001 >nul
title HOTS Trading - Flow MCP to Photobank Automation Pipeline
color 0B

:MENU
cls
echo ==============================================================================
echo       HOTS TRADING - GOOGLE FLOW MCP TO PHOTOBANK INTEGRATION PIPELINE
echo       Target: https://admin.hotstrading.com/photo-bank
echo ==============================================================================
echo.
echo [1] Ekspor Seluruh Product Input (424 Slots) ke Format JSON
echo [2] Ekspor 1 SKU Tertentu ke Format JSON (Contoh: APB-016)
echo [3] Cek Status Koneksi Google Flow MCP ^& Sisa Kuota Harian
echo [4] Push Seluruh Gambar dari Folder ke Kategori Photobank
echo [5] Keluar
echo.
echo ==============================================================================
set /p opt="Pilih menu [1-5]: "

if "%opt%"=="1" goto EXPORT_ALL
if "%opt%"=="2" goto EXPORT_SKU
if "%opt%"=="3" goto CHECK_STATUS
if "%opt%"=="4" goto PUSH_EXISTING
if "%opt%"=="5" goto EXIT
goto MENU

:EXPORT_ALL
cls
echo [*] Mengekspor seluruh katalog 106 SKU x 4 Slot ke Output/flow_product_input_jobs.json...
python run_flow_photobank.py --export-json
echo.
pause
goto MENU

:EXPORT_SKU
cls
set /p target_sku="Masukkan Kode SKU (contoh APB-016 atau APB-001): "
python run_flow_photobank.py --export-json --sku %target_sku%
echo.
pause
goto MENU

:CHECK_STATUS
cls
echo [*] Memeriksa status server Google Flow MCP (http://127.0.0.1:8787)...
python run_flow_photobank.py --status
echo.
pause
goto MENU

:PUSH_EXISTING
cls
set /p folder_src="Masukkan nama folder gambar (default: Image Flow): "
if "%folder_src%"=="" set folder_src=Image Flow
python run_flow_photobank.py --push-existing "%folder_src%"
echo.
pause
goto MENU

:EXIT
exit
