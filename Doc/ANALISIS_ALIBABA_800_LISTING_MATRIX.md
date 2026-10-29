# 📊 ANALISIS MATRIKS 800 LISTING ALIBABA B2B (PONYTAIL REVIEW)
**File Sumber:** `Input/alibaba-800-listing-matrix.xlsx`  
**Target Platform:** Alibaba.com (B2B Global Trade)  
**Entitas:** PT Indo Sukses Semesta - AP Boots Indonesia  
**Metodologi:** Ponytail Senior Developer (Pragmatis, Data-First, Zero Fluff, 100% Actionable)

---

## ⚡ 1. EXECUTIVE SUMMARY (SIGNAL OVER NOISE)

| Parameter | Hasil Audit | Catatan Teknis / Ponytail Verdict |
| :--- | :--- | :--- |
| **Total Record** | **810 Listing Aktif** | 81 Base SKU × 10 Sudut Industri (B2B Angles). |
| **Kelengkapan Kolom** | **32 / 33 Kolom 100% Lengkap** | Hanya kolom `Alibaba_Category` yang memiliki gap (120 baris kosong / 14.8%). |
| **Struktur Sheets** | **3 Lembar Kerja Valid** | `800_Listings_Master`, `Keyword_Manager_Database`, `SKU_Distribution_Summary`. |
| **Model Harga** | **3-Tier Volume Pricing (USD)** | Tier 1 (MOQ 60), Tier 2 (MOQ 300), Tier 3 (MOQ 1200). Diskon bertingkat konsisten 15-20%. |
| **Spesifikasi Karton** | **Standard Ekspor 100% Seragam** | Dimensi `60 x 40 x 40 cm`, Volume `0.096 CBM`, Isi `12 Pasang/Karton`. Berat kotor: 12 - 24 kg. |
| **Deskripsi Produk** | **HTML Rich Text Pre-Rendered** | 810 deskripsi HTML terstruktur siap tayang dengan parameter spesifik per industri. |
| **Kelemahan Kritis** | **Belum Ada URL Gambar** | Sheet ini murni matriks metadata/konten teks. Perlu di-join dengan CDN Tokopedia / Katalog Gambar. |

---

## 🗂️ 2. ANATOMI SHEETS & METADATA

File excel ini terdiri dari 3 sheet terintegrasi:

### Sheet 1: `800_Listings_Master` (811 Baris × 33 Kolom)
Data operasional utama yang memuat listing lengkap dari identitas SKU, judul SEO, atribut teknis, harga tiered, dimensi logistik, hingga deskripsi HTML khusus:
1. `Listing_ID` (1001 s/d 1810)
2. `Unique_SKU_Code` (Format: `{Base_SKU}-V{1..10}`, contoh: `AP-MX-01-V1`)
3. `Base_SKU` (81 Base SKU unik AP Boots)
4. `Base_Product_Name` (Nama model katalog AP Boots)
5. `Angle_ID` (1 s/d 10)
6. `Target_Industry_Angle` (Niche industri target B2B)
7. `Alibaba_Product_Title` (Judul kaya kata kunci, rata-rata 80-110 karakter)
8. `Alibaba_Category` (Kategori produk Alibaba)
9. `Brand` (`AP Boots` - 100%)
10. `Place_of_Origin` (`Surabaya, Indonesia` - 100%)
11. `Upper_Material` (PVC / Synthetic Rubber Blend)
12. `Outsole_Material` (Nitrile Rubber / Heavy Duty PVC)
13. `Toe_Style` (Soft Toe: 770, 200J Steel Toe Cap: 40)
14. `Boot_Height` (Mid-Calf: 710, High-Cut: 80, Ankle/Clog: 20)
15. `Colors` (Varian warna katalog)
16. `Size_Range` (EU 38 - 43 / EU 39 - 45)
17. `Key_Features` (Waterproof, Oil Resistant, Chemical Proof, Anti-Slip, dll)
18. `Target_Application` (Aplikasi lapangan spesifik)
19. `Primary_Keyword_1` (Keyword utama 1)
20. `Primary_Keyword_2` (Keyword utama 2)
21. `Primary_Keyword_3` (Keyword utama 3)
22. `Longtail_Keywords` (Kombinasi keyword turunan & geografi)
23. `MOQ_Pairs` (60 pasang / 5 karton)
24. `Price_Tier1_USD (MOQ 60)` (Harga pembelian 60-299 pasang)
25. `Price_Tier2_USD (MOQ 300)` (Harga pembelian 300-1199 pasang)
26. `Price_Tier3_USD (MOQ 1200)` (Harga pembelian >= 1200 pasang / 100 karton)
27. `Pairs_Per_Carton` (12 pasang per karton)
28. `Carton_Dimensions` (`60 x 40 x 40 cm`)
29. `Carton_Gross_Weight_KG` (12.0 kg s/d 24.0 kg, rerata 18.0 kg)
30. `Carton_CBM` (`0.096` m³)
31. `Port_of_Loading` (`Surabaya, Indonesia` - Tanjung Perak)
32. `Estimated_Lead_Time` (`7 - 14 Days`)
33. `Tailored_HTML_Description` (HTML pre-styled div container)

### Sheet 2: `Keyword_Manager_Database` (811 Baris × 8 Kolom)
Tabel lookup khusus indexing search engine Alibaba:
- `Unique_SKU_Code`, `Base_Product_Name`, `Target_Industry_Angle`, `Alibaba_Product_Title`
- `Primary_Keyword_1`, `Primary_Keyword_2`, `Primary_Keyword_3` (3 slot kata kunci utama Alibaba)
- `Longtail_Keywords` (Frasa longtail pemancing search intent pembeli B2B global)

### Sheet 3: `SKU_Distribution_Summary` (82 Baris × 4 Kolom)
Distribusi aggregat 81 Base SKU:
- Setiap Base SKU memiliki tepat **10 variasi listing** (`Listing_Variations_Count = 10`).

---

## 🎯 3. STRATEGI MULTI-ANGLE MATRIX (10 SUDUT INDUSTRI)

Setiap produk dasar dipecah menjadi 10 listing independen dengan sudut pemasaran terarah untuk mendominasi hasil pencarian di berbagai segmen industri:

| ID | Target Industry Angle | Fokus Kata Kunci & Copywriting | Porsi Listing |
| :---: | :--- | :--- | :---: |
| **V1** | **Oil & Gas Refinery** | Chemical resistant, oil proof, refinery safety, offshore drilling | 81 listing (10%) |
| **V2** | **Civil Construction** | Impact resistant, heavy duty site wellingtons, puncture proof | 81 listing (10%) |
| **V3** | **Mining & Quarrying** | Heavy duty mining boots, deep cleat, open pit footwear | 81 listing (10%) |
| **V4** | **Agriculture & Farming** | Mud resistant, plantation rubber boots, palm oil plantation boots | 81 listing (10%) |
| **V5** | **Fishery & Seafood** | Wet grip, slip resistant, cold storage, wet market wellingtons | 81 listing (10%) |
| **V6** | **Medical & Kitchen Hygiene** | Cleanroom, hospital clog, food processing sanitary boots | 81 listing (10%) |
| **V7** | **Motorcycle & Courier** | All-weather riding boots, delivery courier waterproof shoes | 81 listing (10%) |
| **V8** | **Chemical & Factory Manufacturing** | Acid & alkali resistant, industrial plant protective footwear | 81 listing (10%) |
| **V9** | **Wholesale OEM Supply** | Bulk distributor supply, OEM private label, export container | 81 listing (10%) |
| **V10** | **All-Weather Rain Utility** | General rain boots, monsoon utility, domestic rubber boots | 81 listing (10%) |

---

## 💰 4. STRUKTUR HARGA TIERED & LOGISTIK EKSPOR

### Distribusi Harga B2B (USD / Pasang)
```
Tier 1 (MOQ 60)   : Min $3.45  | Mean $10.36 | Max $28.75
Tier 2 (MOQ 300)  : Min $2.85  | Mean $8.56  | Max $23.76  (~17.4% discount)
Tier 3 (MOQ 1200) : Min $2.40  | Mean $7.21  | Max $20.00  (~30.4% total discount)
```

### Kapasitas Muat Kontainer Ekspor (Berdasarkan CBM 0.096 & 12 Pasang/Karton)
- **1 Karton:** 12 Pasang | $0.096\text{ m}^3$ | Rata-rata 18.0 kg
- **Kontainer 20ft Standard (Kapasitas efektif ~28 CBM):**
  - Muatan Karton: $\approx 290$ Karton
  - Total Pasang: $\approx 3.480$ Pasang
  - Total Berat Kotor: $\approx 5.2$ Ton
- **Kontainer 40ft High Cube (Kapasitas efektif ~68 CBM):**
  - Muatan Karton: $\approx 700$ Karton
  - Total Pasang: $\approx 8.400$ Pasang
  - Total Berat Kotor: $\approx 12.6$ Ton

---

## 🔍 5. AUDIT TEMUAN & GAP ANALYSIS (CRITICAL FIXES)

### ⚠️ Gap 1: 120 Baris Kategori Kosong (`Alibaba_Category = NaN`)
Sebanyak 12 Base SKU (120 baris variasi) tidak memiliki nilai kategori:
1. `APB-S4-01` (TERRA SAFETY S4 YELLOW) -> Rekomendasi: `Safety Footwear`
2. `APB-MD-01` (AP MEDIC BLUE/GREEN/WHITE) -> Rekomendasi: `Safety Footwear`
3. `APB-TC-06` (TERRA ECO 5 WH) -> Rekomendasi: `Safety Footwear`
4. `APB-T3-02` (TERRA 3 GR - RED) -> Rekomendasi: `Safety Footwear`
5. `APB-TG-03` (TERRA GR/WH/YL) -> Rekomendasi: `Safety Footwear`
6. `APB-B3-03` (963 WH) -> Rekomendasi: `Safety Footwear`
7. `APB-B3-04` (963 CR) -> Rekomendasi: `Safety Footwear`
8. `APB-VT-02` (987/989 /991/995/997/1001 BL) -> Rekomendasi: `Safety Footwear`
9. `APB-ST-03` (AP STAR NAVY/WHITE 38-42) -> Rekomendasi: `Casual Shoes` / `Safety Footwear`
10. `APB-ST-04` (AP STAR BLACK/BLACK 38-42) -> Rekomendasi: `Casual Shoes` / `Safety Footwear`
11. `APB-KD-02` (9307 W) -> Rekomendasi: `Children's Rain Boots`
12. `APB-KD-04` (9309 W) -> Rekomendasi: `Children's Rain Boots`

### ⚠️ Gap 2: Pemetaan ke Template Resmi Alibaba 57 Kolom
File `alibaba-800-listing-matrix.xlsx` memiliki struktur 33 kolom yang sangat kaya, namun template resmi mass upload Alibaba (`Template/Alibaba default template (recommended) (1).xlsx`) mewajibkan 57 kolom spesifik, khususnya:
- Kolom Gambar (`* Product image 1` s/d `Product image 6`): Saat ini kosong di sheet matriks. Harus di-pull dari CDN Tokopedia yang sudah tersimpan di `alibaba_master.db`.
- Atribut Kunci (`Product attribute name 1-5` & `Product attribute value 1-5`): Dipetakan dari `Upper_Material`, `Outsole_Material`, `Toe_Style`, `Boot_Height`, `Colors`.

---

## 🛠️ 6. REKOMENDASI EKSEKUSI PONYTAIL (SHORTEST PATH TO LIVE)

Sesuai prinsip **Ponytail: ladder rung 2 & 5** (gunakan utilitas yang sudah ada di codebase tanpa menambah boilerplate):
1. **Perbaiki Gap Kategori:** Inject nilai kategori untuk 12 SKU yang kosong secara instan dengan one-liner/script singkat.
2. **Sinkronkan URL Gambar dari SQLite:** Ambil 6 URL gambar CDN Tokopedia dari database lokal `Database/alibaba_master.db` berdasarkan pencocokan nama atau SKU dasar.
3. **Generate File Bulk Upload Resmi:** Buat generator ringan yang membaca `alibaba-800-listing-matrix.xlsx` dan mengekspor langsung ke format 57 kolom template Alibaba ke folder `Output/`.
