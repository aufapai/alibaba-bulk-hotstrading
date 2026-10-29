# 📋 MASTER KATALOG ACUAN SHOPEE OKTOBER 2026 (AP BOOTS & PETROVA)
**Dokumen Referensi:** Data Scraping Resmi Shopee Official Store (Oktober 2026)  
**Status Implementasi:** Aktif sebagai Acuan Lampiran Utama & Telah Tersinkronisasi ke Database Alibaba  
**File Sumber:**
1. 📁 `Input/shopee-co-id-2026-10-apboots.csv` (104 Produk Resmi AP Boots)
2. 📁 `Input/shopee-co-id-2026-10-petrova.csv` (19 Produk Resmi Petrova)  
**Total Database Shopee:** **123 Produk Aktif**  
**Legal Manufacturer (Pabrik Resmi):** **PT Waru Gunung** (Surabaya, Jawa Timur, Indonesia)  
**Export Supply Partner (Seller of Record):** **PT Indo Sukses Semesta** (HOTS Trading)  
**Standar Kepatuhan:** Mengacu penuh pada **GPSR Batch Compliance PT Waru Gunung** (Anti-Overclaim, Safe Copy, & Geo-Block Prevention).

---

## 1. Ringkasan Eksekutif Dataset Shopee Oktober

| Parameter | AP Boots Official Store | Petrova Boots Official Store | Total Konsolidasi |
|---|:---:|:---:|:---:|
| **Sumber URL** | `https://shopee.co.id/apbootsofficial` | `https://shopee.co.id/petrovabootsofficial` | 2 Toko Resmi Pabrikan |
| **Total Produk** | 104 Produk | 19 Produk | **123 Produk** |
| **Rentang Harga** | Rp 39.900 — Rp 340.400 (~$2.49 — $21.28) | Rp 77.500 — Rp 239.000 (~$4.84 — $14.94) | Rp 39.900 — Rp 340.400 |
| **Rating Toko** | 4.8 — 5.0 | 4.8 — 5.0 | **Konsisten Sangat Tinggi** |
| **Pabrik Legal** | PT Waru Gunung | PT Waru Gunung | **PT Waru Gunung (Surabaya)** |
| **Pelabuhan Ekspor** | Tanjung Perak (SUB) / Tg. Priok (JKT) | Tanjung Perak (SUB) / Tg. Priok (JKT) | **FOB / CIF Indonesia** |

---

## 2. Kategori Produk & Kebijakan Anti-Overclaim (GPSR Compliance)

Setiap produk telah diklasifikasikan ulang untuk mematuhi regulasi platform Alibaba dan negara tujuan (EU, UK, US, CA) agar **bebas dari risiko blokir (*geo-block*)**:

### A. Lini Sepatu Safety (Steel Toe & Midsole Protection)
* **Model AP Boots:** `AP Boots Safety S4 Black`, `AP Boots Safety S5 BLACK`, `AP Boots METAGUARD Black/Kuning`, `AP Boots Terra Safety S4 Kuning`.
* **Model Petrova:** `Petrova STRENGTH Safety Yellow`, `Petrova Ultimate Yellow`, `Petrova Nelayan Yellow`, `Petrova Safety ERGOS Yellow`, `Petrova Phenom Yellow`.
* **Kategori Kepatuhan:** `Industrial Steel Toe Safety Boots`.
* **Klaim Ujung Kaki:** **`Steel Toe Cap (Impact Resistant)`** / **`Steel Midsole Puncture Protection`**.
* **Aturan Compliance:** Tidak mencatut sertifikasi EN ISO / CE palsu kecuali dokumen uji lab per model terverifikasi aktif.

### B. Lini Workplace Hygiene / AP Medic (Anti-Medical Overclaim)
* **Model:** `AP Boots AP MEDIC Hitam / Hijau / Putih / Pink / Biru`.
* **Tindakan Kepatuhan:** **DIUBAH TOTAL** dari *"Medical Protective Shoes"* menjadi:  
  **`AP Boots MEDIC Anti-Slip Workplace Hygiene Clogs for Commercial Cleanroom Food Service Wholesale`**.
* **Kata Kunci Terlarang Dihapus:** `Medical`, `Hospital`, `Surgical`, `Clinical`, `Healthcare`, `Sterile`, `FDA`.
* **Dampak Positif:** Menghilangkan penyebab pemblokiran wilayah Amerika Serikat (US) dan Kanada (CA).

### C. Lini Sepatu Motor / Allbike & Moto (Anti-PPE Overclaim)
* **Model:** `AP Boots ALLBIKE (Merah, Abu, Hijau, Orange)`, `AP Boots ALLBIKE 2`, `AP Boots MOTO 1, 2, 3`.
* **Tindakan Kepatuhan:** Diposisikan strictly sebagai **`Water-Resistant Motorcycle Shoe Covers for Outdoor Courier Utility Wholesale`** (*Splash protection only*).
* **Kata Kunci Terlarang Dihapus:** `PPE Category II/III`, perlindungan benturan kecelakaan motor.
* **Dampak Positif:** Menghilangkan penyebab pemblokiran wilayah Uni Eropa (EU) dan Inggris (GB).

### D. Lini Boots Perkebunan & Utilitas Kerja Umum (Non-Safety Utility)
* **Model AP Boots:** `TERRA GP (Hitam, Hijau)`, `TERRA ECO 2, 3, 5`, `TERRA 1, 2, 3, Forest, Army`, `AP 2003, 2005, 2006, 2007, 2011, 2015 Ultimate, 2017 Green/Tosca/Lime, 2018 Ultraflex`, `AP 1, AP 3, 9303, 9506, 9905`, `Hobby N Work`, `ORCA`, `AP XTR`.
* **Model Petrova:** `Petrova Strength WB (Hitam, Kuning, Biru, Hijau, Orange)`, `Petrova Classic Black`, `Petrova Pro Green`.
* **Kategori Kepatuhan:** **`Waterproof PVC Work Boots`** / **`Reinforced Plain Toe (Non-Safety Utility)`**.
* **Aturan Compliance:** Dilarang mengklaim fitur *safety boot* atau standar EN ISO 20345.

### E. Lini Clogs, Sandal, Pantofel & Olahraga
* **Model Clogs & Sandal:** `AP Clogs (Hitam, Putih Navy, Putih Merah, Putih Abu, Putih Krem, Coklat, Ladies Pink)`, `AP Chef Hitam & Putih`, `Ap Boots 987, 989, 991, 995, 997, 999, 1001, 1003, 977 Pantofel`.
* **Model Sepatu Olahraga/Bola:** `AP 963 Putih/Cream`, `AP 967 Hitam`, `AP 969 Putih Cream`, `AP STAR Hitam Hitam / Hitam Putih`.
* **Model Anak:** `AP Kids 2001`, `AP Kids 2012 (Polkadot, Blue Jeans, Mixed Black, Ungu, Merah)`, `AP Kids Safari (Crocodile, Duck, Elephant, Zebra)`.

---

## 3. Komponen Wajib Baru pada B2B Description HTML (Semua Produk)

Setiap deskripsi produk yang digenerate oleh sistem menyertakan 4 blok integritas:

1. **Header Legalitas & Manufaktur:**
   * **Legal Manufacturer:** **PT Waru Gunung** (Surabaya, Jawa Timur, Indonesia).
   * **Export Supply Partner:** **PT Indo Sukses Semesta** (HOTS Trading).
2. **Klausul Kepatuhan Anti-Overclaim (GPSR Section 11):**
   * Menyatakan produk disuplai untuk keperluan umum/industri (*general use*).
   * Menegaskan bahwa produk **bukan medical device** dan **bukan certified PPE** tanpa dokumen resmi.
3. **Peringatan Keselamatan Wajib (GPSR Section 6 Box):**
   * Pengecekan visual sebelum pakai (tidak boleh dipakai jika retak/robek/bocor).
   * Larangan penggunaan untuk paparan kimia pekat, api terbuka, tegangan tinggi, atau bahaya biologis.
   * Panduan penyimpanan dan kewajiban uji sampel (*sample approval*) sebelum komitmen pesanan massal.
4. **Matriks Spesifikasi Teknis Presisi:**
   * Informasi bahan: *High-Grade PVC / Synthetic Polymer*.
   * Detail toe protection: *Steel Toe Cap* atau *Reinforced Plain Toe*.
   * Negara asal: *Indonesia*.
   * Pelabuhan muat: *Tanjung Perak Seaport (Surabaya)* & *Tanjung Priok Seaport (Jakarta)*.

