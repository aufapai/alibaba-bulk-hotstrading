# Panduan Template & Generator Prompt Foto Produk (Photobank / Alibaba SOP)

Dokumen ini menjelaskan alur kerja (*workflow*) pembuatan gambar produk AI otomatis berbasis **Alibaba Footwear Photo SOP**, khususnya untuk produk yang **belum memiliki deskripsi** (kolom deskripsi kosong).

---

## 🚀 Masalah yang Diselesaikan

Di katalog produk, banyak SKU hanya memiliki judul dan kategori singkat (misalnya: `AP Boots S5 Kuning`, kategori `Safety`), namun kolom `Description` kosong melompong.

Generator ini secara cerdas merakit deskripsi teknis dan 4 prompt foto standar industri B2B secara otomatis menggunakan rumus:
```
[Branding] + [Clean Product Title] + [Detected Color] + [Material] + [Sole] + [Category Contextual Scene]
```

---

## 📁 File yang Tersedia di Folder Ini

| Nama File | Fungsi |
|---|---|
| **`Alibaba_Master_106_SKU_ImageGen_Ready.csv`** | **File Paling Lengkap:** Berisi seluruh **106 SKU AP Boots** dari database master. Deskripsi dan 4 slot prompt foto sudah terisi lengkap 100%! |
| **`Alibaba_Bulk_Template.csv`** | File template asli kamu untuk input produk batch. |
| **`Alibaba_Bulk_Template_With_Prompts.csv`** | Hasil generate dari file `Alibaba_Bulk_Template.csv`. |
| **`Alibaba_Template_Input_Kosong.csv`** | Template bersih jika ingin menambahkan produk baru manual (kolom deskripsi cukup dikosongkan). |
| **`generate_image_prompts.py`** | Script Python inti pembuat prompt otomatis. |
| **`run_image_prompt_generator.bat`** | File klik ganda (*one-click batch*) untuk menjalankan script tanpa perlu buka terminal. |

---

## 📸 Standar 4 Slot Foto Alibaba yang Dihasilkan

| Slot | Jenis Foto | Latar Belakang | Standar Prompt yang Dibuat |
|---|---|---|---|
| **Slot 1** | **Hero / Main Photo** | Pure White (`RGB 255,255,255`) | Sudut 3/4 depan, produk berdiri tegak, mengisi ~85% frame, rasio 1:1, bayangan alami lembut, tanpa teks/watermark. |
| **Slot 2** | **Side Profile** | Pure White (`RGB 255,255,255`) | Sudut samping 90 derajat lurus, menonjolkan tinggi leher sepatu (*shaft height*) dan kontur sol. |
| **Slot 3** | **Outsole / Tread** | Pure White (`RGB 255,255,255`) | Detail makro close-up telapak sol anti-slip, memperlihatkan alur cengkeraman (*traction lugs*). |
| **Slot 4** | **Contextual Usage** | Lokasi Nyata (*Real Scene*) | Foto dokumenter kaki kebawah (tanpa wajah) di lokasi kerja nyata sesuai kategori produk. |

---

## 🏭 Pemetaan Otomatis Lokasi Realistis (Slot 4)

Jika kolom `Description` kosong, generator membaca nama kategori atau kata kunci judul untuk menentukan latar belakang Slot 4:

1. **Safety / Industri:** Lantai pabrik manufaktur industri aktif dengan batas garis kuning keselamatan.
2. **Terra / Pertanian / Perkebunan:** Medan perkebunan tanah basah / berlumpur tropis di siang hari.
3. **Orca / Tambang / Heavy:** Area konstruksi berat dengan kerikil dan puing beton.
4. **Chef / Dapur Restoran:** Lantai dapur komersial basah higienis dengan ubin anti-slip dan stainless steel.
5. **Medic / Medis / Rumah Sakit:** Koridor laboratorium / rumah sakit higienis dengan lantai vinil klinis.
6. **Biker / Casual / Allbike:** Aspal jalanan kota basah setelah hujan lebat dengan pantulan genangan air.
7. **Kids / Anak:** Trotoar pejalan kaki yang basah terkena hujan dengan daun-daun gugur.
8. **Classic / Umum:** Jalanan beraspal basah setelah hujan lebat tropis.

---

## ⚡ Cara Menjalankan Generator untuk Data Baru

1. Masukkan daftar produk kamu ke file **`Alibaba_Bulk_Template.csv`**.
2. Kolom **`Description`** boleh dikosongkan jika belum punya deskripsi.
3. Cukup klik 2x pada file:
   👉 **`run_image_prompt_generator.bat`**
4. File **`Alibaba_Bulk_Template_With_Prompts.csv`** akan langsung terisi prompt lengkap untuk setiap baris SKU!
