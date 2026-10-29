# Panduan Unggah Foto Photobank Sesuai Kategori (2026)
**PT Indo Sukses Semesta — AP Boots Photobank Manager**

Dokumen ini menjelaskan struktur 416 foto `.webp` yang telah dipilah, diberi prefix SKU/Model, dan dikelompokkan ke dalam 11 folder kategori resmi agar saat diunggah ke Photobank Admin (`https://admin.hotstrading.com/photo-bank`), seluruh foto **otomatis terdeteksi sebagai `product`** dengan SKU dan kategori yang tepat (tidak lagi masuk ke `unmatched`).

---

## 📁 Lokasi Folder & Pembagian Kategori

Seluruh file yang sudah siap unggah tersimpan rapi di:  
👉 **[`Output/Photobank_Siap_Upload/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload)**

| No | Folder Kategori | Kategori Produk | Jumlah File | Contoh Prefix SKU / Model |
|---|---|---|---|---|
| 1 | [`01_Safety_Boots/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/01_Safety_Boots) | Safety Boots | 19 file | `APB-016_ap-s5.webp`, `APB-019_metaguard...` |
| 2 | [`02_Terra_Series/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/02_Terra_Series) | Terra Series | 39 file | `APB-015_terra_gp...`, `APB-007_terra_eco_3...` |
| 3 | [`03_Orca_Series/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/03_Orca_Series) | Orca Industrial | 8 file | `APB-024_orca_realistic...`, `APB-024_orca_specs...` |
| 4 | [`04_Chef_Series/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/04_Chef_Series) | Chef Series | 16 file | `APB-021_chef_shoe...`, `APB-021_chef_specs...` |
| 5 | [`05_Medic_Series/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/05_Medic_Series) | Medic Series | 4 file | `APB-022_medic_banner...`, `APB-022_medic_white...` |
| 6 | [`06_Biker_Casual/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/06_Biker_Casual) | Biker & Casual | 19 file | `APB-001_allbike...`, `APB-028_moto_2...` |
| 7 | [`07_Classic_Boots/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/07_Classic_Boots) | Classic Boots | 23 file | `APB-006_2003...`, `APB-005_2005...`, `APB-002_2017...` |
| 8 | [`08_Kids_Boots/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/08_Kids_Boots) | Kids Boots | 6 file | `APB-017_kids_safari...`, `APB-018_kids_2012...` |
| 9 | [`09_Sandals_Clogs/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/09_Sandals_Clogs) | Sandals & Clogs | 13 file | `APB-011_clogs_pink...`, `APB-032_clogs_1...` |
| 10 | [`10_Kasual_Sneakers/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/10_Kasual_Sneakers) | Sneakers & Sports | 6 file | `APB-014_bola...`, `APB-033_star_series...` |
| 11 | [`11_General_Lifestyle_Boots/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/11_General_Lifestyle_Boots) | General / Construction | 263 file | `APB-GEN_boots_at_construction...` |
| **TOTAL** | | | **416 file** | |

---

## 📑 File Master Mapping
File tabel CSV lengkap dengan nama file asli, nama file baru, prefix SKU, dan nama folder tersedia di:  
👉 [`Output/Photobank_Siap_Upload/DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv)

---

## 🚀 Cara Unggah ke Website Photobank

1. Buka browser dan login ke:  
   **`https://admin.hotstrading.com/photo-bank`**
2. Pilih / drag-and-drop file **per folder kategori** (atau sekaligus per batch) dari folder [`Output/Photobank_Siap_Upload/`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload):
   * *Tips:* Mengunggah per folder kategori (misal: folder `01_Safety_Boots` terlebih dahulu, lalu `02_Terra_Series`, dst.) akan memudahkan Anda mengontrol status sukses di Photobank admin.
3. Karena setiap file sudah memiliki nama yang diawali kode SKU dan model yang jelas, sistem Photobank akan langsung membaca dan mengelompokkannya sebagai **`product`** dengan SKU terkait secara akurat.
4. Setelah selesai upload, jika Photobank menyediakan tombol **Export CSV** (seperti yang Abang lakukan sebelumnya), cukup simpan CSV-nya dan kirimkan ke sini agar semua link di file Excel Alibaba kita perbarui otomatis!
