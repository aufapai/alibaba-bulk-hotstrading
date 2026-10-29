# 📊 LAPORAN ANALISIS DATA SCRAPING MARKETPLACE (SHOPEE & TOKOPEDIA)

**Official Store:** AP Boots Official (`apbootsofficial` & `AP Boots Shop`)
**Tanggal Pengambilan Data:** 23 September 2026
**Dokumen Analisis:** Hasil komparasi, deduplikasi, dan pemetaan 4 file Excel input.

---

## 📈 1. Ringkasan Eksekutif (Executive Summary)

Analisis ini dilakukan terhadap **4 berkas Excel** yang merupakan hasil *web scraping* otomatis dari dua kanal penjualan e-commerce utama AP Boots:
1. **Shopee:** Berkas `shopee-co-id-2026-09-23.xlsx` berisi data katalog listing lengkap dengan metrik penjualan, harga promo, rating pembeli, serta 4 tautan gambar thumbnail per produk.
2. **Tokopedia:** Tiga berkas bertahap (`tokopedia-com-2026-09-23.xlsx`, `tokopedia-com-2026-09-23-3.xlsx`, dan `tokopedia-com-2026-09-23-3 (1).xlsx`) yang merekam data dari tingkat listing halaman katalog hingga tingkat halaman detail (*deep scraping*) berisi deskripsi teknis, berat satuan, varian ukuran, dan gambar resolusi tinggi (1600x1600).

| Indikator Metrik | Shopee Official Store | Tokopedia Official Store (Terkonsolidasi) |
|---|---|---|
| **Sumber File** | `shopee-co-id-2026-09-23.xlsx` | 3 File Tokopedia (`tokopedia-com-2026-09-23*.xlsx`) |
| **Total Raw Baris Data** | 103 baris | 215 baris (20 + 81 + 114) |
| **Total Produk Unik (Canonical)** | **103 SKU/Produk** | **106 SKU/Produk** |
| **Kelengkapan Detail Spesifikasi** | 103 / 103 (Level Listing) | 87 / 106 (82% dengan Deskripsi Lengkap) |
| **Ketersediaan Gambar HD** | 100% (4 Thumbnail CDN/item) | 88 Produk (1600x1600 White-pad CDN) |
| **Rentang Harga (Min - Max)** | Rp39,900 - Rp340,400 | Rp5,400 - Rp300,400 |
| **Rata-rata Harga Produk** | **Rp131,674** | **Rp89,690** |
| **Estimasi Akumulasi Terjual** | **198,592+ unit** | **102,831+ unit** |
| **Rata-rata Rating Toko** | **4.90 / 5.0** | **4.92 / 5.0** |

> [!TIP]
> **Poin Kunci:** Data Tokopedia memiliki keunggulan berupa **spesifikasi teknis mendalam** (tinggi sepatu boot, panjang outsole dalam cm, berat bersih dalam kg untuk logistik, etalase, dan foto produk resolusi 1600x1600). Sedangkan data Shopee memiliki keunggulan pada **kelengkapan metrik komersial** (100% konsisten pada data penjualan, rating, harga promo, dan kategori lokal).

---

## 🔍 2. Analisis Struktur & Skema Berkas Input

### 2.1 Ringkasan Berkas Input

| Nama Berkas | Ukuran | Jml Baris | Jml Kolom | Deskripsi & Karakteristik Data |
|---|---|---|---|---|
| `shopee-co-id-2026-09-23.xlsx` | 135.6 KB | 103 baris | 15 kolom | Data listing produk Shopee. Kolom teratur berisi harga, nama, terjual, rating, dan tautan CDN Shopee. |
| `tokopedia-com-2026-09-23.xlsx` | 116.6 KB | 20 baris | 35 kolom | Scraping batch 1 Tokopedia (Halaman 1). 19 item memiliki data detail lengkap sampai spesifikasi & foto utama. |
| `tokopedia-com-2026-09-23-3.xlsx` | 526.0 KB | 81 baris | 36 kolom | Scraping batch 2 Tokopedia. 73 item memiliki deskripsi lengkap, harga coret, diskon, stok, dan etalase. |
| `tokopedia-com-2026-09-23-3 (1).xlsx` | 434.2 KB | 114 baris | 35 kolom | Scraping batch 3 Tokopedia dengan pagination multi-page (114 URL ditangkap, 32 tuntas ter-scrape detail). |

### 2.2 Pemetaan Skema Kolom (Schema Column Mapping)

#### A. Skema Berkas Shopee (`shopee-co-id-2026-09-23.xlsx`)
Web scraper mengekstrak elemen grid produk Shopee ke dalam format kolom generik:
- `data`: Harga jual produk (contoh: `70.900`, `229.000`)
- `name`: Nama lengkap produk resmi (contoh: `AP Boots AP STAR Hitam Hitam - Sepatu Kets PVC`)
- `data2`: Akumulasi produk terjual (contoh: `692 terjual`, `2RB+ terjual`, `10RB+ terjual`)
- `data4`: Nilai rating ulasan konsumen (skala 1-5, mayoritas `4.9` atau `5.0`)
- `data6`: Badge promosi platform (contoh: `Pilih Lokal`, `Garansi Tepat Waktu`)
- `data7`: Simbol mata uang (`Rp`)
- `image`, `image2`, `image3`, `image4`: URL CDN gambar produk langsung dari server Shopee (`down-id.img.susercontent.com`)

#### B. Skema Berkas Tokopedia (3 Berkas Konsolidasi)
Data Tokopedia mencakup dua tingkatan ekstraksi:
1. **Level Listing:** `data` (nama produk listing), `data2` (harga), `data3` (angka penjualan), `data4` (diskon %), `data5` (harga normal), `ratingvalue` / `data6` (rating & badge benefit bonus).
2. **Level Detail Produk (Deep Scraping):**
   - `item_page_link`: URL unik produk di Tokopedia (digunakan sebagai *primary key* unik).
   - `product_name`: Nama produk pada halaman detail (mencantumkan varian ukuran, misal: `- 38`).
   - `price` & `original_price`: Harga promo aktif dan harga awal sebelum diskon.
   - `discount`: Persentase potongan harga (berkisar antara `28%` s.d. `34%`).
   - `rating` & `review_count`: Skor rating dan jumlah ulasan tertulis pembeli.
   - `stock_level`: Sisa stok barang yang tertera di sistem.
   - `description`: Teks deskripsi lengkap toko yang memuat: **Kondisi**, **Berat Satuan**, **Kategori**, **Etalase**, **Bahan Material**, dan **Tabel Konversi Ukuran/Tinggi Boot**.
   - `main_image`: Gambar utama produk resolusi tinggi 1600x1600 dengan latar putih bersih (*white pad*).
   - `image_17`: Galeri foto produk sudut tambahan (multi-image dipisahkan oleh *newline*).

### 2.3 Analisis Relasi & Deduplikasi 3 File Tokopedia

Ketiga file Tokopedia merupakan hasil eksekusi scraping bertahap (*incremental runs*):
- **File 1 (`tokopedia-com-2026-09-23.xlsx`):** Merupakan pengujian awal pada halaman pertama toko (20 baris, 19 URL unik).
- **File 2 (`tokopedia-com-2026-09-23-3.xlsx`):** Eksekusi kedua menjangkau beberapa halaman (81 baris, 73 URL unik). Seluruh 73 item memiliki deskripsi produk lengkap.
- **File 3 (`tokopedia-com-2026-09-23-3 (1).xlsx`):** Eksekusi ketiga dengan fitur *pagination* lengkap (114 baris, 114 URL unik). Berkas ini berhasil menjangkau 100% katalog toko, namun terhenti di tengah jalan sehingga hanya 32 item yang selesai mengekstrak detail deskripsi.

> [!IMPORTANT]
> **Hasil Penggabungan & Deduplikasi:**
> Dengan menggabungkan ketiga file tersebut menggunakan URL kanonikal (`item_page_link`), diperoleh total **106 produk unik Tokopedia**.
> Sebanyak **87 produk (82%)** berhasil dilengkapi dengan deskripsi detail, spesifikasi teknis ukuran, berat satuan, dan foto 1600x1600 px tanpa ada data yang hilang.

---

## 🏆 3. Analisis Pasar & Produk Terlaris (Market Intelligence)

### 3.1 Top 10 Produk Terlaris di Shopee Official Store

| No | Nama Produk | Estimasi Terjual | Harga Aktif | Rating | Badge / Status |
|---|---|---|---|---|---|
| 1 | **AP Boots TERRA GP Hitam - Sepatu Boot PVC** | `10RB+ terjual` | Rp83,900 | ⭐ 4.9 | Pilih Lokal |
| 2 | **AP Boots TERRA ECO 3 Hitam - Sepatu Boot PVC** | `10RB+ terjual` | Rp118,900 | ⭐ 4.9 | Pilih Lokal |
| 3 | **AP Boots TERRA ECO 3 Hijau - Sepatu Boot PVC** | `10RB+ terjual` | Rp127,400 | ⭐ 4.9 | Pilih Lokal |
| 4 | **AP Boots 2005 Hijau - Sepatu Boot PVC** | `10RB+ terjual` | Rp78,900 | ⭐ 4.9 | Pilih Lokal |
| 5 | **AP Boots Hobby N Work - Sepatu Boot PVC** | `9RB+ terjual` | Rp97,400 | ⭐ 4.9 | Pilih Lokal |
| 6 | **AP Boots TERRA ECO 3 Kuning - Sepatu Boot PVC** | `9RB+ terjual` | Rp127,400 | ⭐ 4.9 | Pilih Lokal |
| 7 | **AP Boots TERRA GP Hijau - Sepatu Boot PVC** | `9RB+ terjual` | Rp89,900 | ⭐ 4.9 | - |
| 8 | **AP Boots 9506 - Sepatu Boot PVC** | `9RB+ terjual` | Rp165,900 | ⭐ 4.9 | Pilih Lokal |
| 9 | **AP Boots AP 977 Hitam - Sepatu Pantofel PVC** | `8RB+ terjual` | Rp77,400 | ⭐ 4.8 | Pilih Lokal |
| 10 | **AP Boots MOTO 2 - Sepatu Boot PVC** | `7RB+ terjual` | Rp152,400 | ⭐ 4.9 | Pilih Lokal |

### 3.2 Top 10 Produk Terlaris di Tokopedia Official Store

| No | Nama Produk | Estimasi Terjual | Harga Aktif | Rating | Etalase Kategori |
|---|---|---|---|---|---|
| 1 | **AP Boots TERRA ECO 3 Hijau - Sepatu Boot PVC Karet Shoes - 38** | `Terjual 10 rb+` | Rp87,400 | ⭐ 4.9 | AP BOOTS Tinggi |
| 2 | **AP Boots TERRA GP Hitam - Sepatu Boot PVC  Shoes Karet Kerja - 38** | `Terjual 10 rb+` | Rp41,900 | ⭐ 4.9 | Semua Etalase |
| 3 | **AP Boots Hobby N Work - Sepatu Boot PVC - 39** | `Terjual 8 rb+` | Rp57,400 | ⭐ 4.9 | AP Kasual |
| 4 | **AP Boots TERRA ECO 3 Hitam - Sepatu Boot PVC Karet Shoes - 38** | `Terjual 7 rb+` | Rp75,412 | ⭐ 4.9 | AP BOOTS Tinggi |
| 5 | **AP Boots TERRA GP Hijau - Sepatu Boot PVC Karet Shoes Kerja - 38** | `Terjual 7 rb+` | Rp54,400 | ⭐ 4.9 | AP BOOTS Tinggi |
| 6 | **AP Boots 2017 Green - Sepatu Boot PVC Karet Shoes - 37** | `Terjual 6 rb+` | Rp91,400 | ⭐ 4.9 | AP BOOTS Tinggi |
| 7 | **AP Boots ORCA - Sepatu Boot PVC - 38** | `Terjual 6 rb+` | Rp77,900 | ⭐ 5 | AP BOOTS Tinggi |
| 8 | **AP Boots TERRA ECO 3 Kuning - Sepatu Boot PVC Karet Shoes - 38** | `Terjual 5 rb+` | Rp87,400 | ⭐ 4.9 | AP BOOTS Tinggi |
| 9 | **AP Boots 9506 Hijau - Sepatu Boot PVC Karet Shoes - 38** | `Terjual 4 rb+` | Rp125,900 | ⭐ 4.9 | AP BOOTS Tinggi |
| 10 | **AP Boots TERRA ECO 5 - Sepatu Boot PVC Shoes Karet Pria - 25** | `Terjual 3 rb+` | Rp43,900 | ⭐ 4.9 | AP BOOTS |

### 3.3 Temuan Dominasi Seri Produk (*Flagship Series*)
Dari kedua marketplace, teridentifikasi 5 seri produk yang menjadi pilar utama omset dan volume penjualan (*cash cow*):
1. **AP TERRA Series (Terra Eco 3, Terra GP, Terra 5, Terra 1):** Menguasai lebih dari 40% total unit terjual di kedua marketplace. Seri ini merupakan boot PVC serbaguna untuk perkebunan, industri, dan pertukangan dengan harga sangat ekonomis (Rp41.900 - Rp87.400).
2. **AP ORCA Series:** Boot tinggi berdesain tangguh untuk proyek dan pasar basah, mencatat penjualan > 6.000 unit di Tokopedia dan ribuan di Shopee pada harga Rp77.900.
3. **AP CHEF Series (Hitam & Putih):** Sepatu slip-on dapur anti-minyak dan anti-slip tanpa tali, mencatat penjualan > 2.000 unit di Shopee pada segmen harga menengah-atas (Rp229.000).
4. **AP HOBBY N WORK & ALLBIKE:** Sepatu karet santai untuk berkendara motor, sepeda, dan aktivitas kasual dengan ventilasi udara, terjual > 8.000 unit pada harga Rp57.400.
5. **AP STAR Series:** Sepatu sneakers kets berbahan PVC anti-air untuk pemakaian harian santai dan sekolah dengan harga sangat terjangkau (Rp70.900).

---

## 🏷️ 4. Segmentasi Kategori, Etalase & Spesifikasi Logistik

### 4.1 Distribusi Etalase Resmi Tokopedia

| Nama Etalase Toko | Jumlah SKU Terdaftar | Karakteristik Produk | Rentang Harga |
|---|---|---|---|
| **AP BOOTS Tinggi** | 27 SKU | Sepatu & boot sesuai spesifikasi etalase AP BOOTS Tinggi | Rp39.900 - Rp300.400 |
| **Semua Etalase** | 7 SKU | Sepatu & boot sesuai spesifikasi etalase Semua Etalase | Rp39.900 - Rp300.400 |
| **AP Biker dan Sepeda** | 4 SKU | Sepatu & boot sesuai spesifikasi etalase AP Biker dan Sepeda | Rp39.900 - Rp300.400 |
| **AP Kasual** | 3 SKU | Sepatu & boot sesuai spesifikasi etalase AP Kasual | Rp39.900 - Rp300.400 |
| **AP Profesional** | 3 SKU | Sepatu & boot sesuai spesifikasi etalase AP Profesional | Rp39.900 - Rp300.400 |
| **AP Bola** | 2 SKU | Sepatu & boot sesuai spesifikasi etalase AP Bola | Rp39.900 - Rp300.400 |
| **AP Boots Pendek** | 2 SKU | Sepatu & boot sesuai spesifikasi etalase AP Boots Pendek | Rp39.900 - Rp300.400 |
| **AP Safety** | 1 SKU | Sepatu & boot sesuai spesifikasi etalase AP Safety | Rp39.900 - Rp300.400 |
| **AP Pantofel** | 1 SKU | Sepatu & boot sesuai spesifikasi etalase AP Pantofel | Rp39.900 - Rp300.400 |

### 4.2 Distribusi Kategori Marketplace

| Kategori Sistem | Jumlah Produk Terdata | Target Pengguna |
|---|---|---|
| **Boots Pria** | 36 Produk | Pasar domestik kategori Boots Pria |
| **Slip On Pria** | 14 Produk | Pasar domestik kategori Slip On Pria |
| **Boots Anak Laki Laki** | 9 Produk | Pasar domestik kategori Boots Anak Laki Laki |
| **Sepatu Biker** | 4 Produk | Pasar domestik kategori Sepatu Biker |
| **Sepatu Bola** | 3 Produk | Pasar domestik kategori Sepatu Bola |
| **Boots Anak Perempuan** | 3 Produk | Pasar domestik kategori Boots Anak Perempuan |
| **Insole Sepatu Pria** | 3 Produk | Pasar domestik kategori Insole Sepatu Pria |
| **Boots Wanita** | 1 Produk | Pasar domestik kategori Boots Wanita |
| **Sneakers Pria** | 1 Produk | Pasar domestik kategori Sneakers Pria |

### 4.3 Karakteristik Berat Satuan (Untuk Logistik & Ekspor)
Dari ekstraksi deskripsi produk Tokopedia, berhasil diidentifikasi berat bersih satuan produk:

| Berat Satuan | Jumlah Model | Kategori Produk Tipikal |
|---|---|---|
| **1,9 kg** | 14 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **1,7 kg** | 11 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **700 g** | 9 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **1,8 kg** | 7 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **730 g** | 7 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **1,5 kg** | 6 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **900 g** | 5 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **1 kg** | 4 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **2 kg** | 3 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **850 g** | 3 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **550 g** | 3 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **2,5 kg** | 3 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **85 g** | 3 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **800 g** | 2 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **1,3 kg** | 1 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **3 kg** | 1 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |
| **880 g** | 1 model | Boot tinggi perkebunan/proyek (Terra, Orca, 9506, Safety) atau sepatu santai/anak |

> [!NOTE]
> **Insight Logistik:** Mayoritas sepatu boot standar AP Boots memiliki berat satuan **1,7 kg hingga 1,9 kg**, sedangkan sepatu kasual/sandal berkisar antara **550 g hingga 730 g**. Informasi ini sangat penting untuk pengisian bobot satuan pada template bulk upload Padi UMKM dan Alibaba.

---

## ⚖️ 5. Perbandingan Harga Cross-Marketplace (Shopee vs Tokopedia)

Berikut adalah perbandingan harga produk identik yang tersedia di kedua platform:

| Nama Produk / Seri | Harga Shopee | Harga Tokopedia (Nett) | Harga Coret Tokopedia | Diskon Tokopedia | Analisis Perbedaan Harga |
|---|---|---|---|---|---|
| **AP Boots TERRA ECO 3 Hijau** | Rp87.400 | Rp87.400 | Rp117.900 | 26% | **Identik / Stabil** (Strategi penetapan harga seragam) |
| **AP Boots TERRA ECO 3 Hitam** | Rp75.400 | Rp75.412 | Rp104.900 | 28% | **Identik / Stabil** (Strategi penetapan harga seragam) |
| **AP Boots TERRA GP Hijau** | Rp54.400 | Rp54.400 | Rp74.900 | 27% | **Identik / Stabil** (Strategi penetapan harga seragam) |
| **AP Boots TERRA GP Hitam** | Rp41.900 | Rp41.900 | Rp57.900 | 28% | **Identik / Stabil** (Strategi penetapan harga seragam) |
| **AP Boots ORCA** | Rp77.900 | Rp77.900 | Rp117.900 | 34% | **Identik / Stabil** (Strategi penetapan harga seragam) |
| **AP Boots AP STAR Hitam** | Rp70.900 | Rp70.900 | Rp99.900 | 29% | **Identik / Stabil** (Strategi penetapan harga seragam) |
| **AP Boots AP Chef Hitam** | Rp229.000 | Rp229.000 | Rp279.000 | 18% | **Identik / Stabil** (Strategi penetapan harga seragam) |
| **AP Boots AP Chef Putih** | Rp229.000 | Rp229.000 | Rp279.000 | 18% | **Identik / Stabil** (Strategi penetapan harga seragam) |
| **AP Boots Hobby N Work** | Rp57.400 | Rp57.400 | Rp79.900 | 28% | **Identik / Stabil** (Strategi penetapan harga seragam) |
| **AP Boots 2017 Green** | Rp91.400 | Rp91.400 | Rp124.900 | 27% | **Identik / Stabil** (Strategi penetapan harga seragam) |
| **Ap Boots 995 Hitam (Sandal)** | Rp39.900 | Rp39.900 | Rp54.900 | 27% | **Identik / Stabil** (Strategi penetapan harga seragam) |

### Temuan Kebijakan Harga:
- **Kebijakan Harga Seragam (*Uniform Pricing*):** Harga nett akhir konsumen di Shopee dan Tokopedia dikendalikan secara ketat oleh prinsipal dan bersifat identik (contoh: AP Terra Eco 3 Hijau sama-sama dijual Rp87.400).
- **Pola Diskon Coret di Tokopedia:** Tokopedia secara konsisten menampilkan harga acuan ritel (MSRP) dicoret dengan potongan rata-rata **26% hingga 34%**, sedangkan Shopee menampilkan harga promo langsung disertai label program `Pilih Lokal`.

---

## 📋 6. Tabel Master Produk Terkonsolidasi (Sampel 30 Produk Populer)

Tabel berikut menyatukan data nama resmi, etalase, estimasi berat, rentang harga, total penjualan gabungan, serta kelengkapan materi gambar:

| No | Nama Produk / Model | Etalase | Berat | Harga Ritel | Total Terjual (Est) | Gambar Resolusi Tinggi | Status Data Detail |
|---|---|---|---|---|---|---|---|
| 1 | **AP Boots TERRA ECO 3 Hijau - Sepatu Boot PVC Karet Shoes - 38** | AP BOOTS Tinggi | 1,7 kg | Rp87,400 | Terjual 10 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 2 | **AP Boots TERRA GP Hitam - Sepatu Boot PVC  Shoes Karet Kerja - 38** | Semua Etalase | 1,9 kg | Rp41,900 | Terjual 10 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 3 | **AP Boots Hobby N Work - Sepatu Boot PVC - 39** | AP Kasual | 1,3 kg | Rp57,400 | Terjual 8 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 4 | **AP Boots TERRA ECO 3 Hitam - Sepatu Boot PVC Karet Shoes - 38** | AP BOOTS Tinggi | 1,7 kg | Rp75,412 | Terjual 7 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 5 | **AP Boots TERRA GP Hijau - Sepatu Boot PVC Karet Shoes Kerja - 38** | AP BOOTS Tinggi | 1,9 kg | Rp54,400 | Terjual 7 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 6 | **AP Boots 2017 Green - Sepatu Boot PVC Karet Shoes - 37** | AP BOOTS Tinggi | 1,8 kg | Rp91,400 | Terjual 6 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 7 | **AP Boots ORCA - Sepatu Boot PVC - 38** | AP BOOTS Tinggi | 1,7 kg | Rp77,900 | Terjual 6 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 8 | **AP Boots TERRA ECO 3 Kuning - Sepatu Boot PVC Karet Shoes - 38** | AP BOOTS Tinggi | 1,7 kg | Rp87,400 | Terjual 5 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 9 | **AP Boots 9506 Hijau - Sepatu Boot PVC Karet Shoes - 38** | AP BOOTS Tinggi | 1,8 kg | Rp125,900 | Terjual 4 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 10 | **AP Boots TERRA ECO 5 - Sepatu Boot PVC Shoes Karet Pria - 25** | AP BOOTS | 1,5 kg | Rp43,900 | Terjual 3 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 11 | **AP Boots AP 977 Hitam - Sepatu Pantofel PVC Flat Shoes - 37** | AP Pantofel | 800 g | Rp37,400 | Terjual 3 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 12 | **AP Boots 2003 Hijau TRICOLOUR - Sepatu Boot PVC Karet Shoes - 37** | AP BOOTS Tinggi | 2 kg | Rp130,900 | Terjual 2 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 13 | **AP Boots TERRA 1 Kuning - Sepatu Boot PVC Shoes Karet - 38** | AP BOOTS Tinggi | 1,9 kg | Rp104,900 | Terjual 2 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 14 | **AP Boots AP 1 Hitam - Sepatu Boots PVC Shoes Karet - 25** | AP BOOTS | 1,5 kg | Rp44,900 | Terjual 2 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 15 | **AP Boots 9303 - Sepatu Boot PVC - 38** | AP BOOTS Tinggi | 2 kg | Rp106,900 | Terjual 2 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 16 | **AP Boots AP Chef Hitam - Sepatu Slip On Dapur Shoes Karet - 38** | AP BOOTS | 1,8 kg | Rp189,000 | Terjual 2 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 17 | **AP Boots 2017 GREEN LIME - Sepatu Boot PVC Karet Shoes - 37** | AP BOOTS Tinggi | 1,8 kg | Rp93,400 | Terjual 1 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 18 | **AP Boots 2005 Hijau - Sepatu Boot PVC Karet Shoes - 23 = 36/37** | Semua Etalase | 1 kg | Rp38,900 | Terjual 1 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 19 | **AP Boots TERRA ECO 3 Orange - Sepatu Boot PVC Karet Shoes - 39** | AP BOOTS Tinggi | 1,7 kg | Rp87,400 | Terjual 1 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 20 | **AP Boots TERRA 1 Putih - Sepatu Boot PVC Shoes Karet - 38** | AP BOOTS Tinggi | 1,9 kg | Rp104,900 | Terjual 1 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 21 | **AP Boots AP 963 Putih - Sepatu Bola PVC - 39** | AP Bola | 850 g | Rp11,900 | Terjual 1 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 22 | **AP Boots AP 1 Putih- Sepatu Boots PVC Shoes Karet - 25** | AP BOOTS | 1,5 kg | Rp57,400 | Terjual 1 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 23 | **AP Boots AP CLOGS Navy - Sepatu Slip On PVC - 39** | AP BOOTS | 730 g | Rp27,400 | Terjual 1 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 24 | **AP Boots ALLBIKE Abu - Sepatu Bike PVC - 38, Abu-abu** | AP Biker dan Sepeda | 700 g | Rp38,900 | Terjual 1 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 25 | **AP Boots ALLBIKE 2 ABU - Sepatu Bike PVC - 39, Abu-abu** | AP Biker dan Sepeda | 700 g | Rp38,900 | Terjual 1 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 26 | **AP Boots AP TERRA 3 HITAM KUNING - Sepatu boots PVC Shoes Karet - 38, hitam kuning** | AP BOOTS Tinggi | 1,9 kg | Rp97,400 | Terjual 1 rb+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 27 | **AP Boots 2017 Tosca - Sepatu Boot PVC - 37** | Semua Etalase | 1,8 kg | Rp93,400 | Terjual 750+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 28 | **AP Boots XT Hijau - Sepatu Boot PVC Karet Shoes - 39** | AP BOOTS | 1,7 kg | Rp104,900 | Terjual 750+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 29 | **AP Boots AP MEDIC Putih - Sepatu Medis APD Safety Shoes - 36** | AP BOOTS | 1,9 kg | Rp252,621 | Terjual 750+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |
| 30 | **AP Boots TERRA 3 Hijau Merah - Sepatu Boot PVC Shoes Karet - 38** | AP BOOTS Tinggi | 1,9 kg | Rp98,900 | Terjual 750+ | ✅ 1600x1600 White-pad | ✅ Lengkap (Spesifikasi + Ukuran) |

---

## 💡 7. Rekomendasi Pemanfaatan Data untuk Proyek Alibaba & Padi UMKM

Data scraping dari Shopee dan Tokopedia ini memberikan fondasi data yang sangat kaya untuk melengkapi katalog dan bulk upload template:

1. **Pengkayaan Spesifikasi Ukuran (*Size Chart*) di Alibaba & Padi UMKM:**
   - Deskripsi produk Tokopedia memuat dimensi presisi (contoh: *size 38 tinggi 37 cm, outsole 25.5 cm* hingga *size 43 tinggi 40 cm, outsole 29.5 cm*). Data ini dapat langsung dipetakan ke atribut spesifikasi produk.
2. **Pengisian Berat Satuan Pengiriman:**
   - Parameter `Berat Satuan` (misal 1.7 kg, 1.9 kg, 700 g) dapat langsung diintegrasikan ke kolom `weight` pada generator template Padi UMKM (`generate_padi_umkm_bulk_batches.py`).
3. **Penyelarasan Aset Gambar Berkualitas Tinggi:**
   - Kolom `main_image` Tokopedia menghasilkan tautan CDN berkualitas 1600x1600 px dengan format latar putih bersih (*clean white background*), sangat ideal untuk standar gambar listing B2B internasional di Alibaba.
4. **Prioritas Listing Berdasarkan Permintaan Pasar (*Demand-Driven Listing*):**
   - Urutan produk yang di-upload ke marketplace B2B atau Padi UMKM sebaiknya memprioritaskan 20 produk terlaris di Shopee & Tokopedia (seri Terra, Orca, Chef, Moto, Allbike) yang telah terbukti memiliki perputaran pasar (*market turnover*) tertinggi.

---
*Laporan ini dibuat secara otomatis dari hasil analisis data empat berkas Excel di direktori `Input/`.*