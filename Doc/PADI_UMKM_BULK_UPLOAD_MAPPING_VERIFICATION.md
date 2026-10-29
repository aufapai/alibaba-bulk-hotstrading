# Document Verifikasi & Mapping Bulk Upload PaDi UMKM - AP Boots (2026)

Document ini memuat hasil verifikasi data, pemetaan 32 kolom template PaDi UMKM, pengelompokan 4 batch file Excel, serta pengelompokan foto produk per batch pada folder khusus **[`Output_PadiUMKM`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM)**.

---

## 1. Lokasi Output & Struktur Folder

Seluruh file hasil generasi tersimpan pada directory:
**[`d:\Work\Hots\Product Input\Output_PadiUMKM`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM)**

- 📄 **File Excel Bulk Upload**:
  1. [`PadiUMKM_Bulk_Upload_Batch_1.xlsx`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_1.xlsx) (20 Produk)
  2. [`PadiUMKM_Bulk_Upload_Batch_2.xlsx`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_2.xlsx) (20 Produk)
  3. [`PadiUMKM_Bulk_Upload_Batch_3.xlsx`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_3.xlsx) (20 Produk)
  4. [`PadiUMKM_Bulk_Upload_Batch_4.xlsx`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_4.xlsx) (16 Produk)

- 🖼️ **Folder Foto Produk (Struktur 1 Folder Flat - Maksimal 3 Foto Terbaik Per Produk)**:
  1. [`Batch_1_Images/`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/Batch_1_Images) (55 foto terbaik disatukan dalam 1 folder flat tanpa subfolder)
  2. [`Batch_2_Images/`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/Batch_2_Images) (54 foto terbaik disatukan dalam 1 folder flat tanpa subfolder)
  3. [`Batch_3_Images/`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/Batch_3_Images) (44 foto terbaik disatukan dalam 1 folder flat tanpa subfolder)
  4. [`Batch_4_Images/`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/Batch_4_Images) (30 foto terbaik disatukan dalam 1 folder flat tanpa subfolder)

---

## 2. Struktur 32 Kolom Template Upload PaDi UMKM

Sesuai dengan sheet **Contoh Pengisian Template Baran** pada [`bulk_template_master_barang.xlsx`](file:///d:/Work/Hots/Product%20Input/bulk_template_master_barang.xlsx):

| No | Nama Kolom Excel | Nilai / Format Default | Ket. |
|---|---|---|---|
| 1 | `Error_Message` | Dikosongkan | Dikelola otomatis oleh PaDi UMKM |
| 2 | `Tipe_Produk` | `Barang` | Wajib |
| 3 | `Nama_Produk` | Max 70 Karakter, Unik | Wajib |
| 4 | `Deskripsi_Produk` | Deskripsi Fitur, Ukuran, PDN 100% | Wajib |
| 5 | `Kategori_Kode` | **`2450`** (Safety Boots), `519` (Kids), `660` (Pantofel), `661` (Clogs) | Wajib |
| 6 | `Berat_Produk_gr` | Berat Satuan per Pasang (500g - 1800g) | Wajib |
| 7-9 | `Dimensi_Panjang_cm` / `Lebar` / `Tinggi` | `35` x `25` x `12` | Wajib |
| 10 | `Pembelian_Minimum` | `1` | Wajib |
| 11 | `Brand` | `AP Boots` | Opsional |
| 12 | `PDN` | `Ya` | Wajib |
| 13 | `Jenis_TKDN` | `Tidak Mengetahui` | Wajib |
| 14-15 | `Nilai_TKDN` & `Dokumen_Pendukung_TKDN` | Dikosongkan | Conditional |
| 16 | `Foto_Produk_1` | Direct Link URL Gambar Publik | Wajib |
| 17-21 | `Foto_Produk_2-5` & `URL_Video_Produk_1` | Dikosongkan | Opsional |
| 22 | `Stok_Unit` | `100` | Wajib |
| 23 | `Satuan_Stok` | `pcs` | Wajib |
| 25 | `Stok_Selalu_Ada` | `Aktif` | Wajib |
| 27 | `Harga_Satuan` | Harga Resmi IDR | Wajib |
| 28 | `PPN` | `Non Aktif` | Wajib |
| 29 | `Opsi_PPh` | `PPH 22` | Wajib |
| 30 | `Asuransi_Pengiriman` | `Wajib` | Wajib |
| 31 | `Jadikan_Gratis_Ongkir` | `Tidak` | Wajib |
| 32 | `Visibilitas_Produk` | `Publik` | Wajib |

---

## 3. Pembagian Batch & Pengelompokan Foto (1 Folder Flat)

- **Batch 1 (20 Produk)**: AP Clogs, AP Allbike, AP Moto, AP Boots Dewasa (Black/White, Green, 9303). Seluruh foto disatukan langsung dalam 1 folder flat di [`Output_PadiUMKM/Batch_1_Images/`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/Batch_1_Images).
- **Batch 2 (20 Produk)**: AP XT, AP 2006, AP Safety S4, AP Metaguard, AP Safety S5. Seluruh foto disatukan langsung dalam 1 folder flat di [`Output_PadiUMKM/Batch_2_Images/`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/Batch_2_Images).
- **Batch 3 (20 Produk)**: AP Max, AP Terra Eco, AP Terra 5, AP Terra 3, AP Terra 2, AP Terra GP. Seluruh foto disatukan langsung dalam 1 folder flat di [`Output_PadiUMKM/Batch_3_Images/`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/Batch_3_Images).
- **Batch 4 (16 Produk)**: AP Terra Army, AP Terra Forest, AP Orca, AP Chef, AP Medic, AP Pantofel Vantopel, AP Kids Boots. Seluruh foto disatukan langsung dalam 1 folder flat di [`Output_PadiUMKM/Batch_4_Images/`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/Batch_4_Images).

