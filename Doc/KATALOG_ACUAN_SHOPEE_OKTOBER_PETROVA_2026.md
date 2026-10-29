# 📋 KATALOG ACUAN UTAMA SHOPEE OKTOBER 2026 — PETROVA & PT WARU GUNUNG
**Dokumen Referensi:** Data Scraping Shopee Official Store Petrova (`https://shopee.co.id/petrovabootsofficial`)  
**Status Implementasi:** Aktif sebagai Acuan Lampiran Utama & Telah Tersinkronisasi ke Database Alibaba  
**File Sumber:** `Input/shopee-co-id-2026-10-petrova.csv`  
**Pabrik / Legal Manufacturer:** **PT Waru Gunung** (Surabaya, Jawa Timur, Indonesia)  
**Export Supply Partner / Seller:** **PT Indo Sukses Semesta** (HOTS Trading)  
**Standar Kepatuhan:** Mengacu penuh pada **GPSR Batch Compliance PT Waru Gunung** (Anti-Overclaim, Safe Copy, & Geo-Block Prevention).

---

## 1. Ringkasan Eksekutif Dataset Shopee Oktober

| Parameter | Keterangan / Nilai |
|---|---|
| **Sumber Scraping** | Shopee Official Store Petrova Boots (`petrovabootsofficial`) |
| **Total Baris Data** | 19 Baris (12 Model Unik Kanonikal + 7 Varian Ukuran/Warna) |
| **Rentang Harga Eceran** | Rp 77.500 — Rp 239.000 (~USD 4.84 — USD 14.94) |
| **Rating Rata-rata Toko** | 4.8 — 5.0 (Tingkat kepuasan sangat tinggi) |
| **Model Terlaris** | Petrova STRENGTH Safety Kuning (10RB+ Terjual) & Strength WB Kuning (4RB+ Terjual) |
| **Foto Produk** | Menggunakan direct CDN resmi Shopee (Image 1 s/d Image 4 per produk) |

---

## 2. Matriks Pemetaan Produk, SKU, dan Kategori Kepatuhan (GPSR)

Berikut adalah daftar 19 baris produk Shopee Oktober yang telah ditandai dan diintegrasikan ke sistem Alibaba Manager dengan penyesuaian aturan kepatuhan anti-overclaim:

| No | SKU Sistem | Nama Produk Asli Shopee | Model Bersih B2B | Kategori & Perlindungan Ujung Kaki | Terjual | Rating | Harga (IDR) | Harga B2B (USD) | Status Kepatuhan GPSR |
|:---:|:---:|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 1 | `PTR-001` | Sepatu Boots Tinggi Safety Petrova STRENGTH kuning-Steel Toe PVC. | Petrova STRENGTH Yellow | **Steel Toe Safety Boots** (Impact Toe) | 10RB+ | 4.9 | Rp 161.000 | \$10.06 | Lolos (Factory Steel Toe Standard) |
| 2 | `PTR-002` | Petrova - Sepatu Boots Strength WB Hitam - Boots Air PVC | Petrova Strength WB Black | **Waterproof PVC Work Boots** (Plain Toe / Utility) | 3RB+ | 4.8 | Rp 77.500 | \$4.84 | Lolos (Non-PPE / General Utility) |
| 3 | `PTR-003` | Petrova - Sepatu Boots Strength WB Kuning - Boots Air PVC | Petrova Strength WB Yellow | **Waterproof PVC Work Boots** (Plain Toe / Utility) | 4RB+ | 4.8 | Rp 95.000 | \$5.94 | Lolos (Non-PPE / General Utility) |
| 4 | `PTR-004` | Petrova - Sepatu Boots Strength WB Biru - Boots Air PVC | Petrova Strength WB Blue | **Waterproof PVC Work Boots** (Plain Toe / Utility) | 1RB+ | 4.8 | Rp 110.000 | \$6.88 | Lolos (Non-PPE / General Utility) |
| 5 | `PTR-005` | Petrova - Sepatu Boots Strength WB Hijau - Boots Air PVC | Petrova Strength WB Green | **Waterproof PVC Work Boots** (Plain Toe / Utility) | 641 | 4.9 | Rp 110.000 | \$6.88 | Lolos (Non-PPE / General Utility) |
| 6 | `PTR-006` | Petrova - Sepatu Boots Strength WB orange - Boots Air PVC | Petrova Strength WB Orange | **Waterproof PVC Work Boots** (Plain Toe / Utility) | 876 | 4.8 | Rp 110.000 | \$6.88 | Lolos (Non-PPE / General Utility) |
| 7 | `PTR-007` | Sepatu Boots Tinggi PETROVA Classic Hitam - Boots PVC Lentur Lokal | Petrova Classic Black | **Flexible PVC Work Boots** (Plain Toe / Utility) | 15 | 5.0 | Rp 140.000 | \$8.75 | Lolos (Non-PPE / General Utility) |
| 8 | `PTR-008` | Petrova - Sepatu Boots Ultimate Yellow - PVC Steel Toe Cap Anti Static | Petrova Ultimate Yellow | **Industrial Steel Toe Safety Boots** (Impact + Anti-Static) | 1RB+ | 4.9 | Rp 216.500 | \$13.53 | Lolos (Factory Steel Toe Standard) |
| 9 | `PTR-009` | Petrova - Sepatu Boots Nelayan Yellow - PVC Steel Toe Cap Anti Static | Petrova Nelayan Yellow | **Fishery Safety Boots with Steel Toe** (Impact Toe) | 408 | 4.8 | Rp 239.000 | \$14.94 | Lolos (Fishery Marine Safety) |
| 10 | `PTR-010` | Petrova - Sepatu Boots Tinggi Safety ERGOS kuning - Steel Toe PVC | Petrova Safety ERGOS Yellow | **Ergonomic Steel Toe Work Boots** (Impact Toe) | 754 | 4.9 | Rp 167.000 | \$10.44 | Lolos (Factory Steel Toe Standard) |
| 11 | `PTR-011` | Sepatu Boots Tinggi PETROVA Pro Green Boots Karet Lentur Lokal perkebunan | Petrova Pro Green | **Flexible PVC Plantation Boots** (Plain Toe / Utility) | 25 | 5.0 | Rp 90.000 | \$5.62 | Lolos (Plantation Utility) |
| 12 | `PTR-012` | Petrova - Sepatu Boots Ultimate Yellow Size 43 - PVC Steel Toe Cap | Petrova Ultimate Yellow (43) | **Industrial Steel Toe Safety Boots** (Size Variant) | 50 | 4.8 | Rp 216.500 | \$13.53 | Lolos (Factory Steel Toe Standard) |
| 13 | `PTR-013` | Petrova - Sepatu Boots Ultimate Yellow Size 39 - PVC Steel Toe Cap | Petrova Ultimate Yellow (39) | **Industrial Steel Toe Safety Boots** (Size Variant) | 27 | 4.8 | Rp 216.500 | \$13.53 | Lolos (Factory Steel Toe Standard) |
| 14 | `PTR-014` | Petrova - Sepatu Boots Ultimate Yellow Size 44 - PVC Steel Toe Cap | Petrova Ultimate Yellow (44) | **Industrial Steel Toe Safety Boots** (Size Variant) | 23 | 4.8 | Rp 216.500 | \$13.53 | Lolos (Factory Steel Toe Standard) |
| 15 | `PTR-015` | Petrova - Sepatu Boots Ultimate Yellow Size 41 - PVC Steel Toe Cap | Petrova Ultimate Yellow (41) | **Industrial Steel Toe Safety Boots** (Size Variant) | 89 | 4.8 | Rp 216.500 | \$13.53 | Lolos (Factory Steel Toe Standard) |
| 16 | `PTR-016` | Petrova - Sepatu Boots Ultimate Yellow Size 38 - PVC Steel Toe Cap | Petrova Ultimate Yellow (38) | **Industrial Steel Toe Safety Boots** (Size Variant) | 15 | 5.0 | Rp 216.500 | \$13.53 | Lolos (Factory Steel Toe Standard) |
| 17 | `PTR-017` | Petrova - Sepatu Boots Ultimate Yellow Size 40 - PVC Steel Toe Cap | Petrova Ultimate Yellow (40) | **Industrial Steel Toe Safety Boots** (Size Variant) | 85 | 4.9 | Rp 216.500 | \$13.53 | Lolos (Factory Steel Toe Standard) |
| 18 | `PTR-018` | Petrova - Sepatu Boots Phenom Yellow Size 39 - PVC Steel Toe Cap | Petrova Phenom Yellow (39) | **Anti-Static Steel Toe Safety Boots** (Size Variant) | 1 | 5.0 | Rp 177.000 | \$11.06 | Lolos (Factory Steel Toe Standard) |
| 19 | `PTR-019` | Petrova - Sepatu Boots Phenom Yellow - PVC Steel Toe Cap Anti Static | Petrova Phenom Yellow | **Anti-Static Steel Toe Safety Boots** (Impact Toe) | 11 | 4.8 | Rp 177.000 | \$11.06 | Lolos (Factory Steel Toe Standard) |

---

## 3. Ketentuan Baru pada Deskripsi Produk B2B (GPSR Compliance)

Seluruh deskripsi produk yang digenerate oleh sistem untuk listing Petrova di Alibaba secara otomatis menyertakan:

1. **Header Legalitas & Produsen:**
   * Brand: **PETROVA®**
   * Legal Manufacturer: **PT Waru Gunung** (Surabaya, Jawa Timur, Indonesia)
   * Export Supply Partner: **PT Indo Sukses Semesta** (HOTS Trading)
   * Port of Dispatch: **Tanjung Perak Seaport (Surabaya)** & **Tanjung Priok Seaport (Jakarta)**.

2. **Klausul Kepatuhan Anti-Overclaim (Section 11 Copy):**
   * Menyatakan bahwa produk disuplai untuk keperluan umum/industri (*general use*).
   * Menegaskan bahwa produk **bukan medical device** dan **bukan PPE tersertifikasi Uni Eropa/Inggris/Amerika** kecuali terdapat sertifikat uji lab resmi per model.

3. **Kotak Peringatan Keselamatan Wajib (Section 6 Safety Information):**
   * Inspeksi sebelum pemakaian (tidak boleh dipakai jika retak/robek/bocor).
   * Batasan penggunaan (dilarang untuk paparan kimia pekat, api terbuka, tegangan tinggi, atau bahaya biologis tanpa sertifikasi khusus).
   * Petunjuk penyimpanan di tempat kering & sejuk.
   * Rekomendasi inspeksi sampel fisik (*sample approval*) sebelum pemesanan kontainer massal.

4. **Matriks Spesifikasi Teknis Presisi:**
   * Membedakan secara tegas produk yang memiliki **Steel Toe Cap (Impact Resistant)** (seperti seri Strength Safety, Ultimate, Nelayan, Ergos, Phenom) versus produk **Reinforced Plain Toe (Non-Safety Utility)** (seperti seri Strength WB, Classic, Pro Green).
   * Tidak ada pencatutan nomor sertifikat palsu / kedaluwarsa.

