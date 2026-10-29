@echo off
title Photobank Image Generation Template Generator
echo ===================================================================
echo     PHOTOBANK IMAGE GENERATION TEMPLATE GENERATOR (ALIBABA SOP)
echo               PT Indo Sukses Semesta - AP Boots
echo ===================================================================
echo.
cd /d "%~dp0"
python generate_image_prompts.py
echo.
echo ===================================================================
echo Selesai! File CSV hasil generate tersedia di folder ini:
echo 1. Alibaba_Master_106_SKU_ImageGen_Ready.csv (106 SKU lengkap dari database)
echo 2. Alibaba_Bulk_Template_With_Prompts.csv (Hasil proses template input)
echo 3. Alibaba_Template_Input_Kosong.csv (Template kosong untuk tambah produk)
echo ===================================================================
pause
