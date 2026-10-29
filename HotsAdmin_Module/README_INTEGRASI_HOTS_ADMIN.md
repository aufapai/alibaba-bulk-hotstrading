# PANDUAN ARSITEKTUR, FOLDER & INTEGRASI HOTS ADMIN MODULE
**Modul Ekspor Alibaba B2B & Sinkronisasi Database Sistem**  
*Target Integrasi: `https://admin.hotstrading.com/` • cPanel MariaDB / MySQL • Environment Debug*  
**Versi:** 2.0 (Oktober 2026) | **Folder:** `HotsAdmin_Module/`

---

## 1. STRUKTUR FOLDER MODULAR SIAP TRANSFER KE DEBUG

Folder [`HotsAdmin_Module/`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module) telah distrukturkan secara terstandarisasi (modular package) agar siap di-transfer langsung ke server staging, cPanel hosting, maupun environment debug lokal:

```
HotsAdmin_Module/
├── index.php                      # [MASTER UI] Interactive Debug Dashboard & Live Tester
├── README_INTEGRASI_HOTS_ADMIN.md # [DOKUMENTASI] Panduan Lengkap Arsitektur & SOP Transfer
├── cpanel_export_controller.php   # [BACKWARD COMPAT] Controller wrapper kompatibel legacy
├── hots_db_adapter.py             # [BACKWARD COMPAT] Python bridge wrapper di root
├── database_schema.sql            # [BACKWARD COMPAT] Skema MySQL/MariaDB master di root
├── openapi_spec.json              # [BACKWARD COMPAT] OpenAPI 3.0 JSON specification
├── openapi_spec.yaml              # [BACKWARD COMPAT] OpenAPI 3.0 YAML Swagger
│
├── config/                        # ⚙️ KONFIGURASI SISTEM
│   ├── config.php                 # File konfigurasi aktif (DB, Forex, Packaging, Fees, CORS)
│   ├── config.sample.php          # Template sampel untuk konfigurasi cPanel live
│   └── .env.example               # Contoh environment variable untuk staging / server
│
├── src/                           # 🧠 BACKEND CORE OOP ENGINE
│   ├── AlibabaExportController.php# Controller inti ekspor Alibaba & logika bisnis
│   ├── Database.php               # Dual Driver (MySQL/MariaDB + SQLite fallback auto-diagnostic)
│   └── ForexService.php           # Layanan kurs live USD/IDR dengan caching 30 menit
│
├── api/                           # 🔌 REST API ENDPOINTS (JSON OUTPUT)
│   ├── health.php                 # GET: Status diagnosa PHP, PDO Driver, DB, & Forex
│   ├── exchange_rate.php          # GET: Kurs live real-time USD/IDR (?refresh=1)
│   ├── calculate_carton.php       # GET: Kalkulator CBM, kontainer 20ft/40ft, & fee HOTS
│   ├── prompts.php                # GET/POST: Generator 4-slot AI photo prompts
│   ├── products.php               # GET: Daftar katalog produk dari database
│   ├── smart_top_picks.php        # GET: Smart Top Pick Generator (Alibaba B2B Export Packages)
│   ├── market_intelligence.php    # GET: Intelijen Pasar 5 Benua (Q1-Q4) & 10 Accio Angles
│   ├── generate_alibaba_listing.php # GET/POST: Full Alibaba Listing Generator (V6 HTML & SEO)
│   ├── export_alibaba_bulk.php    # GET: Direct 57-Column Alibaba Bulk Upload CSV Download
│   ├── photobank_sync.php         # GET/POST: Status sinkronisasi 11 kategori folder Photobank
│   └── flow_jobs.php              # GET: Data 424 AI Photo Generation jobs dari Product Input
│
├── sql/                           # 🗄️ DATABASE MIGRATIONS & SEED DATA
│   ├── database_schema.sql        # Skema tabel alibaba_export_listings, rules, & view
│   ├── seed_market_rules.sql      # Data seed intelijen pasar 5 benua (Q1 - Q4)
│   └── sample_products_seed.sql   # Data seed produk AP Boots untuk test database kosong
│
├── scripts/                       # 🐍 SCRIPT CLI & OTOMASI TESTING
│   ├── test_module_connection.py  # Script diagnosa otomatis pra-transfer (Python)
│   └── hots_db_adapter.py         # Adaptor database SQLite <-> MySQL
│
├── docs/                          # 📖 DOKUMENTASI SPESIFIKASI API
│   ├── openapi_spec.json          # OpenAPI 3.0 JSON Contract
│   └── openapi_spec.yaml          # OpenAPI 3.0 YAML Swagger Contract
│
└── cache/                         # 💾 CACHE RUNTIME (Dibuat Otomatis)
    └── forex_cache.json           # File cache kurs valas lokal
```

---

## 2. DETAIL FUNGSI SETIAP SUB-FOLDER & KOMPONEN

| Sub-Folder / File | Fungsi & Peran Teknis | Catatan Penggunaan |
|---|---|---|
| [`index.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/index.php) | **Master Debug Dashboard GUI**. Menyediakan antarmuka web interaktif untuk kalkulasi kemasan, generator AI prompt 4-slot, preview produk, dan tester API live. | Akses via browser saat di-deploy di cPanel atau `php -S localhost:8000`. |
| [`config/`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/config) | **Sentral Pengaturan**. Menyimpan kredensial database cPanel, setting CBM kontainer (20ft = 28 CBM, 40ft HC = 68 CBM), dan tier fee HOTS (Member 2%, Mandiri 5%, Full Assistance 15%). | Edit `config.php` sesuai database cPanel target. |
| [`src/`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/src) | **Core Business Logic (OOP)**. Terdiri dari `Database.php`, `ForexService.php`, dan `AlibabaExportController.php`. Bersih tanpa dependensi library eksternal (Pure PHP 7.4 - 8.3+). | Siap dipanggil dari framework Laravel, CodeIgniter, atau PHP native. |
| [`api/`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/api) | **Endpoint REST API**. Mengembalikan format JSON terstandarisasi dengan header CORS aktif, siap dikonsumsi oleh frontend AJAX maupun sistem eksternal. | Dilengkapi endpoint `health.php` untuk memonitor status server. |
| [`sql/`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/sql) | **Migrasi & Seed Data**. Menjamin database di environment debug tidak kosong dan memiliki aturan benua Q1-Q4 serta relasi foreign key yang aman (`ON DELETE CASCADE`). | Import via phpMyAdmin cPanel atau CLI mysql. |
| [`scripts/`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/scripts) | **Automated Diagnostics**. Berisi script verifikasi integritas file, database test, dan koneksi API sebelum modul ditransfer. | Jalankan `python scripts/test_module_connection.py`. |

---

## 3. CHECKLIST PRA-TRANSFER & DEPLOY KE DEBUG / CPANEL

Saat mentransfer modul ini ke environment debug (cPanel atau server staging), ikuti checklist 4 langkah berikut:

### Langkah 1: Copy / Upload Folder ke Server
* **cPanel Live:** Upload seluruh folder `HotsAdmin_Module/` ke direktori web cPanel, misalnya:  
  `/home/username/public_html/admin/modules/HotsAdmin_Module/`  
  atau jadikan subdomain: `https://export.hotstrading.com/`
* **Local Debug Server:** Cukup masuk ke folder `HotsAdmin_Module/` dan jalankan:
  ```bash
  php -S localhost:8000
  ```
  Lalu buka `http://localhost:8000` di browser.

### Langkah 2: Setup Kredensial Database
Buka file [`config/config.php`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/config/config.php) dan sesuaikan kredensial MySQL cPanel:
```php
'db' => [
    'driver'    => 'mysql',
    'host'      => 'localhost',
    'port'      => 3306,
    'database'  => 'hotj4796_hotstrading',
    'username'  => 'hotj4796_user',
    'password'  => 'password_database_anda',
    'charset'   => 'utf8mb4'
]
```
*(Jika database MySQL belum aktif, sistem otomatis beralih ke local mock / fallback tanpa crash)*.

### Langkah 3: Import File SQL ke phpMyAdmin
Buka phpMyAdmin cPanel di database yang dituju, lalu import file secara berurutan:
1. [`sql/database_schema.sql`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/sql/database_schema.sql) -> Membuat tabel `alibaba_export_listings`, `alibaba_market_rules`, `alibaba_upload_audits`, dan view katalog.
2. [`sql/seed_market_rules.sql`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/sql/seed_market_rules.sql) -> Mengisi aturan pasar 5 benua (Eropa, Amerika, ASEAN, Timur Tengah, Oseania).
3. *(Opsional)* [`sql/sample_products_seed.sql`](file:///d:/Work/Hots/Product%20Input/HotsAdmin_Module/sql/sample_products_seed.sql) -> Jalankan jika tabel `products` di server masih kosong agar langsung ada data uji coba.

### Langkah 4: Izin Folder Cache (Write Permission)
Pastikan web server memiliki izin tulis untuk folder `cache/`:
```bash
chmod 775 cache/
```
Hal ini memastikan kurs live dari Google/Forex API tersimpan di `cache/forex_cache.json` selama 30 menit.

---

## 4. DAFTAR REST API ENDPOINTS

Endpoint berikut langsung dapat diakses setelah folder di-upload:

| Endpoint | Method | Parameter Contoh | Keterangan Respon |
|---|---|---|---|
| `/api/health.php` | `GET` | - | Status PHP, PDO Driver, Koneksi DB, Izin Cache |
| `/api/exchange_rate.php` | `GET` | `?refresh=1` | Nilai kurs live USD/IDR terkini & status cache |
| `/api/calculate_carton.php` | `GET` | `?usd=5.50&pairs=12` | Perhitungan CBM, berat, muat 20ft/40ft, fee HOTS |
| `/api/prompts.php` | `GET/POST`| `?product=AP+Max&sku=AP-MX-01&continent=Europe` | Prompt AI 4-slot terstandarisasi Alibaba |
| `/api/products.php` | `GET` | `?limit=20` | Daftar produk dari MySQL/SQLite |
| `/api/photobank_sync.php` | `GET/POST` | - | Status sinkronisasi 11 kategori folder Photobank |
| `/api/flow_jobs.php` | `GET` | `?sku=APB-016&limit=10` | 424 AI Photo Generation jobs dari Product Input |

---

## 5. CARA MENJALANKAN TEST VERIFIKASI SEBELUM TRANSFER

Jalankan script verifikasi di terminal lokal:
```bash
python "d:\Work\Hots\Product Input\HotsAdmin_Module\scripts\test_module_connection.py"
```
Jika seluruh indikator menampilkan `[OK] PASS` dan `[SUCCESS] ALL MODULE COMPONENTS ARE COMPLETE AND READY TO TRANSFER!`, maka paket modul siap ditransfer tanpa ada file yang tertinggal.
