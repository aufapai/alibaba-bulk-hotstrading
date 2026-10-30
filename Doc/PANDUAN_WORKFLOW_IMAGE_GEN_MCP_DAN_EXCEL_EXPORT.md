# 📘 PANDUAN LENGKAP WORKFLOW IMAGE GENERATION (NATIVE VS MCP), TAHAP RESOLVE/REVIEW, HINGGA EKSPOR EXCEL ALIBABA

**Dokumen Standar Operasional Prosedur (SOP) & Arsitektur Teknis**  
**Project:** Alibaba & Photobank Catalog Manager  
**Legal Manufacturer:** PT Waru Gunung  
**Export Operator:** PT Indo Sukses Semesta  
**Target Platform:** Alibaba B2B, Shopee Official, & Photobank (`admin.hotstrading.com/photo-bank`)  

---

## 1. RINGKASAN & PENEGASAN ALUR KERJA UTAMA

Berdasarkan kebutuhan operasional terbaru:
1. **Shopee Official Asset Studio Hanya Memiliki 1 Foto Resmi (Hero Image):**
   * Data resmi dari official store Shopee hanya menyediakan 1 foto tampak depan/3-quarter (`hero_[nama].webp`).
   * Foto samping (*side image*) sebelumnya yang keliru telah **dihapus dari Shopee Asset Studio**.
   * Dari 1 foto Hero resmi inilah sistem lokal akan memproduksi 4 variasi slot untuk kebutuhan Photobank & Alibaba B2B.
2. **Tiga Pilihan Mesin Image Generation (Actual AI vs Local Canvas):**
   * **Mode 1: 🚀 Actual Generative AI Studio (FLUX / Diffusion — Rekomendasi Utama):**
     * Menghasilkan foto produk AI nyata yang fotorealistis berdasarkan spesifikasi JSON produk dan referensi foto.
     * Menggenerasi tampak depan 3/4 studio, profil lateral 90°, foto makro tapak sol bergerigi anti-slip, dan foto pemakaian aktif di tanah perkebunan/pertanian becek nyata.
     * Otomatis mengunduh dan menyimpannya langsung ke folder produk masing-masing (`hero_*.webp`, `side_*.webp`, `tread_*.webp`, `usage_*.webp`) tanpa perlu API key atau kuota.
   * **Mode 2: 🔑 Google AI Studio / Imagen 3 (Direct Cloud API):**
     * Terintegrasi langsung dengan endpoint Google AI Studio (`imagen-3.0-generate-002`). Pengguna dapat memasukkan API Key pribadi (`AIzaSy...`) langsung dari modal generator untuk hasil visual resolusi ultra-tinggi.
   * **Mode 3: 📐 Studio Smart Canvas (Offline Local Standalone — Anti Kekecilan):**
     * 100% berjalan lokal di Python (`App/photobank_api_bridge.py`).
     * Memotong kelebihan padding putih (*bounding box detection*), melakukan *upscale* berkualitas tinggi (*Lanczos Resampling + Unsharp Mask*), sehingga sepatu **mengisi 85% bingkai kanvas 1000×1000 px** berlatar putih `#FFFFFF` murni (bebas dari bug gambar kekecilan di tengah kanvas).
     * Sangat cepat, stabil, tanpa dependensi internet/server.
3. **Navigasi Atas Bersih & Bar Aksi Produk Terpilih (Clean Top Navigation):**
   * Header utama dirapikan: 8 tombol utilitas dikelompokkan ke dalam dropdown **`[ 🛠️ Alibaba Tools & Utilities ▾ ]`**.
   * Ketika produk dipilih (dicentang), **Bar Aksi Terpilih** langsung muncul secara mencolok di navigasi atas:
     * **`🎯 [X] Produk Terpilih`**
     * **`[ ⚡ Buat Image Generation (X Terpilih) ]`**
     * **`[ 📑 Export to Excel (X Terpilih) ]`**
     * **`[ ✖ Clear / Batalkan Pilihan ]`**
4. **Tahap "Resolve & Review" Sebelum Upload:**
   * Foto hasil generate dapat ditinjau (*preview*) secara visual di Web GUI terlebih dahulu untuk memastikan resolusi tajam, rasio kanvas 1:1, dan framing 85%.
5. **Tahap Ekspor ke Excel Alibaba & Sinkronisasi Photobank:**
   * Setelah foto di-resolve, pengguna cukup klik `[ 📑 Export to Excel ]` untuk langsung men-generate file **Alibaba Bulk Upload Sheet (.xlsx)** standar 57 kolom siap impor, serta mendaftarkannya ke folder 11 kategori Photobank dan manifest CSV.

---

## 2. DIAGRAM ALUR END-TO-END

```mermaid
flowchart TD
    A["Shopee Official Store (123 SKU)"] -->|Download / Sync| B["Shopee Asset Studio (HANYA FOTO HERO)"]
    B --> C["Pilih Produk (Checklist / Bulk Select di GUI)"]
    
    C --> D{"Pilih Mesin Image Generation"}
    
    subgraph "Jalur 1: Native Standalone (Tanpa MCP)"
        D -->|Pilihan Cepat & Stabil| E1["Python PIL Studio Engine"]
        E1 --> E2["Bounding Box Crop + 85% Canvas Fill"]
        E2 --> E3["Pencocokan Model Katalog (Tread & Usage)"]
        E3 --> G["Hasil 4 Variasi Slot 1000x1000 WebP"]
    end
    
    subgraph "Jalur 2: Google Flow MCP (AI Engine)"
        D -->|Pilihan AI Prompt| F1["Google Flow SDK / Shared Tool"]
        F1 --> F2["Akun: aufahots@gmail.com"]
        F2 --> F3["Render Slot 1-4 via AI Prompts"]
        F3 --> G
    end

    G --> H["TAHAP RESOLVE & REVIEW DI GUI"]
    H -->|Cek Kualitas, Framing 85%, Warna White BG| I{"Apakah Gambar Sudah Sesuai?"}
    I -->|Perlu Koreksi| J["Ganti Foto / Drag & Drop / Re-generate"]
    J --> H
    
    I -->|Disetujui / Resolved| K["Simpan Permanen & Auto-Index"]
    K --> L["Shopee_Product_Assets/[Nama_Folder]/"]
    K --> M["Master Bank Flow/"]
    K --> N["Output/Photobank_Siap_Upload/[11_Kategori]/ & CSV Manifest"]
    
    K --> O["GENERATE OUTPUT AKHIR"]
    O --> P["Alibaba Bulk Sheet (.xlsx) Siap Upload"]
    O --> Q["REST API Push ke admin.hotstrading.com/photo-bank"]
```

---

## 3. PENJELASAN TEKNIS: JIKA MENGGUNAKAN MCP

Jika Anda ingin menggunakan **MCP (Model Context Protocol)** untuk Google Flow:

### A. Mengapa Sandbox Browser Menolak Selenium?
* Google Flow Tools (`https://flow.google.com/shared/tool/...`) berjalan di dalam sandbox `<iframe>` React murni di peramban klien.
* Sandbox browser memiliki batasan keamanan ketat (*Content Security Policy*) yang melarang pemanggilan proses sistem operasi seperti `chromedriver.exe` atau socket lokal Selenium.

### B. Cara Kerja yang Benar dengan MCP:
1. **Arsitektur Eksternal (Local MCP Bridge):**
   * File: [`run_flow_photobank.py`](file:///d:/Work/Hots/Product%20Input/run_flow_photobank.py) dan [`setup_flow_mcp.bat`](file:///d:/Work/Hots/Product%20Input/setup_flow_mcp.bat).
   * Script ini berjalan di luar browser (di terminal Windows Anda) menggunakan Chrome Remote Debugging port (`9222`).
   * Browser Chrome lokal dibuka dengan profil akun **`aufahots@gmail.com`**.
   * MCP server bertindak sebagai jembatan yang mengirimkan prompt dan gambar referensi langsung ke tab Google Flow yang sedang terbuka.
2. **Arsitektur Internal (Flow Tool React TypeScript App):**
   * File: [`Flow_Tool_React_App/FlowImageGeneratorTool.tsx`](file:///d:/Work/Hots/Product%20Input/Flow_Tool_React_App/FlowImageGeneratorTool.tsx).
   * Ditempelkan langsung di dalam editor Google Flow Tool.
   * Memanggil fungsi bawaan `window.Flow.generate.image({ prompt, referenceImage, aspectRatio: "1:1" })`.
   * Menghasilkan gambar langsung di dalam canvas browser tanpa membutuhkan Selenium sama sekali.

---

## 4. TAHAP "RESOLVE & REVIEW" SEBELUM UPLOAD

Sebelum gambar diunggah ke server atau dikonversi ke Excel, gambar harus melalui tahap verifikasi (*Resolve*):

### Checklist Validasi Foto (Resolve Checklist):
1. **Format & Ekstensi:** Harus berekstensi `.webp` (kualitas kompresi 90–92).
2. **Rasio & Resolusi:** Rasio tepat **1:1 Square** dengan ukuran minimal **1000 × 1000 px** (atau 1200 / 1600 px).
3. **Latar Belakang (*Background*):** 
   * Slot 1, 2, dan 3 **WAJIB** berlatar belakang putih bersih seamless (`#FFFFFF` murni / RGB 255, 255, 255).
   * Tidak boleh ada artefak abu-abu atau bayangan kotor di pinggir bingkai.
4. **Proporsi Objek (*Framing Ratio*):**
   * Objek sepatu boot harus **mengisi 82% – 85% area kanvas** (tidak boleh terlalu kecil seperti prangko dan tidak boleh terpotong di tepi).
5. **Kesesuaian 4 Slot:**
   * **Slot 1 (Hero):** Sudut 3/4 tampak depan studio.
   * **Slot 2 (Side):** Profil lateral murni 90° (memperlihatkan tinggi shaft leher boot dan tebal sol).
   * **Slot 3 (Tread):** Tapak sol bawah memperlihatkan alur anti-slip dan cleat bergerigi.
   * **Slot 4 (Contextual):** Tampak pemakaian di tanah perkebunan/pertanian atau pabrik (framing lutut ke bawah).

### Cara Me-review di Web GUI:
* Buka Web GUI (`start.bat` -> `http://localhost:8888`).
* Masuk ke tab **Shopee Official Asset Studio**.
* Klik tombol **`[⚡ Buat Image Gen]`** atau tombol **`[🌐 Flow Studio]`** pada kartu produk.
* Preview visual ke-4 slot akan langsung terlihat. Anda bisa klik gambar untuk memperbesar resolusi aslinya.
* Jika ada gambar yang kurang memuaskan, Anda cukup men-drag foto pengganti ke kotak dropzone kartu produk tersebut.

---

## 5. TAHAP KONVERSI KE EXCEL ALIBABA BULK UPLOAD (`.xlsx`)

Setelah gambar ter-resolve dan tersimpan di folder lokal:

1. **Pemetaan Nama File Standar B2B:**
   Setiap gambar diberi nama otomatis yang terstruktur:
   * Slot 1: `[SKU]_[Nama_Produk]_slot_1_hero.webp`
   * Slot 2: `[SKU]_[Nama_Produk]_slot_2_side.webp`
   * Slot 3: `[SKU]_[Nama_Produk]_slot_3_tread.webp`
   * Slot 4: `[SKU]_[Nama_Produk]_slot_4_usage.webp`
2. **Kompilasi Metadata ke JSON:**
   Metadata spesifikasi produk diperbarui secara otomatis di `Shopee_Product_Assets/[Folder]/[Folder].json`:
   * Kepatuhan GPSR Pabrikan: **PT Waru Gunung** (Surabaya, Indonesia).
   * Eksportir Resmi: **PT Indo Sukses Semesta**.
   * Daftar URL / path gambar ter-resolve untuk slot 1 hingga 4.
3. **Generate File Excel Alibaba:**
   * Di Web GUI, klik tombol **`Export Center`** -> **`Export to Excel (.xlsx)`** atau tombol centang terpilih.
   * Sistem akan mengonversi baris produk menjadi tabel standar template unggah massal Alibaba (*Alibaba Product Bulk Upload Template*):
     * Kolom `Product Name`: Format SEO B2B Bahasa Inggris (contoh: *AP Boots XTR Black Waterproof PVC Work Boots with Self-Cleaning Mud Tread for Agriculture Plantation*).
     * Kolom `Category`: Kategori resmi footwear B2B.
     * Kolom `Image URLs / Image Names`: Mengarahkan ke file gambar 4-slot yang telah di-resolve.
     * Kolom `Price USD` & `MOQ`: Dihitung otomatis berdasarkan Kurs Live Google Forex terkini.

---

## 6. SINKRONISASI KE ADMIN PHOTOBANK (`admin.hotstrading.com`)

Untuk mengunggah gambar ke website tanpa risiko FTP mentah:
1. **Gunakan Tombol "Uji Coba Upload API (Simulasi)":**
   * Di dalam modal studio, klik tombol biru `🧪 Uji Coba Upload API (Simulasi)`.
   * Sistem akan memverifikasi integritas file dan payload multipart tanpa mengubah database live.
2. **Push Live via REST API:**
   * Klik tombol ungu `🚀 Push API ke Admin Photobank`.
   * Endpoint `https://admin.hotstrading.com/api/photobank/upload` akan menerima file dan memasukkannya langsung ke kategori yang tepat (`01_Safety_Boots` s/d `11_General_Lifestyle_Boots`).
3. **Pembaruan Manifest Otomatis:**
   * File [`Output/Photobank_Siap_Upload/DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv`](file:///d:/Work/Hots/Product%20Input/Output/Photobank_Siap_Upload/DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv) akan otomatis mencatat entri baru lengkap dengan ukuran file (KB), nama file baru, dan grup kategori.

---

## 7. CARA MENJALANKAN APLIKASI (QUICK LAUNCH)

Cukup klik ganda file launcher di folder utama:
```bat
start.bat
```
Server lokal akan aktif di `http://localhost:8888` dan peramban web akan terbuka otomatis.

