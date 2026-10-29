# Panduan Sistem Database Multi-Marketplace & Web GUI Alibaba

Sistem ini mengkonsolidasikan seluruh data produk dari folder `Input/` (**Lazada**, **Blibli**, **Tokopedia**, **Shopee**, dan **Alibaba 800 Listing Matrix**) ke dalam database lokal **SQLite** (`Database/alibaba_master.db`), dilengkapi dengan **Smart Image Deduplicator**, **Keyword Bot 800-Matrix**, dan antarmuka **Web GUI** interaktif (`http://localhost:8888`).

---

## 1. Arsitektur Database SQLite Terpadu (`alibaba_master.db`)

Dengan database SQLite ini, Python **tidak perlu lagi bolak-balik membaca file Excel/CSV besar** setiap kali runtime:
- **`products`**: Tabel master katalog ekspor Alibaba (519 produk aktif dengan 47+ kolom spesifikasi Alibaba, harga USD & IDR, MOQ tiers, galeri foto CDN unik, status, dan target keywords).
- **`marketplace_raw`**: Tabel data mentah dari hasil scraping (413 data Lazada, Blibli, Tokopedia, dan Shopee lengkap dengan link asli, rating, penjualan, dan deskripsi).
- **`alibaba_matrix_800`**: 810 listing lengkap dari sheet `800_Listings_Master` dengan 10 Target Industry Angles.
- **`alibaba_keywords`**: 810 baris keyword presisi dari sheet `Keyword_Manager_Database`.

---

## 2. Fitur Smart Image Deduplicator (`App/image_deduplicator.py`)

Menjawab kebutuhan agar foto-foto yang mirip atau thumbnail tidak dobel:
1. **Lazada Image Cleaning**:
   - Menghapus thumbnail `_120x120` yang merupakan duplikat foto utama.
   - Mengubah URL ke format resolusi tinggi kanonikal: `https://img.lazcdn.com/g/p/{hash}.jpg_720x720q80.jpg_.webp`.
   - Mengeliminasi banner promosi, watermark Lazada (`TB13YfFofzO3...`), dan ikon non-produk.
2. **Blibli Image Cleaning**:
   - Mengekstrak identifier gambar produk `_full02`, `_full03`, dll.
   - Memfilter gambar kosong / base64 transparent 1x1 GIF.
3. **Tokopedia & Shopee Normalization**:
   - Menyamakan cache path Tokopedia (`/200-square/`, `/500-square/`) menjadi resolusi penuh `/900/`.
4. **Slot Enforcing**:
   - Memastikan ke-6 slot foto (`image_1` s/d `image_6`) tidak ada foto yang terulang pada listing yang sama.

---

## 3. Integrasi Keyword Bot 800 Matrix (`App/keyword_bot.py`)

Mengintegrasikan file `alibaba-800-listing-matrix.xlsx` secara langsung ke produk:
- Mencocokkan nama produk marketplace dengan 81 model utama AP Boots (AP Max, AP Medic, AP Terra, AP Chef, AP 2003, AP 2006, AP All Bike, AP Clogs 995, dll).
- Menerapkan **10 Target Industry Angles**:
  1. *Agriculture & Farming*
  2. *Civil Construction*
  3. *Oil & Gas Refinery*
  4. *Mining & Quarrying*
  5. *Fishery & Seafood*
  6. *Medical & Kitchen Hygiene*
  7. *Motorcycle & Courier*
  8. *Chemical & Factory Manufacturing*
  9. *Wholesale OEM Supply*
  10. *All-Weather Rain Utility*
- Mengisi secara otomatis:
  - **Judul Alibaba B2B** yang dioptimalkan (maksimal 128 karakter).
  - **Primary Keyword 1, 2, 3**.
  - **Longtail Keywords** siap ekspor.

---

## 4. Cara Menjalankan Web GUI

Cukup klik 2x file batch:
```bash
start_alibaba_manager.bat
```
Aplikasi akan membuka browser otomatis di alamat:
👉 **`http://localhost:8888`**

### Tombol Aksi di Web GUI:
1. **`⚡ Sync Input ke Database`**:
   - Sekali klik, langsung memproses file baru di folder `Input/` ke SQLite.
2. **`🧹 Deduplicate Foto`**:
   - Memindai seluruh produk dan membersihkan foto ganda/thumbnail dalam database.
3. **`🤖 800-Matrix Bot`**:
   - Menyesuaikan keyword dan judul seluruh produk sesuai Target Industry Angle yang dipilih.
4. **`Tab Marketplace`**:
   - Filter cepat: **Semua (519)**, **Lazada (106)**, **Blibli (173)**, **Tokopedia (31)**, **Shopee (103)**, **Alibaba 800 Matrix (810)**.
5. **`📥 Export File`**:
   - Download langsung file bulk upload template Excel (`.xlsx`) dan CSV (`.csv`) dari browser tanpa menyentuh terminal lagi.
