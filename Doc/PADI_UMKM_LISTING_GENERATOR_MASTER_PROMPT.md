# 🚀 PADI UMKM LISTING GENERATOR — Master Prompt & Workflow v1.0

> **Dibuat untuk:** PT Indo Sukses Semesta — HOTs Trading  
> **Target Platform:** PaDi UMKM (Pasar Digital Pengadaan B2B BUMN & Pemerintah)  
> **Kompatibel dengan:** ChatGPT, Gemini, Claude, Ollama/OpenWebUI (Local LLM)  
> **Tujuan:** Menghasilkan Listing B2B BUMN yang Memenuhi Standar Pengadaan (TKDN, PDN, Pajak PPN/PPh 22, & SEO B2B) Sesuai Batasan Template Resmi (33 Kolom)

---

## Daftar Isi

- [Konsep Dasar](#konsep-dasar)
- [Master Prompt v1.0 PaDi UMKM](#master-prompt-v10-padi-umkm)
- [Struktur 33 Kolom PaDi UMKM Output Schema](#struktur-33-kolom-padi-umkm-output-schema)
- [Taksonomi Kategori Produk AP Boots PaDi UMKM](#taksonomi-kategori-produk-ap-boots-padi-umkm)
- [Aturan Khusus Regulasi BUMN (TKDN, PDN, Pajak)](#aturan-khusus-regulasi-bumn-tkdn-pdn-pajak)
- [Workflow Otomasi & Eksekusi Batch](#workflow-otomasi--eksekusi-batch)

---

## Konsep Dasar

Berbeda dengan platform ekspor global (seperti Alibaba) maupun e-commerce ritel (Shopee/Tokopedia), pengadaan di **PaDi UMKM** memiliki aturan kepatuhan (*compliance*) yang ketat:

1. **Batas Judul Sangat Ketat:** Maksimal **70 karakter** (Alibaba 128 char). Dilarang memasukkan kata spam (*murah*, *promo*, dsb).
2. **Deskripsi Teknis Terstruktur:** Minimal **50 karakter** dan maksimal **2000 karakter** dalam teks polos (*plain text*) yang rapi (bukan HTML).
3. **Kepatuhan TKDN & PDN:** Verifikasi bahwa produk adalah 100% buatan Indonesia (PDN = "Ya") dan pencantuman sertifikasi TKDN resmi.
4. **Pajak Pengadaan BUMN:** Transparansi DPP harga satuan, perlakuan PPN, dan opsi pemungutan PPh Pasal 22 (`PPH 22`).
5. **Maksimal 20 SKU Per File:** Sistem validator PaDi UMKM menolak file yang memuat lebih dari 20 baris produk.

---

## Master Prompt v1.0 PaDi UMKM

Salin prompt di bawah ini ke AI pilihan Anda (Gemini, ChatGPT, Claude, dsb.), isi bagian `[INPUT DATA PRODUK]`, lalu jalankan.

```text
# ROLE

Anda adalah Senior B2B Government & Corporate Procurement Specialist, Indonesian Technical Copywriter, dan Spesialis Listing Marketplace BUMN PaDi UMKM.

Tugas Anda adalah membuat listing produk pengadaan B2B yang presisi, profesional, dan siap unggah ke portal resmi PaDi UMKM (sesuai template resmi 33 kolom).

==================================================
# INPUT DATA PRODUK
==================================================

[ISI DATA DI SINI — Contoh:]
Brand              : AP Boots
Model / Seri       : AP Safety S5
Varian Warna       : Kuning (Yellow)
Ukuran Tersedia    : 38 - 45
Fitur Utama        : Steel Toe Cap (200J), Steel Midsole Anti-Paku, 100% Waterproof, Sol Anti-Slip & Oil Resistant
Material           : PVC Kualitas Industri Heavy Duty
Sertifikasi        : SNI 7079:2009, EN ISO 20345:2011 S5
Status Produksi    : 100% Produk Dalam Negeri (PDN = Ya)
Status TKDN        : Sertifikasi Pihak Ketiga (Nilai: 70.38%)
Harga Satuan (IDR) : Rp 140.800 (Sebelum PPN)
Stok Unit          : 100 pcs
Dimensi Kemasan    : P: 40 cm, L: 30 cm, T: 15 cm | Berat: 2.700 gr
Kategori Target    : Safety Boots (Alat Keselamatan Proyek)

==================================================
# PRIMARY OBJECTIVE & ATURAN VALIDASI
==================================================

1. JUDUL PRODUK:
   - Wajib antara 5 s/d 70 karakter (JANGAN PERNAH LEBIH DARI 70 KARAKTER!).
   - Format baku: [Jenis Barang] [Brand] [Seri] [Warna/Fitur Utama]
   - Contoh: "Sepatu Boot AP Safety S5 Kuning Steel Toe Cap Proyek" (52 char)
   - Buat 3 opsi judul, lalu pilih 1 yang terbaik dan paling efektif untuk pencarian pengadaan BUMN.

2. DESKRIPSI PRODUK:
   - Wajib antara 50 s/d 2000 karakter dalam format Plain Text yang terstruktur rapi.
   - TIDAK MENGGUNAKAN TAG HTML (bukan <p>, <div>, <b>). Gunakan baris baru dan tanda strip (-) untuk bullet points.
   - Wajib memuat:
     a. Paragraf pembuka (Fungsi produk dan target industri pengadaan: pertambangan, konstruksi, perkebunan, logistik, dll).
     b. Poin keunggulan dan fitur keselamatan/teknis.
     c. Rincian spesifikasi teknis lengkap (Material, standar SNI, rentang ukuran, berat).
     d. Pernyataan legalitas: 100% Produk Dalam Negeri (PDN) & TKDN.

3. PEMETAAN PARAMETER 33 KOLOM PADI UMKM:
   Hasilkan tabel atau format JSON siap pakai yang mencakup seluruh 33 kolom template PaDi UMKM:
   - Tipe_Produk           : Barang
   - Nama_Produk           : [Judul terpilih <= 70 char]
   - Deskripsi_Produk      : [Deskripsi 50 - 2000 char]
   - Kategori_Kode         : [Kode numerik resmi PaDi UMKM, misal 2450 untuk Safety Boots]
   - Berat_Produk_gr       : [Angka bulat gram tanpa titik/koma]
   - Dimensi P/L/T         : [Angka bulat cm]
   - Pembelian_Minimum     : 1
   - Brand                 : AP Boots
   - PDN                   : Ya
   - Jenis_TKDN            : Sertifikasi Pihak Ketiga / Tidak Mengetahui
   - Nilai_TKDN            : [Angka desimal atau kosong]
   - Dokumen_Pendukung_TKDN: [URL link sertifikat atau kosong]
   - Foto_Produk_1 s/d 5   : [URL foto langsung]
   - Stok_Unit             : 100
   - Satuan_Stok           : pcs
   - Stok_Selalu_Ada       : Aktif
   - Harga_Satuan          : [Angka bulat tanpa Rp/titik/koma]
   - PPN                   : Non Aktif (atau Aktif)
   - Opsi_PPh              : PPH 22
   - Asuransi_Pengiriman   : Wajib
   - Jadikan_Gratis_Ongkir : Tidak
   - Visibilitas_Produk    : Publik
   - Kode_SKU              : [Kode SKU unik]

Jalankan instruksi ini dengan teliti tanpa menambahkan asumsi yang tidak faktual.
```

---

## Struktur 33 Kolom PaDi UMKM Output Schema

| Kolom | Nama Field Excel | Aturan Nilai | Keterangan Pengadaan BUMN |
|:---:|---|---|---|
| A | `Error_Message` | *Kosong* | Diisi otomatis oleh sistem jika terjadi kesalahan validasi |
| B | `Tipe_Produk` | `Barang` | Default template barang |
| C | `Nama_Produk` | Min 5, Max 70 Char | Unik, tanpa kata promo spam |
| D | `Deskripsi_Produk` | Min 50, Max 2000 Char | Teks terstruktur (Plain Text) |
| E | `Kategori_Kode` | Integer | Kode numerik kategori resmi PaDi UMKM |
| F | `Berat_Produk_gr` | 1 - 500000 | Berat kotor per unit dalam gram |
| G | `Dimensi_Panjang_cm` | Integer | Panjang paket barang (cm) |
| H | `Dimensi_Lebar_cm` | Integer | Lebar paket barang (cm) |
| I | `Dimensi_Tinggi_cm` | Integer | Tinggi paket barang (cm) |
| J | `Pembelian_Minimum` | 1 - 9999 | Minimum Order Quantity (MOQ) |
| K | `Brand` | Max 70 Char | Merek produk (`AP Boots`) |
| L | `PDN` | `"Ya"` / `"Tidak"` | Wajib `"Ya"` untuk produk buatan lokal |
| M | `Jenis_TKDN` | Enum | `"Sertifikasi Pihak Ketiga"` atau `"Tidak Mengetahui"` |
| N | `Nilai_TKDN` | Desimal 0 - 100 | Angka persentase tanpa `%` |
| O | `Dokumen_Pendukung_TKDN` | URL | Link file PDF sertifikat audit Kemenperin |
| P | `Foto_Produk_1` | Direct URL | Foto utama rasio 1:1 latar putih |
| Q-T | `Foto_Produk_2-5` | Direct URL | Foto sudut lain & sol bawah |
| U | `URL_Video_Produk_1` | Direct URL | Link video demo produk (opsional) |
| V | `Stok_Unit` | Integer | Jumlah unit stok gudang |
| W | `Satuan_Stok` | Enum | `"pcs"`, `"pack"`, `"box"`, atau `"lainnya"` |
| X | `Nama_Satuan_Lainnya` | String | Diisi hanya jika satuan = `lainnya` |
| Y | `Stok_Selalu_Ada` | Enum | `"Aktif"` atau `"Non Aktif"` |
| Z | `Pre_Order_Duration` | 1 - 180 | Durasi PO dalam hari (kosong jika ready) |
| AA | `Harga_Satuan` | Integer | Harga satuan DPP sebelum PPN |
| AB | `PPN` | Enum | `"Aktif"` atau `"Non Aktif"` |
| AC | `Opsi_PPh` | Enum | `"PPH 22"` atau `"Tidak Dipotong"` |
| AD | `Asuransi_Pengiriman` | Enum | `"Wajib"` atau `"Opsional"` |
| AE | `Jadikan_Gratis_Ongkir`| Enum | `"Ya"` atau `"Tidak"` |
| AF | `Visibilitas_Produk` | Enum | `"Publik"` atau `"Privat"` |
| AG | `Kode_SKU` | String | Kode SKU unik internal |

---

## Taksonomi Kategori Produk AP Boots PaDi UMKM

Gunakan kode numerik berikut sesuai karakteristik lini produk:

1. **`2450` — Pertukangan > Alat Keselamatan > Safety Boots**  
   - Cocok untuk: *AP Safety S5*, *AP Safety S4*, *AP Metaguard*.  
   - Dilengkapi pelindung jari besi (*Steel Toe Cap*) & telapak baja (*Midsole*).
2. **`658` — Fashion Pria > Sepatu Pria > Boots Pria**  
   - Cocok untuk: *AP Terra (Eco, 2, 3, 5, GP)*, *AP 2006*, *AP Max*, *AP Moto*, *AP Green*, *AP 9303*.  
   - Boot kerja harian, pertanian, perkebunan sawit, sanitasi, dan proyek umum.
3. **`664` — Fashion Pria > Sepatu Pria > Sneakers Pria**  
   - Cocok untuk: *AP All Bike*, *AP Star*.  
   - Sepatu karet casual riding & kegiatan outdoor basah.
4. **`661` — Fashion Pria > Sepatu Pria > Sandal Pria**  
   - Cocok untuk: *AP Clogs*, *AP Van Sandal*.  
   - Selop dan sandal karet anti-slip serbaguna.
5. **`663` — Fashion Pria > Sepatu Pria > Slip On Pria**  
   - Cocok untuk: *AP Chef*, *AP Pantofel*.  
   - Sepatu kerja kitchen/food hygiene & perkantoran.
6. **`519` — Fashion Anak & Bayi > Sepatu Anak Laki-laki > Boots Anak Laki Laki**  
   - Cocok untuk: *AP Kids*, *AP Safari*.  
   - Boot anak tahan air dan lumpur.

---

## Aturan Khusus Regulasi BUMN (TKDN, PDN, Pajak)

1. **Prioritas Belanja BUMN (P3DN):** Pejabat pengadaan BUMN memiliki target kepatuhan P3DN (Peningkatan Penggunaan Produk Dalam Negeri). Memilih `PDN = Ya` dan mencantumkan sertifikat TKDN valid meningkatkan kemungkinan produk terpilih dalam tender atau pembelian langsung secara drastis.
2. **Kesesuaian Faktur Pajak:** Penentuan `Opsi_PPh = PPH 22` mempermudah bendahara instansi BUMN melakukan pemotongan otomatis tanpa harus menolak invoice saat proses pencairan dana.

---

## Workflow Otomasi & Eksekusi Batch

File bulk upload hasil automasi Python telah disiapkan dalam batch maksimal 20 produk:
1. Jalankan skrip pembangun batch:
   ```bash
   python Output/generate_padi_umkm_bulk_batches.py
   ```
2. Ambil file Excel dan folder foto di:
   - [`Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_1.xlsx`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_1.xlsx) (20 Produk)
   - [`Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_2.xlsx`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_2.xlsx) (20 Produk)
   - [`Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_3.xlsx`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_3.xlsx) (20 Produk)
   - [`Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_4.xlsx`](file:///d:/Work/Hots/Product%20Input/Output_PadiUMKM/PadiUMKM_Bulk_Upload_Batch_4.xlsx) (16 Produk)
3. Unggah ke portal [seller.padiumkm.id](https://seller.padiumkm.id) sesuai panduan teknis operasional.
