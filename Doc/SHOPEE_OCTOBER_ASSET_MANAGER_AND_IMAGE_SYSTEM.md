# 🟧 PANDUAN LENGKAP SISTEM SHOPEE ASSET STUDIO & MANAJEMEN GAMBAR PRODUK ALIBABA B2B (OKTOBER 2026)

**Versi Dokumen:** 2.0.0 (Oktober 2026 Master Standard)  
**Entitas Produsen Resmi (Legal Manufacturer):** **PT Waru Gunung** (Surabaya, Jawa Timur, Indonesia)  
**Entitas Mitra Ekspor (Seller of Record):** **PT Indo Sukses Semesta** (HOTS Trading)  
**Standar Kepatuhan Internasional:** **EU General Product Safety Regulation (GPSR EU 2023/988)** & **PT Waru Gunung Anti-Overclaim Policy**  
**Repository Git Resmi:** [https://github.com/aufapai/alibaba-bulk-hotstrading.git](https://github.com/aufapai/alibaba-bulk-hotstrading.git)

---

## 1. Ikhtisar Sistem & Navigasi Default Web GUI

Sistem **Shopee Official Asset Studio** diintegrasikan langsung sebagai **tab navigasi utama (default tab)** pada antarmuka web manager (`http://localhost:8888`), yang dijalankan melalui script peluncur `start_alibaba_manager.bat`.

### Fitur Utama Tab "Shopee Official Asset Studio":
1. **Navigasi Default Otomatis:** Saat aplikasi dibuka di browser, antarmuka langsung menyajikan studio aset 123 produk Shopee resmi (104 AP Boots + 19 Petrova Boots) tanpa perlu klik filter tambahan.
2. **Arsitektur 1 Folder per Produk:** Setiap produk secara otomatis memiliki direktori independen di dalam folder induk `Shopee_Product_Assets/`.
3. **Format Naming Terstandarisasi:**
   * **Foto Utama (Hero):** `hero_<Nama_Produk_Sanitized>.webp`
   * **Foto Samping (Side View):** `side_<Nama_Produk_Sanitized>.webp` (Tampilan lateral 90° dengan latar belakang putih bersih `#FFFFFF` / RGB 255, 255, 255).
   * **Metadata JSON Alibaba:** `<Nama_Produk_Sanitized>.json`
4. **Sistem Drag & Drop / Input Foto Otomatis:**
   * Pada setiap kartu produk, terdapat area dropzone interaktif.
   * Pengguna dapat memilih opsi: **Jadikan Hero (`hero_*.webp`)** atau **Jadikan Side (`side_*.webp`)**.
   * Ketika foto di-drag & drop atau dipilih melalui tombol browse, sistem secara otomatis:
     1. Mengonversi foto ke format WEBP teroptimasi (LANCZOS resampling, quality 92).
     2. Menamai file sesuai nama folder produk (`hero_<folder>.webp` atau `side_<folder>.webp`).
     3. Menyimpannya ke folder spesifik produk tersebut di disk.
     4. Memperbarui metadata `<folder>.json`.
     5. Memperbarui preview foto pada kartu produk secara instan (real-time cache buster).
5. **Tombol "Buka Folder" Instan:** Membuka folder produk langsung di Windows Explorer dengan 1 klik.
6. **Viewer Spesifikasi JSON Alibaba:** Modal interaktif untuk memeriksa dan menyalin JSON B2B spesifikasi fungsi produk untuk integrasi sistem Alibaba.

---

## 2. Struktur Folder & Skema Penamaan File (1 Produk = 1 Folder)

Folder induk aset tersimpan pada:
```
d:\Work\Hots\Product Input\Shopee_Product_Assets\
```

Contoh struktur internal pada tiap produk:
```
Shopee_Product_Assets/
├── AP_Boots_XTR_Hitam_Sepatu_Boot_PVC/
│   ├── hero_AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.webp      <-- Foto Utama (3/4 Front-Quarter View)
│   ├── side_AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.webp      <-- Foto Profil Samping (White Background #FFFFFF)
│   └── AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.json           <-- Metadata Spesifikasi Teknis & B2B Alibaba
├── AP_Boots_AP_Chef_Hitam_Sepatu_Slip_On_Dapur/
│   ├── hero_AP_Boots_AP_Chef_Hitam_Sepatu_Slip_On_Dapur.webp
│   ├── side_AP_Boots_AP_Chef_Hitam_Sepatu_Slip_On_Dapur.webp
│   └── AP_Boots_AP_Chef_Hitam_Sepatu_Slip_On_Dapur.json
├── Sepatu_Boots_Tinggi_Safety_Petrova_STRENGTH_kuning_Steel_Toe_PVC/
│   ├── hero_Sepatu_Boots_Tinggi_Safety_Petrova_STRENGTH_kuning_Steel_Toe_PVC.webp
│   ├── side_Sepatu_Boots_Tinggi_Safety_Petrova_STRENGTH_kuning_Steel_Toe_PVC.webp
│   └── Sepatu_Boots_Tinggi_Safety_Petrova_STRENGTH_kuning_Steel_Toe_PVC.json
└── ... (Total 123 Folder Produk)
```

### Aturan Sanitasi Penamaan (`sanitize_name`):
- Karakter terlarang pada Windows (`\ / : * ? " < > |`) dihilangkan secara aman.
- Spasi, tanda minus, dan titik diubah menjadi *underscore* tunggal (`_`).
- Karakter titik di akhir nama dihapus untuk mencegah diskrepansi sistem file Windows.

---

## 3. Spesifikasi Foto Samping Latar Belakang Putih (*Side View White BG*)

Sesuai standar listing B2B Alibaba dan katalog komersial:
* **Background Type:** Pure White `#FFFFFF` (RGB 255, 255, 255).
* **Sudut Pengambilan (Camera Angle):** Lateral Profile (Side-to-Side 90° Orthogonal View).
* **Dimensi Kanvas:** $1000 \times 1000$ piksel (aspek rasio 1:1 Square).
* **Kejelasan Visual:** Menampilkan siluet lengkap ketinggian *shaft*, lekukan *ankle collar*, kontur *vamp*, dan profil gerigi *outsole*.
* **Prioritas Sumber:**
  1. Jika ditemukan foto katalog studio lateral pada folder `Images_Produk_Katalog/` (misalnya file dengan akhiran `_02.jpg`, `_03.jpg`, atau `_04.jpg`), foto tersebut dikonversi langsung ke `.webp`.
  2. Jika tidak tersedia foto samping tersendiri, sistem membuat kanvas $1000 \times 1000$ berlatar putih bersih dengan bantalan proporsional (*aspect ratio preserving*).

---

## 4. Struktur Schema JSON Alibaba B2B (`<folder>.json`)

Setiap file JSON di dalam folder produk memiliki skema terstruktur sebagai berikut:

```json
{
  "alibaba_system_metadata": {
    "catalog_standard": "Alibaba B2B Global Trade Standard 2026",
    "platform_compliance": "GPSR EU 2023/988 & PT Waru Gunung Anti-Overclaim Matrix",
    "last_updated": "2026-10-29",
    "source_marketplace": "Shopee Official Store (Verified Reference)"
  },
  "product_identification": {
    "sku": "SHP-001",
    "product_name_shopee": "AP Boots XTR Hitam - Sepatu Boot PVC",
    "product_name_sanitized": "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC",
    "brand": "AP Boots",
    "model_series": "AP Boots XTR Hitam",
    "price_idr": "73.900",
    "sold_count": "526 terjual",
    "rating_score": "4.9"
  },
  "manufacturer_and_export_entity": {
    "legal_manufacturer": {
      "name": "PT Waru Gunung",
      "facility_location": "Karang Pilang, Mastrip, Surabaya, East Java, Indonesia",
      "jurisdiction": "Republic of Indonesia",
      "role": "OEM / Legal Footwear Manufacturer"
    },
    "export_partner_and_seller_of_record": {
      "name": "PT Indo Sukses Semesta",
      "brand_unit": "HOTS Trading",
      "port_of_loading_primary": "Tanjung Perak Seaport (ID SUB), Surabaya",
      "port_of_loading_secondary": "Tanjung Priok Seaport (ID TKG), Jakarta",
      "role": "Authorized Global Export Distributor & B2B Seller of Record"
    }
  },
  "side_to_side_white_background_specifications": {
    "background_type": "Pure White (#FFFFFF / RGB 255, 255, 255)",
    "camera_angle": "Lateral Profile (Side-to-Side 90-Degree Orthogonal View)",
    "canvas_dimensions": "1000 x 1000 pixels (1:1 Square)",
    "visual_clarity": "Clean isolated silhouette highlighting shaft height, collar curve, vamp contour, and cleated outsole profile",
    "primary_side_asset": "side_AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.webp"
  },
  "hero_image_specifications": {
    "background_type": "Clean White / Light Neutral Studio",
    "camera_angle": "3/4 Hero Perspective Front-Quarter View",
    "canvas_dimensions": "1000 x 1000 pixels (1:1 Square)",
    "primary_hero_asset": "hero_AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.webp",
    "source_shopee_cdn_url": "https://down-id.img.susercontent.com/file/..."
  },
  "technical_specifications": {
    "category_classification": "Agricultural & General Industrial Rubber Boots",
    "toe_cap_protection": "Reinforced Plain Toe",
    "upper_material": "High-Grade Virgin Polyvinyl Chloride (PVC) / EVA Polymer",
    "outsole_tread_pattern": "Heavy-Duty Cleated Lug Outsole with Deep Anti-Slip Siping Channels",
    "waterproofing_level": "Water-Resistant Injection-Molded Seamless Construction",
    "lining_material": "Quick-Drying Breathable Polyester Textile Mesh Lining",
    "size_range_available": "EU 37 - 45 (UK 4 - 11, US 5 - 12)",
    "colorways": "Standard Industrial Black / High-Visibility Yellow / Agriculture Green / Hygiene White",
    "origin_country": "Made in Indonesia"
  },
  "b2b_commercial_functions": {
    "primary_applications": "Agricultural harvesting, wet market processing, plantation drainage, construction mud protection.",
    "recommended_industries": [
      "Agricultural & Commercial Plantations (Oil Palm, Rice, Rubber)",
      "Aquaculture, Marine Processing & Commercial Wet Markets",
      "Civil Construction, Trenching & Heavy Infrastructure",
      "Food Processing Facilities, Commercial Catering & Cleanroom Utility",
      "Municipal Drainage, Disaster Relief & Heavy Monsoon Protection"
    ],
    "banned_claims_and_overclaim_removal": [
      "No unverified CE PPE II/III claims without certified lab documentation",
      "No unverified FDA medical device classification (AP Medic re-positioned to Workplace Hygiene Clogs)",
      "No unverified motorcycle crash PPE claims (Allbike re-positioned to Water-Resistant Shoe Covers)"
    ]
  },
  "packaging_and_logistics": {
    "packaging_type": "Export Grade 5-Ply Corrugated Master Carton",
    "pairs_per_carton": 12,
    "estimated_carton_weight_kg": 18.5,
    "container_loadability_20ft": "Approx. 3,600 - 4,200 pairs",
    "container_loadability_40ft_hq": "Approx. 8,500 - 9,600 pairs",
    "minimum_order_quantity_moq": "500 pairs (negotiable for trial orders)"
  },
  "local_assets_inventory": {
    "folder_relative_path": "Shopee_Product_Assets/AP_Boots_XTR_Hitam_Sepatu_Boot_PVC",
    "hero_image": "hero_AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.webp",
    "side_image": "side_AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.webp",
    "json_metadata": "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.json"
  }
}
```

---

## 5. API Endpoints Studio Aset (`App/alibaba_manager_app.py`)

Aplikasi web menyediakan endpoint REST API untuk manajemen aset produk:

| Method | Endpoint | Deskripsi |
|---|---|---|
| `GET` | `/shopee-assets/{folder}/{filename}` | Menyajikan file gambar `.webp` atau `.json` lokal secara langsung ke browser. |
| `GET` | `/api/shopee/products` | Mengembalikan daftar 123 produk beserta status eksistensi folder, hero, side, dan JSON. |
| `GET` | `/api/shopee/product-json?folder={folder}` | Membaca dan menampilkan isi file JSON spesifikasi B2B produk. |
| `GET` | `/api/shopee/open-folder?folder={folder}` | Membuka folder spesifik produk di Windows Explorer. |
| `POST` | `/api/shopee/upload-image` | Menerima data base64 gambar yang di-upload pengguna, mengonversi ke `.webp`, dan menyimpannya sebagai `hero_*.webp` atau `side_*.webp`. |
| `POST` | `/api/shopee/sync-batch` | Mengunduh ulang / memproses sinkronisasi massal seluruh 123 folder produk. |
| `POST` | `/api/shopee/download-one` | Mengunduh ulang aset untuk satu produk tertentu. |

---

## 6. Sinkronisasi Git & Pengunggahan ke GitHub

Repositori Git telah dikonfigurasikan untuk menyinkronkan seluruh kode aplikasi, template web, dokumentasi kepatuhan GPSR, katalog acuan, dan modul engine ke:
**`https://github.com/aufapai/alibaba-bulk-hotstrading.git`**

### Panduan Sinkronisasi Git Manual:
```bash
# Memeriksa status file
git status

# Menambahkan file yang telah diperbarui
git add App/ Doc/ Input/ start_alibaba_manager.bat

# Melakukan commit
git commit -m "feat(shopee-studio): implement Shopee Asset Studio default tab, 1-folder-per-product WEBP downloader, and B2B JSON generator"

# Melakukan push ke GitHub
git push origin master
```

