# 🚀 ALIBABA LISTING GENERATOR — Master Prompt & Workflow v1.0

> **Dibuat untuk:** PT Indo Sukses Semesta — HOTs Trading
> **Target Platform:** Alibaba Gold Supplier
> **Kompatibel dengan:** ChatGPT, Gemini, Claude, Ollama/OpenWebUI (Local LLM)
> **Tujuan:** Memaksimalkan **Product Information Score (PIS)** Alibaba secara konsisten & terstruktur

---

## Daftar Isi

- [Konsep Dasar](#konsep-dasar)
- [Master Prompt v1.0](#master-prompt-v10)
- [Pipeline Workflow](#pipeline-workflow)
- [Struktur Database](#struktur-database)
- [Rencana Pengembangan Sistem](#rencana-pengembangan-sistem)
- [Catatan Implementasi & Koreksi](#catatan-implementasi--koreksi)
- [Roadmap](#roadmap-pengembangan)

---

## Konsep Dasar

Pendekatan ini **bukan sekadar prompt biasa**. Tujuannya adalah membangun sebuah **Master Prompt + Workflow** yang bisa digunakan lintas platform AI — sehingga cukup ganti data produk, dan hasilnya konsisten & otomatis.

AI dipaksa berperan sebagai **4 entitas sekaligus**:

| Peran | Fungsi |
|---|---|
| Product Researcher | Menggali & memverifikasi spesifikasi dari sumber resmi |
| SEO Copywriter | Menghasilkan keyword, title, dan deskripsi yang ranking-friendly |
| HTML Generator | Menulis HTML yang kompatibel dengan Alibaba Description Builder V6 |
| Fact Checker | Menandai data yang belum terverifikasi — bukan mengarang |

---

## Master Prompt v1.0

Salin prompt berikut, isi bagian `[INPUT DATA PRODUK]`, lalu jalankan di AI model pilihan.

```text
# ROLE

You are a Senior B2B Product Researcher, SEO Specialist, Alibaba Listing Expert,
Export Copywriter, and HTML Generator specializing in Alibaba Gold Supplier listings.

Your objective is to create a complete, professional, SEO-optimized Alibaba product listing that:
- Maximizes Product Information Score (PIS)
- Improves search ranking on Alibaba
- Increases buyer conversion rate
- Follows Alibaba Description Builder V6 HTML compatibility

The final result must look and feel like a premium Alibaba Gold Supplier listing.

==================================================
# INPUT DATA PRODUK
==================================================

[ISI DI SINI — Contoh:]

Brand        : AP Boots
SKU          : APB-TG-14-BLK-43
Model        : Terra GP
Color        : Black
Size Range   : EU 37-46
Material     : Natural Rubber
Certification: SNI (Standar Nasional Indonesia)
Origin       : Indonesia
MOQ          : 12 Pairs / Model
OEM          : Available
Application  : Agriculture, Construction, Outdoor, Mining, Hiking

==================================================
# PRIMARY OBJECTIVE
==================================================

Generate a COMPLETE Alibaba Product Listing using ONLY verified information.

Every specification, feature, and claim MUST be based on factual sources.
NEVER invent specifications.

If information is unavailable, write:
    "Not Publicly Available"
instead of guessing.

==================================================
# DATA COLLECTION
==================================================

Before writing anything, research and validate the product using multiple trusted sources.
Cross-check every important specification.

Priority sources (in order):
1.  Official Brand Website
2.  Manufacturer Website
3.  Alibaba.com
4.  Global Sources
5.  Made-in-China.com
6.  Amazon
7.  Shopee / Tokopedia / Lazada
8.  Distributor Catalog
9.  Product PDF / Datasheet
10. Government Certification Database
11. Product Manual
12. Technical Datasheet

RULE: Only use information confirmed by at least TWO sources.

If conflicting information exists:
Always choose the MANUFACTURER'S official specification.

==================================================
# SEO REQUIREMENTS
==================================================

Step 1: Generate keyword research BEFORE writing any content.

Output format:
- Primary Keyword       : [1 keyword]
- Secondary Keywords    : [5-8 keywords]
- Long Tail Keywords    : [5-8 phrases]
- Buyer Intent Keywords : [e.g. "buy", "wholesale", "bulk order", "supplier"]
- Commercial Keywords   : [e.g. "OEM", "private label", "custom logo"]
- Export Keywords       : [e.g. "Indonesia manufacturer", "FOB Jakarta"]
- Wholesale Keywords    : [e.g. "distributor", "bulk", "low MOQ"]

Rules:
- Natural keyword density (do NOT keyword stuff)
- Use keywords naturally in title, first 100 words, headers, and spec table

==================================================
# PRODUCT TITLE
==================================================

Generate 5 SEO-optimized title candidates.
Then select the BEST ONE.

Rules:
- Maximum 128 characters
- Include: Brand + Model + Key Feature + Material + Application
- Alibaba SEO-friendly format

==================================================
# PRODUCT DESCRIPTION
==================================================

Target audience:
- Importers & Distributors
- Wholesalers & Retail Chains
- OEM Buyers
- Government Procurement
- Industrial sectors: Mining, Construction, Agriculture, Healthcare, Food Service

Tone: Professional | Premium | Technical | Commercial

Structure:
1. Opening hook (2-3 sentences, include primary keyword)
2. Product story (why this product exists, problem it solves)
3. Key features (bullet points)
4. Target industries
5. Why choose this brand

==================================================
# PRODUCT ADVANTAGES (USP)
==================================================

Generate 5-8 unique selling propositions.
Explain WHY buyers should choose this product over competitors.

Rules:
- No generic AI filler text (e.g. "high quality", "best product")
- Each USP must be specific, verifiable, and buyer-focused
- Connect to material, certification, performance, or price advantage

==================================================
# TECHNICAL SPECIFICATION TABLE
==================================================

Generate a specification table using ONLY verified data.

Required fields:
- Product Name
- Brand
- Model Number
- Material (Outsole / Upper / Lining)
- Construction Method
- Available Colors
- Size Range (EU)
- Weight per Pair (approx.)
- Certification
- Country of Origin
- Primary Application
- Export Packaging
- MOQ
- OEM Available
- ODM Available
- Private Label
- HS Code (if available)
- Shelf Life (if applicable)

Mark unverified fields as: [Needs Verification]

==================================================
# APPLICATIONS
==================================================

List all suitable industries and use cases.
Explain HOW and WHY this product is suitable for each.

Minimum 6 industries.

==================================================
# OEM & CUSTOMIZATION SERVICES
==================================================

Explain available customization options:
- OEM (Original Equipment Manufacturer)
- ODM (Original Design Manufacturer)
- Private Label / White Label
- Logo Printing (emboss / print / embroidery)
- Packaging Customization
- Color Customization
- Size Customization

Include minimum order quantity for each service.

==================================================
# PACKAGING & SHIPPING INFORMATION
==================================================

Generate complete export packaging information:

Inner Packaging  : [e.g. polybag per pair]
Outer Carton     : [e.g. 12 pairs per master carton]
Carton Size (cm) : L x W x H
Gross Weight     : [kg]
Net Weight       : [kg]
CBM per carton   : [m3]
20GP capacity    : [pairs approx.]
40GP capacity    : [pairs approx.]
40HQ capacity    : [pairs approx.]

Mark unknowns as: [Needs Verification]

==================================================
# FAQ (Frequently Asked Questions)
==================================================

Generate 15-20 realistic buyer FAQs.

Mix of:
- Technical questions (material, size, weight)
- Commercial questions (MOQ, price, OEM)
- Shipping questions (lead time, port, Incoterms)
- Quality questions (certifications, testing)
- Customization questions

==================================================
# CALL TO ACTION
==================================================

Generate 3 professional B2B Call-to-Action variants:
1. Short CTA (1 line)
2. Standard CTA (3-4 lines)
3. Full CTA with contact info placeholder

==================================================
# HTML GENERATION RULES
==================================================

IMPORTANT: Generate HTML COMPATIBLE with Alibaba Description Builder V6.

ALLOWED HTML tags ONLY:
  table, tr, td, p, b, font, br, img

STRICTLY FORBIDDEN:
  - Flexbox / CSS Grid
  - JavaScript / jQuery
  - External CSS / Stylesheets
  - SVG / Canvas / Iframe
  - Bootstrap / React / Tailwind
  - Complex DIV layouts
  - Media queries

HTML sections to generate (in this order):
  1.  Product Highlight Banner
  2.  Product Description
  3.  Product Gallery (images)
  4.  Why Choose Us
  5.  Key Features
  6.  Technical Specification Table
  7.  Applications
  8.  OEM & Customization Services
  9.  Packaging & Shipping Info
  10. Company Profile
  11. FAQ Section
  12. Contact / CTA Section

==================================================
# IMAGE HANDLING
==================================================

DO NOT modify or generate image URLs.
Keep original image links as provided by user.

Image format:
  <img src="[ORIGINAL_URL_AS_PROVIDED]" width="100%">

If no image URL is provided, write:
  <!-- IMAGE PLACEHOLDER: [product name] [view angle] -->

==================================================
# FACT CHECK BEFORE OUTPUT
==================================================

Before generating final HTML, verify:
- All specifications match at least 2 sources
- Certification numbers are real (not invented)
- Size ranges are accurate
- Materials are correctly named
- Applications are appropriate for this product type
- GPSR & Regional Compliance Rules (PT Waru Gunung & HOTS Trading Standard):
  * Legal Manufacturer is verified: PT Waru Gunung (Surabaya, East Java, Indonesia)
  * Export Supply Partner is identified: PT Indo Sukses Semesta (HOTS Trading)
  * Prohibited Overclaims: FDA approved, CE certified, EN standard compliant, PPE certified, Medical grade, Hospital grade, Surgical, Sterile, Virus-proof, Chemical-proof, Guaranteed protection.
  * Mandatory Safety Information Box (Pre-use inspection, storage, non-medical status, hazard limits) must be present.
  * Mandatory General Use & Anti-Overclaim Disclaimer (Section 11) must be included.
  * Non-steel toe boots (like WB series, Terra, Classic) must NOT be described as safety boots or PPE.

Unverified items: mark inline as [Needs Verification]
Uncertain items : mark inline as [Verify Before Publishing]

==================================================
# OUTPUT FORMAT
==================================================

Return ONLY:
  Ready-to-copy Alibaba HTML code

Do NOT include:
  - Explanation or commentary
  - Markdown formatting
  - Notes or disclaimers
  - AI-generated text warnings

Only output: clean, ready-to-paste HTML.
```

---

## Pipeline Workflow

Workflow ini mengubah input produk mentah menjadi HTML siap-paste ke Alibaba secara bertahap:

```
+---------------------------------------------+
|           INPUT DATA PRODUK                 |
|  (SKU, Brand, Model, Material, Spec, Gambar)|
+----------------------+----------------------+
                       |
                       v
           +-----------------------+
           |    GOOGLE SEARCH      |
           |  Cari data produk di  |
           |  web resmi, katalog   |
           +----------+------------+
                      |
                      v
           +-----------------------+
           |  OFFICIAL WEBSITE     |
           |  Ambil spek resmi     |
           |  dari brand/manufaktur|
           +----------+------------+
                      |
                      v
           +-----------------------+
           |  MARKETPLACE          |
           |  CROSS-CHECK          |
           |  Alibaba, Shopee,     |
           |  Tokopedia, Amazon    |
           +----------+------------+
                      |
                      v
           +-----------------------+
           |  EXTRACT              |
           |  SPECIFICATION        |
           |  Kumpulkan semua data |
           |  yang terverifikasi   |
           +----------+------------+
                      |
                      v
           +-----------------------+
           |  NORMALIZE DATA       |
           |  Standarisasi format, |
           |  satuan, terminologi  |
           +----------+------------+
                      |
                      v
           +-----------------------+
           |  SEO KEYWORD          |
           |  GENERATOR            |
           |  Primary, Secondary,  |
           |  Long-tail, Buyer     |
           +----------+------------+
                      |
                      v
           +-----------------------+
           |  ALIBABA HTML         |
           |  GENERATOR            |
           |  Full listing HTML    |
           |  Alibaba-compatible   |
           +----------+------------+
                      |
                      v
           +-----------------------+
           |  QUALITY CHECKER      |
           |  Fact-check semua     |
           |  klaim & spesifikasi  |
           +----------+------------+
                      |
                      v
+---------------------------------------------+
|              READY HTML                     |
|      Siap copy-paste ke Alibaba             |
+---------------------------------------------+
```

---

## Struktur Database

Agar tidak mengisi data berulang untuk setiap SKU, gunakan skema database berikut.
Cukup update data produknya, generator akan menarik data secara otomatis dan menghasilkan HTML yang konsisten.

### Tabel: products

```sql
CREATE TABLE products (
  id              INT PRIMARY KEY AUTO_INCREMENT,
  sku             VARCHAR(50)  UNIQUE NOT NULL,
  brand           VARCHAR(100) NOT NULL,
  model           VARCHAR(100) NOT NULL,
  title           VARCHAR(128),           -- Final SEO-optimized title (max 128 char)
  description     TEXT,                   -- Product description (plain text draft)
  material        VARCHAR(255),           -- e.g. "Natural Rubber / PVC"
  construction    VARCHAR(100),           -- e.g. "Injection / Vulcanized / Cemented"
  color           VARCHAR(100),           -- e.g. "Black, Green, Red"
  size_range      VARCHAR(50),            -- e.g. "EU 37-46"
  weight_gram     INT,                    -- Weight per pair in grams
  application     TEXT,                   -- Comma-separated or JSON
  certification   VARCHAR(255),           -- e.g. "SNI, ISO 20345"
  origin          VARCHAR(100) DEFAULT 'Indonesia',
  moq             INT DEFAULT 12,         -- Minimum Order Quantity (pairs)
  oem_available   TINYINT(1) DEFAULT 1,
  odm_available   TINYINT(1) DEFAULT 0,
  private_label   TINYINT(1) DEFAULT 1,
  packing_unit    INT,                    -- Pairs per master carton
  carton_l_cm     DECIMAL(6,1),
  carton_w_cm     DECIMAL(6,1),
  carton_h_cm     DECIMAL(6,1),
  gross_weight_kg DECIMAL(6,2),
  net_weight_kg   DECIMAL(6,2),
  cbm             DECIMAL(8,4),           -- Volume per carton in m3
  hs_code         VARCHAR(20),            -- HS Code for customs
  category_src    VARCHAR(255),           -- Alibaba category path
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME ON UPDATE CURRENT_TIMESTAMP
);
```

### Tabel: product_images

```sql
CREATE TABLE product_images (
  id          INT PRIMARY KEY AUTO_INCREMENT,
  product_id  INT NOT NULL,
  image_order INT DEFAULT 0,       -- Urutan tampil (0 = main image)
  image_url   TEXT NOT NULL,       -- URL gambar (lokal atau CDN)
  image_type  VARCHAR(30),         -- e.g. "main", "detail", "left", "rear", "spec"
  alt_text    VARCHAR(255),
  FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Tabel: keywords

```sql
CREATE TABLE keywords (
  id                  INT PRIMARY KEY AUTO_INCREMENT,
  product_id          INT NOT NULL,
  primary_keyword     VARCHAR(100),
  secondary_keywords  TEXT,    -- JSON array atau comma-separated
  long_tail_keywords  TEXT,
  buyer_keywords      TEXT,
  commercial_keywords TEXT,
  export_keywords     TEXT,
  FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Tabel: specifications

```sql
CREATE TABLE specifications (
  id          INT PRIMARY KEY AUTO_INCREMENT,
  product_id  INT NOT NULL,
  attribute   VARCHAR(100) NOT NULL,  -- e.g. "Outsole Material"
  value       VARCHAR(255) NOT NULL,  -- e.g. "Natural Rubber"
  is_verified TINYINT(1) DEFAULT 0,   -- 1 = verified, 0 = needs verification
  FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Tabel: faq

```sql
CREATE TABLE faq (
  id         INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT,           -- NULL = global FAQ (berlaku untuk semua produk)
  question   TEXT NOT NULL,
  answer     TEXT NOT NULL,
  faq_order  INT DEFAULT 0,
  FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Tabel: listing_html

```sql
-- Menyimpan hasil HTML yang sudah di-generate (cache)
CREATE TABLE listing_html (
  id           INT PRIMARY KEY AUTO_INCREMENT,
  product_id   INT NOT NULL UNIQUE,
  html_content LONGTEXT,
  generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  is_published TINYINT(1) DEFAULT 0,
  FOREIGN KEY (product_id) REFERENCES products(id)
);
```

---

## Rencana Pengembangan Sistem

Jika dikembangkan menjadi **aplikasi internal HOTs Trading**, berikut arsitektur yang direkomendasikan:

### Stack Teknologi

| Layer | Teknologi | Alasan |
|---|---|---|
| **Backend** | PHP Native (no framework) | Sesuai stack yang sudah digunakan |
| **Database** | MariaDB / MySQL | Ringan, cepat, cocok untuk ribuan SKU |
| **Frontend** | HTML + Bootstrap 5 | Simple, tidak perlu build process |
| **AI Layer** | OpenAI API / Gemini API / Ollama | Fleksibel, bisa lokal maupun cloud |
| **Fact Check** | Google Custom Search API | Verifikasi data dari web resmi |
| **Export** | HTML file download | Ready copy-paste ke Alibaba |

### Fitur yang Direncanakan

```
[v] Input Form             -> Isi data produk via web UI (tidak perlu coding)
[v] Database Storage       -> Semua SKU tersimpan, tidak perlu isi ulang
[v] AI Generator           -> Koneksi ke OpenAI / Gemini / Claude / Ollama
[v] Fact Checking Layer    -> Auto-scrape sumber resmi, tandai data tidak valid
[v] HTML Preview           -> Preview hasil listing sebelum copy ke Alibaba
[v] Template Engine        -> Format konsisten untuk semua 80+ SKU AP Boots
[v] Batch Generator        -> Generate listing untuk banyak SKU sekaligus
[v] Export Manager         -> Download HTML per SKU atau per batch
[v] Revision History       -> Simpan versi HTML sebelumnya
[v] Image Manager          -> Kelola gambar produk per SKU
[v] Keyword Manager        -> Simpan dan reuse keyword per kategori produk
```

### User Flow Sistem

```
[ Admin Login ]
      |
      v
[ Dashboard ] --> [ Pilih SKU ] --> [ Edit Data Produk ]
                                           |
                                           v
                                 [ Klik: Generate Listing ]
                                           |
                                           v
                                 [ AI + Fact Check Layer ]
                                           |
                                           v
                                 [ Preview HTML Listing ]
                                           |
                               +-----------+-----------+
                               v                       v
                         [ Revisi ]             [ Approve ]
                               |                       |
                               +----------+------------+
                                          |
                                          v
                                [ Download / Copy HTML ]
                                          |
                                          v
                                [ Paste ke Alibaba ]
```

---

## Catatan Implementasi & Koreksi

Beberapa penyempurnaan dari konsep awal yang perlu diperhatikan:

### 1. HTML Compatibility — Koreksi Penting

Alibaba Description Builder V6 memang sangat terbatas. Tag yang **aman** digunakan:

```html
<!-- AMAN -->
<table width="100%" cellpadding="8" cellspacing="0" border="0">
<tr><td align="center">
<p><b>Teks tebal</b></p>
<font color="#333333" size="3">Teks berwarna</font>
<br>
<img src="url_gambar" width="100%" />

<!-- HINDARI -->
<div style="display:flex">     <!-- Tidak semua browser Alibaba support -->
<style>.class { ... }</style>  <!-- Sering di-strip oleh Alibaba parser -->
<script>...</script>           <!-- Diblokir total -->
```

> **Tips:** Selalu test HTML hasil generate di mode preview Alibaba sebelum publish. Beberapa tag `div` sederhana masih bisa lolos, tapi jangan andalkan CSS external.

### 2. Keyword Priority untuk Alibaba — Koreksi SEO

Untuk Alibaba (bukan Google), prioritas keyword berbeda:

| Prioritas | Jenis Keyword | Contoh untuk AP Boots |
|---|---|---|
| 1 | Product type + material | rubber boots Indonesia |
| 2 | Brand + model | AP Boots Terra GP |
| 3 | Application | agriculture safety boots |
| 4 | Certification | SNI certified rubber boots |
| 5 | Commercial | wholesale rubber boots manufacturer |

### 3. Fact Checking — Prioritas Sumber untuk AP Boots

Untuk produk AP Boots (brand lokal Indonesia), urutan sumber yang realistis:

1. **apboots.co.id** (website resmi AP Boots)
2. **Tokopedia / Shopee** (distributor resmi, lihat tab spesifikasi)
3. **bsn.go.id** (SNI database untuk verifikasi sertifikasi)
4. **PDF katalog AP Boots** (tanyakan ke distributor)
5. **Alibaba listings** yang sudah ada (hati-hati, sering tidak akurat — verifikasi ulang)

### 4. HS Code untuk Rubber Boots Indonesia

| Jenis Produk | HS Code |
|---|---|
| Rubber boots / rain boots (waterproof) | 6401.92.00 |
| Safety boots with steel toe (PVC/rubber) | 6401.10.00 |
| Footwear with rubber sole, textile upper | 6404.19.90 |
| Clogs (sandal platform) | 6402.99.90 |

> **Catatan:** Verifikasi HS Code dengan tim export / freight forwarder sebelum mencantumkan di listing.

### 5. Estimasi Kapasitas Kontainer (Rubber Boots)

| Kontainer | Estimasi Kapasitas |
|---|---|
| 20GP | 2.000 - 3.000 pairs (tergantung ukuran carton) |
| 40GP | 4.500 - 6.000 pairs |
| 40HQ | 5.500 - 7.000 pairs |

> **Catatan:** Hitung ulang berdasarkan CBM aktual karton setelah packaging final dikonfirmasi.

### 6. MOQ yang Realistis untuk AP Boots

| Jenis Order | MOQ yang Wajar |
|---|---|
| Standard order (off-the-shelf) | 12 pairs / model / warna |
| Mixed container order | 50 pairs minimum total |
| OEM / Private Label | 300 - 500 pairs per design |
| ODM (custom mold) | 1.000+ pairs |

---

## File Terkait

| File | Keterangan |
|---|---|
| [KATALOG_PRODUK_AP_BOOTS_2026.md](./KATALOG_PRODUK_AP_BOOTS_2026.md) | Katalog lengkap 76 SKU AP Boots dengan foto rata tengah |
| [Output/alibaba_2026_products.csv](./Output/alibaba_2026_products.csv) | Data produk terstruktur (76 SKU aktif) |
| [Output/alibaba_all_products_v2.csv](./Output/alibaba_all_products_v2.csv) | Data lengkap semua produk (158 SKU) |
| [Output/generate_catalog_md.py](./Output/generate_catalog_md.py) | Script generator katalog Markdown |
| [Output/image_auto_sorter.py](./Output/image_auto_sorter.py) | Script auto-sort gambar produk per SKU |

---

## Roadmap Pengembangan

```
Phase 1 — SEKARANG (Done)
  [x] Struktur folder gambar per SKU
  [x] Database CSV produk (76 SKU)
  [x] Katalog Markdown dengan gambar rata tengah
  [x] Master Prompt siap pakai (dokumen ini)

Phase 2 — TARGET 1-2 bulan
  [ ] Input form web (PHP + Bootstrap 5)
  [ ] Koneksi database MySQL
  [ ] Basic HTML generator (template-based, tanpa AI)
  [ ] Preview listing di browser

Phase 3 — SCALE UP 3-6 bulan
  [ ] Integrasi AI API (Gemini / OpenAI / Claude)
  [ ] Auto fact-check dari web resmi
  [ ] Batch generator (semua SKU sekaligus)
  [ ] Image CDN untuk URL gambar stabil
  [ ] Export manager (download per SKU / bulk)

Phase 4 — PRODUCTION 6+ bulan
  [ ] Alibaba API integration (jika tersedia)
  [ ] Keyword tracking & ranking monitor
  [ ] A/B testing listing variants
  [ ] Multi-language listing (EN / ZH / AR)
```

---

*Dokumen ini dibuat untuk keperluan internal PT Indo Sukses Semesta — HOTs Trading.*
*Versi: 1.0 | Dibuat: Juli 2026*
