@echo off
chcp 65001 >nul
title Setup GTAI-1/flow-mcp ^& Registrasi ke Antigravity IDE
color 0A

echo ==============================================================================
echo             SETUP GOOGLE FLOW MCP (GTAI-1/flow-mcp) UNTUK WINDOWS
echo ==============================================================================
echo.
echo Modul ini akan:
echo  1. Meng-clone repository GTAI-1/flow-mcp ke C:\Users\%USERNAME%\flow-mcp
echo  2. Menjalankan npm install ^& npm run build
echo  3. Membuka Chrome khusus untuk login Google Flow sekali saja (npm run login)
echo.
set /p confirm="Lanjutkan proses setup sekarang? [Y/N]: "
if /i not "%confirm%"=="Y" exit /b

set TARGET_DIR=C:\Users\%USERNAME%\flow-mcp

if not exist "%TARGET_DIR%" (
    echo.
    echo [*] Meng-clone repository ke %TARGET_DIR%...
    git clone https://github.com/GTAI-1/flow-mcp.git "%TARGET_DIR%"
) else (
    echo.
    echo [*] Folder %TARGET_DIR% sudah ada. Mengambil update terbaru...
    cd /d "%TARGET_DIR%"
    git pull
)

cd /d "%TARGET_DIR%"

echo.
echo [*] Menginstal dependensi Node.js...
call npm install

echo.
echo [*] Mem-build Flow MCP TypeScript project...
call npm run build

echo.
echo ==============================================================================
echo [!] LANGKAH LOGIN SATU KALI:
echo Jendela Google Chrome terisolasi akan terbuka.
echo Silakan login akun Google Anda, buka Flow (flow.google.com), dan buat/pilih 1 project.
echo ==============================================================================
echo.
pause
call npm run login

echo.
echo ==============================================================================
echo [✓] Setup Flow MCP Selesai!
echo Untuk menjalankan local server Studio Flow MCP kapan saja:
echo   cd /d %TARGET_DIR%
echo   npm run studio
echo   (Buka di browser: http://127.0.0.1:8787)
echo ==============================================================================
pause
