# PANDUAN FITUR LENGKAP HOTSADMIN_MODULE & SINKRONISASI PRODUCT INPUT
**HOTS Trading — B2B Alibaba Export Hub, Pricing Engine & Photobank Automation**  
*Target Server: `https://admin.hotstrading.com/` & `https://admin.hotstrading.com/photo-bank`*  
**Versi:** 3.0 (Oktober 2026) | **Folder:** `HotsAdmin_Module/`

---

## 1. RINGKASAN ARSITEKTUR & INTEGRASI SISTEM

Modul [`HotsAdmin_Module/`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module) adalah core backend OOP (Pure PHP 7.4 - 8.5+) yang berfungsi sebagai **jembatan data terpadu** antara:
1. **Katalog Master Produk Lokal** (`products.csv` & `photobank generator/Alibaba_Master_106_SKU_ImageGen_Ready.csv`).
2. **AI Image Generation Pipeline** ([GTAI-1/flow-mcp](https://github.com/GTAI-1/flow-mcp) via port `8787`).
3. **Penyimpanan Gambar Resmi Photobank** (`Output/Photobank_Siap_Upload/` dengan 11 subfolder kategori).
4. **Server Produksi cPanel MariaDB / MySQL** (`admin.hotstrading.com`).

```
[Product Input (106 SKU)] 
       │
       ▼ (run_flow_photobank.py --export-json)
[Output/flow_product_input_jobs.json (424 Jobs)]
       │
       ▼ (Flow MCP Google Flow Automation - 0 Credits)
[Gambar Render WebP (1600x1600)]
       │
       ▼ (Photobank Pusher & Prefix Matcher)
[Output/Photobank_Siap_Upload/ (11 Kategori)] <====== (Auto Sync) ======> [HotsAdmin_Module]
       │                                                                      │
       ▼ (Browser Drag & Drop / API Sync)                                     ▼
[https://admin.hotstrading.com/photo-bank]                       [HotsAdmin Master Dashboard GUI]
```

---

## 2. KATALOG FITUR UTAMA DI HOTSADMIN_MODULE

### 🧮 Fitur 1: Kalkulator Kemasan Master Karton & Kontainer (CBM Engine)
* **Kalkulasi Kubikasi CBM:**
  - Standar karton 12 pasang: **0.096 m³** (dimensi: 60 x 40 x 40 cm).
  - Skalabilitas otomatis untuk karton berisi 18 pasang (0.120 m³) atau custom.
  - Berat kotor estimasi: 1.7 kg / pasang boot.
* **Kapasitas Muat Kontainer Internasional:**
  - **Kontainer 20ft (Volume efektif 28 CBM):** Memuat **291 Karton** (~3.492 Pasang).
  - **Kontainer 40ft HC (Volume efektif 68 CBM):** Memuat **708 Karton** (~8.496 Pasang).
* **Tiering Fee Layanan Ekspor HOTS:**
  - **Member Regular:** **2%** dari nilai FOB.
  - **Non-Member Mandiri:** **5%** dari nilai FOB.
  - **Full Assistance (Mitra Terpandu):** **15%** dari nilai FOB.

### 💵 Fitur 2: Layanan Kurs Valas Real-Time (Forex Service USD/IDR)
* Live feed kurs USD terhadap Rupiah langsung dari Google Finance / Exchangerate API.
* Dilengkapi sistem caching otomatis selama 30 menit di `cache/forex_cache.json` untuk mencegah overhead request dan menjaga performa web server.
* Otomatis mengonversi harga modal IDR ke estimasi harga FOB USD pelabuhan muat (Tanjung Priok / Tanjung Perak).

### 🎯 Fitur 3: Generator AI Photo Prompts 4-Slot (Standar Alibaba B2B)
Menghasilkan 4 prompt studio profesional untuk setiap SKU secara otomatis:
1. **Slot 1 (Hero White BG):** Tampak depan serong 3/4, berdiri tegak, latar belakang putih mulus tanpa bayangan keras (RGB 255,255,255).
2. **Slot 2 (Side Profile):** Tampak samping lurus 90 derajat, memperlihatkan profil sol, kelengkungan tumit, dan tinggi shaft.
3. **Slot 3 (Outsole Tread Detail):** Bidikan detail tapak sol bawah, memperlihatkan alur grip anti-slip dan pembuangan lumpur.
4. **Slot 4 (Contextual In-Use):** Foto in-use pemakaian di tempat kerja nyata sesuai target intelijen pasar 5 benua (Eropa, Amerika, ASEAN, Timur Tengah, Oseania).

### 🗄️ Fitur 4: Dual Driver Database (MySQL MariaDB cPanel + SQLite Auto-Diagnostic)
* Menghubungkan sistem ke database MySQL cPanel server live (`hotj4796_hotstrading`).
* Apabila koneksi server belum terpasang atau sedang offline di komputer lokal, sistem otomatis beralih ke local mock / SQLite fixture tanpa memicu fatal error (*Zero Crash Guarantee*).

### 🔄 Fitur 5: Sync Flow MCP & Photobank Hub
Fitur terintegrasi di antarmuka web dashboard ([`index.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/index.php)) dan REST API:
* **Monitoring Status 11 Kategori Photobank:** Membaca jumlah file dan kesiapan upload di setiap subfolder `Output/Photobank_Siap_Upload/`.
* **Live Flow MCP Jobs Inspector:** Antarmuka pencarian cepat job JSON untuk SKU mana saja (misal `APB-016`), menampilkan prompt dan parameter teknis secara real-time.
* **Sinkronisasi Otomatis:** Tombol 1-klik untuk merefresh hitungan file dan memvalidasi keutuhan manifest `DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv`.

### ⭐ Fitur 6 (PORT DARI ALIBABA MANAGER): Smart Top Pick Generator B2B
Porting lengkap dari fitur `start_alibaba_manager.bat` (`App/alibaba_manager_app.py`) ke web interface:
* **Kurasi Produk Otomatis Berdasarkan Negara & Sudut Industri:** Pilih negara tujuan (Jerman, AS, Malaysia, UAE, Australia, dsb.) dan sudut vertikal industri (Civil Construction, Agriculture, Oil & Gas, Hygiene, Mining, dsb.).
* **Accio 2026 SEO Title Generator:** Otomatis menghasilkan judul listing B2B bahasa Inggris berstandar Alibaba Accio AI yang memaksimalkan click-through rate buyer internasional.
* **Tiered FOB Pricing Calculation:** Menghitung 4 tingkatan harga FOB (100 psg, 500 psg, 1.000 psg, dan >1.000 psg) berdasarkan kurs valas live.
* **Kapasitas Muatan Master Karton & Kontainer:** Detail muatan 20ft dan 40ft HC langsung tertera di setiap kartu produk, siap disalin sebagai payload listing.

### 🌍 Fitur 7 (PORT DARI ALIBABA MANAGER): Intelijen Pasar 5 Benua & 10 Accio Angles
* **Analisis Musiman Q1 - Q4:** Pemicu kebutuhan musiman kuartalan (winter construction, flood emergency, harvest season, dry season refinery maintenance).
* **Regulasi & Sertifikasi Wajib:** Rangkuman standar kepatuhan per wilayah (CE Marking & EN 20345 untuk Eropa, ASTM F2413 & OSHA untuk Amerika, AS/NZS 2210 untuk Oseania, SASO untuk Timur Tengah, SNI untuk ASEAN).
* **10 Vertikal Matriks Accio 2026:** Pemetaan kata kunci buyer berintensitas tinggi, persona pembeli, dan rekomendasi model AP Boots yang tepat.

### 📤 Fitur 8 (MASTER LISTING DARI DOCS): Alibaba Listing & 57-Kolom Bulk Export Generator
Fitur yang dibangun 100% mengikuti standar `Doc/ALIBABA_LISTING_GENERATOR_MASTER_PROMPT.md` dan `Doc/PANDUAN_DAN_SPESIFIKASI_BULK_UPLOAD_ALIBABA_2026.md`:
* **Input Data Produk:** Mendukung input manual atau muat cepat dari katalog master (Brand, SKU, Model, Color, Size Range, Material, Certification, Origin, MOQ, OEM, Application, Harga FOB USD & IDR).
* **SEO Keyword Research Generator:** Menghasilkan Primary keyword, 6 Secondary keywords, 5 Long-tail keywords, Buyer intent, Commercial, Export, dan Wholesale keywords.
* **5 Kandidat Judul B2B (Max 128 Karakter):** Formula resmi `[Brand] + [Model] + [USP/Feature] + [Material] + [Industry Application] for [Country] Market`.
* **6 Keunggulan Utama (USPs) & Spesifikasi Lengkap:** Termasuk kode HS resmi Indonesia untuk boots tahan air (`6401.92.00`).
* **Description Builder V6 HTML (Strict Alibaba Compatible):** Kode HTML terstandarisasi hanya menggunakan tag yang diizinkan Alibaba (`table`, `tr`, `td`, `font`, `b`, `p`, `img`), bebas flexbox/grid/scripts sehingga 100% aman dan tidak di-strip oleh Alibaba.
* **15 B2B Buyer FAQs:** Tanya jawab komersial & teknis (MOQ, sampel, sertifikasi, kapasitas kontainer 20ft/40ft, Incoterms FOB/CIF, pembayaran T/T & L/C).
* **Direct 57-Column CSV Download:** Export 1-klik seluruh katalog produk atau SKU tertentu ke file CSV standar Alibaba Bulk Upload dengan encoding UTF-8 BOM yang langsung dapat dibuka di Microsoft Excel dan diunggah ke Alibaba Supplier Center.

---

## 3. DAFTAR REST API ENDPOINTS

Endpoint berikut mengembalikan format JSON terstandarisasi dengan header CORS aktif (atau file download CSV):

| Endpoint | Method | Parameter Contoh | Fungsi & Deskripsi |
|---|---|---|---|
| [`api/export_alibaba_bulk.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api/export_alibaba_bulk.php) | `GET` | `?format=csv&country=Germany` | **Direct 57-Column CSV Bulk Download**. Menghasilkan file CSV siap upload ke Alibaba Supplier Center dengan 57 kolom resmi. |
| [`api/generate_alibaba_listing.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api/generate_alibaba_listing.php) | `GET`/`POST`| `?sku=APB-001` | **Full Alibaba Listing Generator**. Menghasilkan SEO keywords, 5 title candidates, USPs, specs, 15 FAQs, dan Description Builder V6 HTML. |
| [`api/smart_top_picks.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api/smart_top_picks.php) | `GET` | `?country=Germany&angle=Civil+Construction&limit=3` | **Smart Top Pick Generator**. Menghasilkan paket kurasi ekspor, judul Accio 2026, harga berjenjang FOB, dan kalkulasi kontainer. |
| [`api/market_intelligence.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api/market_intelligence.php) | `GET` | `?quarter=Q4` | **Intelijen Pasar 5 Benua & 10 Accio Angles**. Panduan regulasi sertifikasi, tren musiman kuartal Q1-Q4, dan kata kunci target. |
| [`api/photobank_sync.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api/photobank_sync.php) | `GET` | - | **Status Sinkronisasi Photobank**. Mengembalikan total file di 11 folder kategori, jumlah entri manifest, dan status folder. |
| [`api/flow_jobs.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api/flow_jobs.php) | `GET` | `?sku=APB-016&limit=10` | **Flow MCP Jobs Provider**. Mengembalikan daftar job prompt JSON siap kirim ke Google Flow MCP. |
| [`api/calculate_carton.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api/calculate_carton.php) | `GET` | `?usd=18.5&pairs=12` | **Kalkulator CBM & Margin**. Menghitung harga per karton, kubikasi CBM kontainer, dan tier fee HOTS. |
| [`api/prompts.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api/prompts.php) | `GET` | `?product=AP+Max&sku=APB-016&continent=Europe` | **Prompt Generator**. Menghasilkan 4-slot prompt foto AI disesuaikan benua target. |
| [`api/exchange_rate.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api/exchange_rate.php) | `GET` | `?refresh=1` | **Live Forex Rate**. Menampilkan kurs aktif USD/IDR dari feed Google Finance. |
| [`api/health.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api/health.php) | `GET` | - | **Server Health Monitor**. Diagnosa status PHP, PDO driver, koneksi database, dan cache. |

---

## 4. CONTOH RESPON JSON API BARU

### 1. `GET api/photobank_sync.php`
```json
{
  "success": true,
  "photobank_dir_exists": true,
  "manifest_exists": true,
  "total_files_in_folders": 417,
  "manifest_recorded_entries": 417,
  "categories": {
    "01_Safety_Boots": { "name": "AP Safety Boots", "count": 19 },
    "02_Terra_Series": { "name": "AP Terra Series", "count": 39 },
    "03_Orca_Series": { "name": "AP Orca Series", "count": 8 },
    "04_Chef_Series": { "name": "AP Chef Series", "count": 16 },
    "05_Medic_Series": { "name": "AP Medic Series", "count": 4 },
    "06_Biker_Casual": { "name": "AP Biker & Casual", "count": 20 },
    "07_Classic_Boots": { "name": "AP Classic Boots", "count": 23 },
    "08_Kids_Boots": { "name": "AP Kids Boots", "count": 6 },
    "09_Sandals_Clogs": { "name": "AP Sandals & Clogs", "count": 13 },
    "10_Kasual_Sneakers": { "name": "AP Kasual Sneakers", "count": 6 },
    "11_General_Lifestyle_Boots": { "name": "General & Lifestyle", "count": 263 }
  },
  "target_url": "https://admin.hotstrading.com/photo-bank",
  "last_sync_timestamp": "2026-10-21 16:21:05"
}
```

### 2. `GET api/flow_jobs.php?sku=APB-016&limit=1`
```json
{
  "success": true,
  "total_jobs_in_catalog": 424,
  "total_products": 106,
  "returned_count": 1,
  "filter_sku": "APB-016",
  "jobs": [
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
      "flow_payload": {
        "prompt": "Using the attached reference photos, create a professional e-commerce commercial studio product photograph...",
        "type": "image",
        "aspect": "1:1",
        "resolution": "1080p",
        "reference_images": ["https://p16-images-comn-sg.tokopedia-static.net/.../ref.jpeg"],
        "max_credits": 0
      },
      "status": "ready"
    }
  ]
}
```

---

## 5. CARA MENJALANKAN & MENGUJI DI KOMPUTER LOKAL

### Langkah 1: Jalankan Web Dashboard Lokal
Cukup klik dua kali file launcher:
👉 [`HotsAdmin_Module/run_debug_server.bat`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/run_debug_server.bat)

*Script otomatis mendeteksi instalasi PHP lokal (`C:\php-8.5.1-nts-Win32-vs17-x64\php.exe`) dan membuka `http://localhost:8000` di browser Anda.*

### Langkah 2: Buka Tab "Sync Flow & Photobank Hub"
1. Klik tab **"🔄 Sync Flow & Photobank Hub"** pada menu atas.
2. Anda akan melihat ringkasan 424 jobs AI foto dan 417 file WebP yang telah tersortir di 11 folder kategori.
3. Masukkan kode SKU (contoh: `APB-016` atau `APB-001`) pada kolom pencarian untuk melihat payload JSON real-time.
4. Klik **"Salin JSON"** untuk menggunakannya pada Flow MCP atau sistem lain.

### Langkah 3: Sinkronisasi Ulang Gambar
Jika ada penambahan gambar baru dari Product Input, cukup jalankan:
```cmd
python run_flow_photobank.py --push-existing "Image Flow"
```
Lalu di web dashboard HOTS Admin, klik tombol **"🔄 Refresh Status"** untuk melihat angka file bertambah secara instan.
