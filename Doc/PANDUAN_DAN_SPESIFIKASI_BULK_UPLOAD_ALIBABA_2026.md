# 📘 PANDUAN LENGKAP & SPESIFIKASI BULK UPLOAD ALIBABA 2026 (57 KOLOM)
**PT Indo Sukses Semesta — Official Gold Supplier Exporter (AP Boots)**

> **Status:** Standard Master Template 2026 (Verified & Successfully Uploaded to Alibaba)  
> **Referensi File Sukses:** `id29233741662kjoc_368505_success.xlsx` (84 Produk Berhasil Memperoleh Alibaba Product ID)  
> **Database Lokal:** `alibaba_master.db` (SQLite)  
> **Aplikasi Local Web UI:** `alibaba_manager_app.py` / `start_alibaba_manager.bat`  

---

## 📑 Daftar Isi
1. [Ringkasan Eksekutif & Bukti Keberhasilan Upload](#1-ringkasan-eksekutif--bukti-keberhasilan-upload)
2. [Spesifikasi Teknis 57 Kolom Alibaba (Master Schema)](#2-spesifikasi-teknis-57-kolom-alibaba-master-schema)
3. [Standar URL CDN & Aturan Anti-Duplikasi Gambar](#3-standar-url-cdn--aturan-anti-duplikasi-gambar)
4. [Formula Optimasi Judul B2B, Keywords, dan Deskripsi HTML V6](#4-formula-optimasi-judul-b2b-keywords-dan-deskripsi-html-v6)
5. [Panduan Penggunaan Aplikasi Python & Web UI Lokal](#5-panduan-penggunaan-aplikasi-python--web-ui-lokal)
6. [Struktur Basis Data Lokal SQLite (`alibaba_master.db`)](#6-struktur-basis-data-lokal-sqlite-alibaba_masterdb)

---

## 🏆 1. Ringkasan Eksekutif & Bukti Keberhasilan Upload

Sistem bulk upload ini mengacu langsung pada format resmi **Alibaba Default Template (57 Kolom)**. Keberhasilan skema data ini telah terbukti secara faktual melalui laporan upload resmi dari Alibaba Supplier Center:
- **File Laporan:** `id29233741662kjoc_368505_success.xlsx`
- **Total Listing Sukses Terbit:** **84 SKU Produk** (memperoleh nomor unik *Alibaba Product ID* seperti `10000049124422`, `10000049124423`, dst.).
- **Kategori Terdaftar:** `Safety Shoes`, `Rain Boots`, `Other Shoes`, `Slides Slippers`.

Semua produk yang telah diverifikasi oleh Alibaba kini telah disinkronkan dan ditandai statusnya secara otomatis pada database lokal `alibaba_master.db`.

---

## 📋 2. Spesifikasi Teknis 57 Kolom Alibaba (Master Schema)

Berikut adalah daftar lengkap 57 kolom resmi Alibaba, tipe data, dan aturan pengisiannya:

| No | Nama Kolom Excel | Status | Format / Tipe Data | Contoh Nilai Standar | Keterangan & Batasan |
|---|---|---|---|---|---|
| **1 (A)** | `* Product title` | **Wajib** | Teks (Maks 128 char) | `AP Boots Terra Eco 3 Heavy Duty Waterproof PVC Safety Work Rain Boots` | Rumus: [Brand] + [Model] + [USP] + [Material] + [Aplikasi]. Hindari karakter `!`, `@`, `#`. |
| **2 (B)** | `* Product image 1` | **Wajib** | URL CDN Gambar | `https://p16-images-comn-sg.tokopedia-static.net/...` | Foto utama resolusi 1600x1600 px latar putih bersih (*white pad*). |
| **3 (C)** | `Product image 2` | Opsional | URL CDN Gambar | `https://p19-images-comn-sg.tokopedia-static.net/...` | Foto galeri sudut 1 (Wajib unik, tidak boleh sama dengan Image 1). |
| **4 (D)** | `Product image 3` | Opsional | URL CDN Gambar | `https://p16-images-comn-sg.tokopedia-static.net/...` | Foto galeri sudut 2 (Outsole tread / sol bawah). |
| **5 (E)** | `Product image 4` | Opsional | URL CDN Gambar | `https://p16-images-comn-sg.tokopedia-static.net/...` | Foto galeri sudut 3 (Detail fleksibilitas / logo). |
| **6 (F)** | `Product image 5` | Opsional | URL CDN Gambar | `https://p16-images-comn-sg.tokopedia-static.net/...` | Foto galeri sudut 4 (Kemasan / box). |
| **7 (G)** | `Product image 6` | Opsional | URL CDN Gambar | `https://p16-images-comn-sg.tokopedia-static.net/...` | Foto galeri sudut 5. |
| **8 (H)** | `Product description` | **Wajib** | HTML String | `<div style="font-family: Arial...">...</div>` | Format responsif standar Alibaba Description Builder V6. Maksimal 20.000 karakter. |
| **9 (I)** | `Place of origin` | Standar | Teks | `Indonesia` | Negara produsen. |
| **10 (J)**| `Brand name` | Standar | Teks | `AP Boots` | Merek dagang resmi terdaftar. |
| **11 (K)**| `Category` | **Wajib** | Taxonomy Path | `Shoes & Accessories > Men's Shoes > Boots` | Kategori taksonomi resmi Alibaba. |
| **12-13** | `Attribute 1 (Name & Value)` | Standar | Pasangan Teks | `Outsole Material` : `PVC / Rubber` | Material sol luar anti-slip. |
| **14-15** | `Attribute 2 (Name & Value)` | Standar | Pasangan Teks | `Upper Material` : `PVC` | Material bodi sepatu boot. |
| **16-17** | `Attribute 3 (Name & Value)` | Standar | Pasangan Teks | `Season` : `All Seasons` | Musim pemakaian. |
| **18-19** | `Attribute 4 (Name & Value)` | Standar | Pasangan Teks | `Feature` : `100% Waterproof, Anti-Slip` | Fitur utama keunggulan produk. |
| **20-21** | `Attribute 5 (Name & Value)` | Standar | Pasangan Teks | `Gender` : `Men / Unisex` | Target gender pengguna. |
| **22 (V)**| `Sell product by` | **Wajib** | Enum | `piece` | Pilihan: `piece` atau `batch`. |
| **23 (W)**| `Batch quantity` | Kosong | Integer | `None` | Hanya diisi jika sell by = `batch`. |
| **24 (X)**| `Unit` | **Wajib** | Enum | `Pair/Pairs` | Satuan unit barang. |
| **25 (Y)**| `Currency` | **Wajib** | Kode Mata Uang | `USD` | Mata uang transaksi ekspor. |
| **26 (Z)**| `Pricing type` | **Wajib** | Enum | `Tiered pricing` | Harga bertingkat sesuai volume order. |
| **27 (AA)**| `Inventory` | **Wajib** | Integer | `5000` | Kapasitas stok siap kirim. |
| **28 (AB)**| `SPU ID (Model number)` | **Wajib** | Alfanumerik | `APB-001` | Nomor model barang. |
| **29 (AC)**| `SKU code` | **Wajib** | Alfanumerik Unik | `APB-001` | Kode unik SKU per produk. |
| **30 (AD)**| `SKU pricing` | **Wajib** | Desimal (USD) | `5.50` | Harga dasar ekspor per pasang. |
| **31-32** | `SKU Attribute 1` | Standar | Pasangan Teks | `Color` : `Black; Green; White; Yellow` | Varian warna yang tersedia. |
| **33-34** | `SKU Attribute 2` | Standar | Pasangan Teks | `Size` : `EU 38-44` | Rentang ukuran standar internasional. |
| **35-38** | `SKU Attribute 3 & 4` | Kosong | Pasangan Teks | `None` | Dikosongkan jika atribut < 3. |
| **39-40** | `Tiered Pricing 1 & MOQ 1`| Standar | Desimal & Int | `$5.50` & `100` | Harga Tier 1 pada order minimum 100 pasang. |
| **41-42** | `Tiered Pricing 2 & MOQ 2`| Standar | Desimal & Int | `$5.23` & `500` | Diskon 5% untuk order ≥ 500 pasang. |
| **43-44** | `Tiered Pricing 3 & MOQ 3`| Standar | Desimal & Int | `$4.95` & `1000` | Diskon 10% untuk order ≥ 1.000 pasang. |
| **45-46** | `Range Pricing (Low - High)`| Standar | Desimal (USD) | `$4.68` - `$5.50` | Rentang harga terendah s/d tertinggi. |
| **47 (AU)**| `* Gross weight (KG)` | **Wajib** | Desimal | `1.70` | Bobot kotor satuan (diambil dari data riil Tokopedia). |
| **48 (AV)**| `* Shipping template name`| **Wajib** | Teks | `Default Shipping Template` | Nama template ongkir di akun Alibaba. |
| **49-50** | `Shipping Qty 1 & Lead Time 1` | **Wajib** | Integer & Hari | `100` pairs & `7` days | Estimasi waktu pengiriman tier 1. |
| **51-52** | `Shipping Qty 2 & Lead Time 2` | Standar | Integer & Hari | `500` pairs & `14` days | Estimasi waktu pengiriman tier 2. |
| **53-54** | `Shipping Qty 3 & Lead Time 3` | Standar | Integer & Hari | `1000` pairs & `30` days | Estimasi waktu pengiriman pesanan partai besar. |
| **55-57** | `Product size (L, W, H)` | Standar | Desimal (cm) | `60.0`, `42.0`, `38.0` | Dimensi karton master kemasan ekspor. |

---

## 🖼️ 3. Standar URL CDN & Aturan Anti-Duplikasi Gambar

### 3.1 Aturan Anti-Duplikasi
- **Masalah Sebelumnya:** Pada pengujian awal, terdapat produk yang mengisi kolom `image_1` dan `image_2` dengan URL yang sama persis, sehingga ditolak atau mendapat penalti skor PIS dari Alibaba.
- **Solusi Sistem Baru:** Fungsi `deduplicate_images()` menjamin bahwa setiap slot dari `image_1` hingga `image_6` hanya diisi oleh **URL foto yang berbeda**. Jika sebuah produk hanya memiliki 2 foto unik, maka slot 3-6 dibiarkan kosong (`""`) dan tidak menduplikasi foto sebelumnya.

### 3.2 Pemetaan Domain CDN Publik Permanen
Untuk menghindari error `403 Forbidden` akibat kedaluwarsa tanda tangan URL Tokopedia (`x-expires`), seluruh link otomatis dialihkan ke CDN publik:
1. **Untuk Gambar `tos-alisg-...`**:
   `https://p16-images-comn-sg.tokopedia-static.net/tos-alisg-i-aphluv4xwc-sg/...`
2. **Untuk Gambar `tos-maliva-...`**:
   `https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/...`
3. **Fallback Cadangan**:
   Menggunakan CDN gambar Shopee `https://down-id.img.susercontent.com/file/...` yang terbukti 100% bebas kadaluwarsa.

---

## 🎯 4. Formula Optimasi Judul B2B, Keywords, dan Deskripsi HTML V6

### 4.1 Formula Judul B2B (SEO Title Optimizer)
Judul produk Alibaba dibatasi maksimal **128 karakter**. Formula baku yang menghasilkan Product Information Score (PIS) tertinggi adalah:

$$\text{Formula Judul} = \text{[Merek AP Boots]} + \text{[Nama Seri]} + \text{[Target Kegunaan]} + \text{[Material Utama]} + \text{[Sektor Industri]}$$

*Contoh Penerapan:*
- `AP Boots Terra Eco 3 Heavy Duty Waterproof PVC Safety Work Rain Boots for Agriculture & Construction` (101 karakter)
- `AP Boots Orca Industrial Waterproof High Rubber Rain Boots Anti-Slip Safety Footwear` (86 karakter)
- `AP Boots AP Chef Oil Resistant Slip-On Kitchen Work Shoes Waterproof Anti-Fatigue` (82 karakter)

### 4.2 Formula Top 3 Keywords Alibaba
Alibaba B2B merekomendasikan 3 frasa kata kunci terpenting per listing:
1. **Keyword 1 (Broad):** `waterproof pvc rain boots` / `industrial rain boots`
2. **Keyword 2 (Specific):** `agriculture safety boots` / `slip resistant chef shoes`
3. **Keyword 3 (Long-tail / Origin):** `heavy duty work shoes` / `made in indonesia footwear`

### 4.3 Arsitektur Deskripsi HTML V6 Responsif
Deskripsi produk dibangun dengan format modular yang kompatibel dengan **Alibaba Description Builder V6**:
1. **Header Banner:** Banner biru gradien dengan identitas resmi pabrik eksportir Indonesia dan standar SNI.
2. **Product Highlights (USP):** 5 poin keunggulan (100% Seamless Waterproof, Sol Anti-Slip, Fleksibilitas Tinggi, Tahan Bahan Kimia Ringan, Layanan OEM/ODM).
3. **Tabel Spesifikasi Teknis:** Menyajikan data material, bobot satuan kg riil dari Tokopedia, tinggi shaft (cm), dan panjang tapak (cm).
4. **Tabel Konversi Ukuran Presisi (Size Chart Matrix):** Konversi ukuran EUR 38 s/d 44 beserta ukuran milimeter/centimeter.
5. **Matriks Sektor Industri:** 4 kartu visual untuk Pertanian/Sawit, Konstruksi, Perikanan/Dapur, dan Pemakaian Harian.
6. **Informasi Ekspor & Logistik:** Ketentuan kemasan polybag + karton master, Port of Loading Tanjung Priok Jakarta, serta lead time produksi.

---

## 💻 5. Panduan Penggunaan Aplikasi Python & Web UI Lokal

Aplikasi manajemen listing lokal telah disediakan untuk memudahkan peninjauan (*preview*), penyuntingan (*edit*), dan ekspor data sekali klik.

### Cara Menjalankan Aplikasi:

#### Cara 1: Menggunakan File Batch (Paling Praktis)
Cukup **klik dua kali** pada file:
👉 **`d:\Work\Hots\Product Input\start_alibaba_manager.bat`**

File batch ini akan otomatis:
1. Memeriksa ketersediaan Python.
2. Membuka browser default Anda langsung ke alamat `http://localhost:8080`.
3. Menjalankan server aplikasi di latar belakang.

#### Cara 2: Melalui Terminal / Command Prompt
Buka terminal di folder proyek dan jalankan perintah:
```bash
python alibaba_manager_app.py
```
Lalu buka browser Anda di: `http://localhost:8080`

---

### Fitur-Fitur Utama di Web UI:
1. **Katalog Produk & Bilah Pencarian:** Cari produk berdasarkan SKU, nama seri, atau kata kunci. Terdapat filter khusus untuk produk yang sudah live di Alibaba.
2. **Tombol "👁️ Preview":**
   - Menampilkan simulasi kartu produk calon pembeli Alibaba.
   - Menampilkan *live render* deskripsi HTML Builder V6 yang interaktif.
3. **Tombol "✏️ Edit":**
   - Membuka form penyuntingan harga USD, bobot satuan kg, MOQ, ukuran, dan warna.
   - **Fitur "✨ Optimize Title":** Mengubah judul produk secara otomatis mengikuti standar SEO B2B <128 karakter.
   - **Fitur "✨ Generate Keywords":** Mengisi rekomendasi 3 keyword terbaik Alibaba.
   - **Fitur "✨ Re-Generate B2B Description":** Menyusun ulang kode HTML deskripsi secara instan.
   - **Tombol "💾 Simpan Perubahan":** Menyimpan seluruh perubahan secara permanen ke database SQLite `alibaba_master.db`.
4. **Tombol "⚡ Export Alibaba Excel":**
   - Terletak di pojok kanan atas navbar.
   - Sekali klik, sistem akan mengekspor seluruh 106 produk terupdate dari database ke template resmi 57 kolom `Alibaba_Bulk_Upload_Tokopedia_Master_2026.xlsx`.

---

## 🗄️ 6. Struktur Basis Data Lokal SQLite (`alibaba_master.db`)

Tabel `products` di dalam `alibaba_master.db` memuat seluruh 57 kolom template Alibaba ditambah kolom optimasi:
- `id`: Primary key integer auto-increment.
- `sku`: Kode SKU unik (contoh: `APB-001` s/d `APB-106`).
- `alibaba_product_id`: ID produk dari laporan keberhasilan Alibaba (misal: `10000049124422`).
- `product_title`: Judul produk teroptimasi SEO.
- `keywords`: Kata kunci pencarian B2B Alibaba.
- `image_1` s/d `image_6`: URL gambar CDN publik tanpa duplikasi.
- `description_html`: Konten HTML lengkap deskripsi produk.
- `price_usd`, `tier1_price`, `tier2_price`, `tier3_price`, `tier4_price`: Struktur harga ekspor USD.
- `gross_weight_kg`: Berat satuan logistik.
- `status`: Status produk (`Live on Alibaba` atau `Ready for Upload`).

---
*Dokumen ini merupakan standar acuan baku operasional listing ekspor Alibaba untuk PT Indo Sukses Semesta.*
