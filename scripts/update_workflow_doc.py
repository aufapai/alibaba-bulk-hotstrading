# -*- coding: utf-8 -*-
with open('Doc/WORKFLOW_INTEGRASI_GOOGLE_FLOW_DAN_ALIBABA_MANAGER.md', 'r', encoding='utf-8') as f:
    text = f.read()

new_sections = '''
---

## 9. FITUR PEMILIHAN PRODUK & CUSTOM IMAGE GENERATION (STANDALONE — TANPA MCP)

Untuk memenuhi kebutuhan efisiensi katalog, sistem kini mendukung alur kerja pemilihan produk mirip katalog Alibaba Manager:

1. **Pemilihan Produk Interaktif (Bulk Selection):**
   * Di tab **Shopee Official Asset Studio**, setiap kartu produk dilengkapi kotak centang (*checkbox*).
   * Tersedia **Bar Kontrol Pilihan** dengan tombol `Pilih Semua yang Tampil`, `Pilih Semua (123 Produk)`, dan `Batalkan Pilihan`.
   * Counter realtime menampilkan jumlah produk yang sedang dipilih.

2. **Modal Studio Image Generation Custom (`#photobankGenModal`):**
   * Pengguna dapat memilih opsi gambar apa saja yang ingin digenerate:
     * **Slot 1 (Hero White BG):** Tampak 3/4 depan studio e-commerce berlatar putih bersih (#FFFFFF).
     * **Slot 2 (90° Lateral Side):** Tampak samping ortogonal presisi.
     * **Slot 3 (Outsole Tread):** Tapak sol bawah close-up resolusi tinggi dengan alur gerigi anti-slip.
     * **Slot 4 (Contextual In-Use):** Foto pemakaian aktif di lapangan nyata (kebun/pabrik/konstruksi).
   * Tombol Preset Cepat: `🌟 Semua 4 Slot`, `📐 Hero & Side Saja`, `🔍 Tapak & Pemakaian Saja`.
   * Pilihan Resolusi Kanvas: `1000 x 1000 px`, `1200 x 1200 px`, atau `1600 x 1600 px`.
   * Pilihan Rasio Bingkai Objek: `85% (Optimal - Anti Kekecilan)`, `90% (Penuh)`, `80% (Longgar)`.
   * Pilihan Target Simpan: Otomatis tersimpan ke `Shopee_Product_Assets/[Folder]/`, master `Flow/`, dan terindeks ke 11 kategori resmi Photobank.

3. **Standalone Engine (Tanpa MCP):**
   * Tidak memerlukan instalasi atau dependensi MCP server eksternal.
   * Dijalankan langsung oleh backend Python lokal (`App/photobank_api_bridge.py`) melalui endpoint `/api/photobank/custom-generate` dan `/api/photobank/batch-generate`.
   * Cepat, stabil, dan dapat berjalan secara offline.

---

## 10. LAUNCHER CEPAT BARU: `start.bat`

Telah dibuat launcher cepat baru di root project:
* **File:** [`start.bat`](file:///d:/Work/Hots/Product%20Input/start.bat)
* **Fungsi:** 1-klik untuk memeriksa Python, membuka otomatis browser di `http://localhost:8888`, dan menjalankan aplikasi server Alibaba & Photobank Manager.
'''

if '## 9. FITUR PEMILIHAN PRODUK' not in text:
    text += '\n' + new_sections
    with open('Doc/WORKFLOW_INTEGRASI_GOOGLE_FLOW_DAN_ALIBABA_MANAGER.md', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated WORKFLOW doc successfully!")
else:
    print("Section 9 already present.")
