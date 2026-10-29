# Panduan Integrasi Nano Banana API (Image-to-Image) dari Database Produk di Antigravity

Dokumen ini berisi panduan langkah demi langkah dan kode siap pakai untuk menjalankan *automated image generation* secara lokal (**Run Locally**) di **Antigravity**. 

Alur kerja (*workflow*) ini membaca data dari daftar produk (CSV/JSON) yang sudah memiliki **URL Gambar Referensi**, mengambil gambar tersebut, lalu meminta model **Nano Banana (`gemini-2.5-flash-image`)** untuk membuat variasi atau foto produk baru yang lebih menarik, dan menyimpannya ke folder lokal.

---

## 1. Arsitektur Alur Kerja (Workflow)

1. **Baca Database:** Skrip membaca file `products.csv` (berisi Nama Produk, Kategori/Deskripsi, Prompt Tambahan, dan URL Gambar Sumber).
2. **Download Image Reference:** Skrip mengunduh gambar dari URL sumber secara *in-memory* (tanpa mengotori penyimpanan lokal).
3. **Proses di Nano Banana API:** Mengirim gambar referensi + instruksi *prompt* ke endpoint `gemini-2.5-flash-image`.
4. **Simpan Hasil Lokal:** Hasil *generate* disimpan otomatis ke folder `./output_images/` sesuai dengan ID atau nama produk.
5. **Update Log/Database:** Menyimpan status keberhasilan dan *path* file baru ke dalam file `products_completed.csv`.

---

## 2. Persiapan Environment Lokal (Di Antigravity)

Buka terminal di dalam workspace **Antigravity** lu, lalu jalankan perintah berikut untuk menyiapkan project. Di sini kita menyediakan **2 opsi bahasa** (Python dan Node.js)—pilih salah satu yang paling cocok sama *stack* lu.

### File `.env` (Wajib untuk Kedua Opsi)
Buat file bernama `.env` di *root folder* project lu dan masukkan API Key dari [Google AI Studio](https://aistudio.google.com/):

```env
GEMINI_API_KEY="AIzaSyYourActualAPIKeyHere123456789"
```

---

## 3. Contoh Data Sumber (`products.csv`)

Buat file bernama `products.csv` di folder yang sama. Pastikan kolomnya mencakup informasi produk dan URL gambar sumber seperti contoh berikut:

```csv
id,product_name,description,source_image_url,custom_prompt
PROD-001,Sepatu Safety Kulit Baja,Sepatu safety ujung besi warna coklat tua,https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600,Taruh produk ini di atas lantai beton proyek konstruksi dengan pencahayaan dramatis sinematik pagi hari
PROD-002,Helm Proyek Kuning,Helm pelindung kepala standar industri,https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?w=600,Tampilkan produk di atas meja kerja kayu dengan latar belakang blueprint arsitektur yang blur (bokeh)
```

---

## 4. Script Eksekusi Lokal (Pilih Python atau Node.js)

### OPSI A: Menggunakan Python (Direkomendasikan untuk Data/CSV)

#### 1. Install Library yang Dibutuhkan
Jalankan di terminal Antigravity:
```bash
pip install google-genai pillow requests python-dotenv pandas
```

#### 2. Buat File `run_nanobanana.py`
```python
import os
import time
import requests
import pandas as pd
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load API Key dari file .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Bro, GEMINI_API_KEY belum dipasang di file .env!")

# Inisialisasi Client Google GenAI
client = genai.Client(api_key=API_KEY)

# Konfigurasi Folder & File
INPUT_CSV = "products.csv"
OUTPUT_CSV = "products_completed.csv"
OUTPUT_DIR = "output_images"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_image_from_url(url):
    """Mengunduh gambar dari URL dan mengubahnya menjadi objek PIL Image."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"  [!] Gagal download gambar dari URL ({url}): {e}")
        return None

def generate_product_image(product_row):
    """Mengirim gambar sumber + prompt ke Nano Banana API."""
    prod_id = product_row['id']
    prod_name = product_row['product_name']
    desc = product_row['description']
    img_url = product_row['source_image_url']
    custom_prompt = product_row['custom_prompt']

    print(f"\n[*] Memproses [{prod_id}] - {prod_name}...")

    # Ambil gambar referensi dari URL
    source_img = download_image_from_url(img_url)
    if source_img is None:
        return None

    # Rangkai prompt instruksi untuk Nano Banana
    full_prompt = (
        f"Pertahankan bentuk dan detail utama dari produk '{prod_name}' ({desc}) pada gambar referensi ini. "
        f"Buat foto komersial profesional baru dengan instruksi berikut: {custom_prompt}. "
        f"Pastikan pencahayaan realistis, resolusi tinggi, dan tampak seperti fotografi studio asli."
    )

    try:
        # Panggil model Nano Banana (gemini-2.5-flash-image)
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[
                source_img,
                full_prompt
            ],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"]
            )
        )

        # Ekstrak dan simpan gambar hasil generate
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                generated_img = Image.open(BytesIO(part.inline_data.data))
                output_filepath = os.path.join(OUTPUT_DIR, f"{prod_id}_nanobanana.png")
                generated_img.save(output_filepath)
                print(f"  [+] Sukses! Gambar disimpan di: {output_filepath}")
                return output_filepath

        print("  [!] API merespons, tapi tidak ada output gambar yang dikembalikan.")
        return None

    except Exception as e:
        print(f"  [!] Error saat memanggil API Nano Banana: {e}")
        return None

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"File {INPUT_CSV} tidak ditemukan! Buat dulu sesuai contoh di panduan.")
        return

    df = pd.read_csv(INPUT_CSV)
    results = []

    print(f"=== Memulai Batch Processing untuk {len(df)} Produk ===")

    for index, row in df.iterrows():
        saved_path = generate_product_image(row)
        
        row_data = row.to_dict()
        row_data['generated_image_path'] = saved_path if saved_path else "FAILED"
        row_data['status'] = "SUCCESS" if saved_path else "ERROR"
        results.append(row_data)

        # Jeda 3 detik antar request agar aman dari Rate Limit
        time.sleep(3)

    # Simpan laporan hasil ke CSV baru
    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n=== Selesai! Cek folder '{OUTPUT_DIR}/' dan laporan di '{OUTPUT_CSV}' ===")

if __name__ == "__main__":
    main()
```

#### 3. Jalankan Secara Lokal
```bash
python run_nanobanana.py
```

---

### OPSI B: Menggunakan Node.js / JavaScript

Jika project lu di Antigravity berbasis JavaScript/TypeScript, gunakan skrip di bawah ini:

#### 1. Install Package yang Dibutuhkan
```bash
npm init -y
npm install @google/genai dotenv csv-parser
```
*(Pastikan tambahkan `"type": "module"` di dalam `package.json` lu).*

#### 2. Buat File `run_nanobanana.js`
```javascript
import fs from "fs";
import path from "path";
import csv from "csv-parser";
import dotenv from "dotenv";
import { GoogleGenAI } from "@google/genai";

dotenv.config();

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const OUTPUT_DIR = "./output_images";

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Fungsi download gambar dari URL lalu ubah ke Base64
async function fetchImageAsBase64(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Gagal fetch gambar: ${response.statusText}`);
  const arrayBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);
  const mimeType = response.headers.get("content-type") || "image/jpeg";
  return {
    inlineData: {
      data: buffer.toString("base64"),
      mimeType: mimeType,
    },
  };
}

async function processProduct(row) {
  console.log(`\n[*] Memproses [${row.id}] - ${row.product_name}...`);
  try {
    const imagePart = await fetchImageAsBase64(row.source_image_url);
    const prompt = `Pertahankan bentuk produk '${row.product_name}' (${row.description}) dari gambar ini. Buat foto katalog baru dengan instruksi: ${row.custom_prompt}. Hasilkan gambar berkualitas studio.`;

    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash-image",
      contents: [imagePart, prompt],
    });

    for (const part of response.candidates[0].content.parts) {
      if (part.inlineData) {
        const buffer = Buffer.from(part.inlineData.data, "base64");
        const outputPath = path.join(OUTPUT_DIR, `${row.id}_nanobanana.png`);
        fs.writeFileSync(outputPath, buffer);
        console.log(`  [+] Berhasil disimpan ke: ${outputPath}`);
        return outputPath;
      }
    }
  } catch (err) {
    console.error(`  [!] Gagal memproses ${row.id}:`, err.message);
  }
  return null;
}

async function runBatch() {
  const products = [];
  fs.createReadStream("products.csv")
    .pipe(csv())
    .on("data", (data) => products.push(data))
    .on("end", async () => {
      console.log(`=== Ditemukan ${products.length} produk di database ===`);
      for (const item of products) {
        await processProduct(item);
        // Delay 3 detik biar gak kena rate limit
        await new Promise((r) => setTimeout(r, 3000));
      }
      console.log("\n=== Semua proses selesai! ===");
    });
}

runBatch();
```

#### 3. Jalankan Secara Lokal
```bash
node run_nanobanana.js
```

---

## 5. Tips Troubleshooting Saat Run Locally

1. **Gambar URL Google Drive / Marketplace:**
   * Jika URL gambar sumber berasal dari **Google Drive**, pastikan link-nya sudah diubah ke format *direct download*: `https://drive.google.com/uc?export=download&id=ID_FILE_LU`.
   * Jika dari Tokopedia/Shopee, pastikan URL berakhiran `.jpg`, `.png`, atau `.webp` bisa diakses publik.
2. **Error `429 Too Many Requests` (Rate Limit):**
   * Karena memproses *batch* banyak produk sekaligus dari database, naikkan nilai `time.sleep(3)` menjadi `time.sleep(6)` atau `10` jika akun Google AI Studio lu masih di tier standar.
3. **Database Langsung (MySQL / PostgreSQL / Supabase):**
   * Kalau data produk lu bukan di CSV melainkan langsung di *database* SQL/Supabase, lu tinggal ganti bagian `pd.read_csv("products.csv")` dengan query `SELECT id, product_name, source_image_url FROM products WHERE generated_image IS NULL`.