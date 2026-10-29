# PANDUAN INTEGRASI FLOW MCP DENGAN PRODUCT INPUT & PUSH PHOTOBANK
**HOTS Trading — Solusi Otomasi AI Photo Generator Tanpa Biaya API Pay-Per-Use**  
*Target Website: `https://admin.hotstrading.com/photo-bank` • Flow MCP: `https://github.com/GTAI-1/flow-mcp`*  
**Versi:** 1.0 (Oktober 2026) | **Folder:** `App/flow_photobank/`

---

## 1. LATAR BELAKANG & TUJUAN ARSITEKTUR

Sebelumnya, penggunaan API Gemini langsung (`gemini-2.5-flash-image` pada `run_nanobanana.py`) terkendala oleh `QUOTA_LIMIT_0` (memerlukan billing GCP/AI Studio aktif).

Dengan menggunakan **`GTAI-1/flow-mcp`**, kita dapat:
1. **Memanfaatkan Kuota Gratis Google Flow (`flow.google.com`)**: Setiap akun Google mendapatkan **50 kredit gratis per hari** (atau kuota dari paket langganan Google AI Pro/One), dan **0 kredit (gratis tak terbatas)** untuk batch gambar menggunakan fitur Agent mode (`flow_agent_images`).
2. **Otomasi Langsung via Chrome DevTools Protocol (CDP)**: Berjalan di komputer lokal (Windows/Mac) tanpa memerlukan ekstensi browser tambahan.
3. **Integrasi Penuh dengan Product Input**: Menghubungkan katalog produk lokal kita (106 SKU x 4 Slot Foto = 424 Jobs) langsung ke Flow MCP dalam format JSON standar.
4. **Push Otomatis ke Folder Photobank**: Hasil foto yang di-render otomatis dikonversi ke WebP berkualitas tinggi, diberi nama file ber-prefix SKU standar (`[SKU]_[Model]_[Slot].webp`), dan dimasukkan ke 11 folder kategori resmi siap unggah ke Photobank Admin (`https://admin.hotstrading.com/photo-bank`).

---

## 2. STRUKTUR MODUL DAN FILE SISTEM

Komponen integrasi telah terpasang rapi di dalam proyek:

```
Product Input/
├── run_flow_photobank.py         # [CLI MASTER] Runner utama pipeline JSON & Photobank
├── run_flow_photobank.bat        # [ONE-CLICK LAUNCHER] Menu interaktif Windows
├── setup_flow_mcp.bat            # [AUTO INSTALLER] Script setup repo GTAI-1/flow-mcp
│
├── App/
│   └── flow_photobank/           # 📦 CORE PACKAGE INTEGRASI
│       ├── __init__.py           # Inisialisasi package
│       ├── category_mapper.py    # Pemetaan SKU ke 11 folder kategori Photobank & nama file
│       ├── product_json_exporter.py # Ekstraktor Product Input ke format JSON terstandarisasi
│       ├── flow_mcp_client.py    # Client HTTP/API ke server lokal Flow MCP (port 8787)
│       ├── photobank_pusher.py   # Pengubah ke WebP, pemilah folder, & pengupdate manifest
│       └── pipeline.py           # Master orchestrator alur end-to-end
│
├── Output/
│   ├── flow_product_input_jobs.json # File JSON berisi 424 jobs prompt siap pakai
│   └── Photobank_Siap_Upload/    # 📁 11 FOLDER KATEGORI RESMI PHOTOBANK
│       ├── 01_Safety_Boots/
│       ├── 02_Terra_Series/
│       ├── 03_Orca_Series/
│       ├── 04_Chef_Series/
│       ├── 05_Medic_Series/
│       ├── 06_Biker_Casual/
│       ├── 07_Classic_Boots/
│       ├── 08_Kids_Boots/
│       ├── 09_Sandals_Clogs/
│       ├── 10_Kasual_Sneakers/
│       ├── 11_General_Lifestyle_Boots/
│       └── DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv # Master manifest mapping
```

---

## 3. FORMAT PAYLOAD JSON PRODUCT INPUT

File `Output/flow_product_input_jobs.json` menyajikan seluruh instruksi render dalam format terstruktur:

```json
{
  "job_id": "APB-016_slot_1_hero",
  "sku": "APB-016",
  "product_name": "AP MAX / S5",
  "full_title": "AP Boots MAX S5 - Sepatu Boot Safety PVC Steel Toe",
  "slot_key": "slot_1_hero",
  "slot_label": "Slot 1 - Hero White BG",
  "target_folder": "01_Safety_Boots",
  "category_group": "AP Safety Boots",
  "target_filename": "APB-016_ap_max_s5_slot_1_hero.webp",
  "reference_image": "https://p16-images-comn-sg.tokopedia-static.net/.../ref.jpeg",
  "prompt": "Using the attached reference photos, create a professional e-commerce commercial studio product photograph of AP Boots MAX S5...",
  "flow_payload": {
    "prompt": "Using the attached reference photos, create a professional e-commerce...",
    "type": "image",
    "aspect": "1:1",
    "resolution": "1080p",
    "reference_images": [
      "https://p16-images-comn-sg.tokopedia-static.net/.../ref.jpeg"
    ],
    "max_credits": 0
  },
  "status": "ready"
}
```

---

## 4. PEMETAAN 11 FOLDER PHOTOBANK RESMI

Agar saat diunggah ke `https://admin.hotstrading.com/photo-bank` foto **otomatis terdeteksi sebagai `product`** (tidak masuk ke `unmatched`), sistem menggunakan penamaan dan folder:

| No | Folder Kategori | Kategori Grup | Contoh SKU & Format Nama File |
|---|---|---|---|
| 1 | `01_Safety_Boots/` | AP Safety Boots | `APB-016_ap_max_s5_slot_1_hero.webp`, `APB-019_metaguard...` |
| 2 | `02_Terra_Series/` | AP Terra Series | `APB-015_ap_terra_gp_hitam_slot_2_side.webp`, `APB-007_...` |
| 3 | `03_Orca_Series/` | AP Orca Series | `APB-024_ap_orca_industrial_slot_3_tread.webp` |
| 4 | `04_Chef_Series/` | AP Chef Series | `APB-021_ap_chef_series_slot_4_contextual.webp` |
| 5 | `05_Medic_Series/` | AP Medic Series | `APB-022_ap_medic_series_slot_1_hero.webp` |
| 6 | `06_Biker_Casual/` | AP Biker & Casual | `APB-001_ap_allbike_slot_1_hero.webp`, `APB-013_allbike_2...` |
| 7 | `07_Classic_Boots/` | AP Classic Boots | `APB-006_ap_boots_2003_hijau_tricolour...`, `APB-005_...` |
| 8 | `08_Kids_Boots/` | AP Kids Boots | `APB-017_ap_kids_safari_series...`, `APB-018_kids_2012...` |
| 9 | `09_Sandals_Clogs/` | AP Sandals & Clogs | `APB-011_ap_clogs...`, `APB-032_sandal_series...` |
| 10 | `10_Kasual_Sneakers/` | AP Kasual Sneakers | `APB-014_ap_969_bola_series...`, `APB-033_star_series...` |
| 11 | `11_General_Lifestyle_Boots/` | General & Lifestyle | `APB-GEN_general_boots_slot_4_contextual.webp` |

---

## 5. PANDUAN PENGGUNAAN CEPAT (SOP)

### Langkah 1: Setup GTAI-1/flow-mcp (Satu Kali Saja)
1. Jalankan script installer:
   ```cmd
   setup_flow_mcp.bat
   ```
2. Saat jendela Chrome khusus terbuka, login akun Google Anda, buka `flow.google.com`, dan buat/buka 1 project Flow.

### Langkah 2: Daftarkan Flow MCP ke Antigravity IDE (Opsional)
Buka file `C:\Users\ADVAN\.gemini\antigravity-ide\mcp_config.json`, lalu tambahkan baris berikut di dalam `"mcpServers"`:
```json
"flow": {
  "command": "node",
  "args": ["C:\\Users\\ADVAN\\flow-mcp\\dist\\index.js"]
}
```

### Langkah 3: Ekspor Product Input ke JSON
Cukup jalankan batch file:
```cmd
run_flow_photobank.bat
```
Lalu pilih opsi `[1]` untuk mengekspor 424 jobs, atau gunakan CLI:
```bash
python run_flow_photobank.py --export-json
```

### Langkah 4: Push Gambar ke Folder Photobank
Jika Anda memiliki folder berisi gambar yang sudah di-generate (misalnya dari folder `Image Flow/`), dorong seluruhnya ke Photobank dengan:
```bash
python run_flow_photobank.py --push-existing "Image Flow"
```
Foto akan otomatis di-convert ke WebP beresolusi 1600x1600, disortir ke subfolder kategori Photobank yang sesuai, dan manifest `DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv` akan diperbarui secara otomatis!

---

## 6. SINKRONISASI KE ADMIN PHOTOBANK WEBSITE

Setelah foto berada di `Output/Photobank_Siap_Upload/`:
1. Buka browser ke **`https://admin.hotstrading.com/photo-bank`**.
2. Unggah per folder (misal `01_Safety_Boots`).
3. Karena setiap file sudah memiliki nama yang diawali kode SKU dan model yang jelas, sistem Photobank akan langsung membaca dan mengelompokkannya sebagai **`product`** dengan SKU terkait secara akurat.
4. Klik **Export CSV** di Photobank Admin untuk mendapatkan daftar tautan CDN gambar yang siap dipakai pada listing Alibaba B2B!
