# HOTS Trading: Knowledge Base Internal (Konsolidasi)

**Disusun:** 15 Oktober 2026
**Sumber:** Price List AP Boots (6 April 2026), Guideline Surat Menyurat & SOP Kode Dokumen, T&C Sales & Distribution AP Boots (2 versi), New Business Model Indo Sukses Semesta, brosur AP Chef/Clog, AP Medic, AP Safety, dan catatan kerja proyek.
**Status:** Internal dan rahasia. Jangan dibagikan ke distributor atau buyer (berisi struktur margin dan harga terendah).

---

## 0. Ringkasan Eksekutif

HOTS Trading (PT Indo Sukses Semesta, brand dokumen: PT HOTS Trading Indonesia) menjalankan dua lini bisnis yang berbeda:

| Lini | Model | Pendapatan | Status |
|---|---|---|---|
| **A. Distribusi AP Boots** (principal: PT Waru Gunung Industry / WGI) | Indent agent dan distributor nasional, margin-based | Selisih harga + insentif | Berjalan (Alibaba, CRM, jalur vendor institusi) |
| **B. B2B Export Enabler untuk pabrik/UMKM alas kaki** | Supplier of Record, langganan tahunan + service charge ekspor | Fee paket + 2-20% service charge | Tahap blueprint (dokumen model bisnis versi baru) |

Titik kritis yang perlu diputuskan sebelum dokumen ini dipakai sebagai acuan resmi: lihat **Bagian 9 (Inkonsistensi Data)**. Ada beberapa aturan diskon, kurs, dan PPN yang saling bertentangan antar dokumen.

---

## 1. Profil Perusahaan

- **Entitas:** PT Indo Sukses Semesta (brand: HOTS Trading / PT HOTS Trading Indonesia)
- **Alamat:** Manyar Raya Pantai Indah Kapuk, Blok D5 RT.3/RW.1, Kapuk Muara, Penjaringan, Jakarta Utara 14460
- **Kontak resmi (header surat):** info@hotstrading.com | hotstrading.com | +62 811 6964 7711
- **Gudang:** 2 gudang di Jakarta; pengiriman juga bisa dari gudang pabrik Surabaya
- **Principal utama:** PT Waru Gunung Industry (AP Boots), HOTS berstatus indent agent dan distributor nasional
- **Fokus produk:** Safety footwear, PPE, industrial equipment, rubber & PVC, material konstruksi, consumer goods (positioning: footwear first, APD sebagai konteks sekunder)
- **Brand:** Navy `#0F006C`, Orange `#DE8602`, Gold `#C69D5D`
- **Tim:** BD (Aufa), owner Miss Susi Sumarno
- **Tech stack web:** React + TypeScript (Vite), PHP 8.4, MariaDB, shared cPanel hosting

---

## 2. Portofolio Produk AP Boots

### 2.1 Segmentasi lini

| Segmen | Lini | Catatan |
|---|---|---|
| Safety Utama | AP Safety S4 (Terra Safety), S5, Metaguard, Max | Toe cap; S5 dengan midsole plate anti tusuk |
| Kitchen/Hospitality | AP Chef, AP Clogs | Chef: RubbeTech PVC-free, Ortholite |
| Medical | AP Medic | Anti-static (ESD), tahan sterilisasi hingga 120°C (klaim brosur) |
| Agri / Industri umum | AP Terra (Eco, 2, 3, 5, GP, Army, Forest), seri 2000-an/9000-an, ORCA | Lini volume, margin tipis |
| Comfort/Mobility | AP Moto I-III, AllBike, AllBike 2, Ultraflex 2018 | Perlu dokumen teknis dari pabrik |
| Anak | AP Kids, Safari, Jasmine, dll | Isi 18-24 pasang/dus |
| Bola / Vantopel | Seri 96x (bola), 98x-100x (van) | Harga/dus tertinggi (Rp5-10 juta) |

### 2.2 Spesifikasi brosur (ringkas)

| Produk | Spesifikasi kunci | Harga retail brosur |
|---|---|---|
| AP Chef | Size 38-45, hitam/putih, 6 pasang/karton (65x45x55 cm), 0,7-1,2 kg/pasang | belum tercantum di brosur |
| AP Clog | Size 37-42, 24 pasang/karton (55x40x55 cm), anti slip, ringan | Rp51.000 |
| AP Medic | Size 36-45, warna hijau/hitam/putih/biru/pink, ESD, tahan kimia/asam | Rp299.000 |
| AP Safety S5 | Steel toe 200J, anti-puncture steel midsole, 3M Scotchlite, waterproof; size 39-46 | Rp275.000 (size besar Rp281.000) |
| AP Metaguard | Steel toe 200J, metatarsal guard, proteksi benturan atas tinggi; size 39-43 | Rp253.000 |

Target industri: tambang bawah tanah, heavy civil, petrokimia (Safety); dapur komersial, F&B, sanitasi (Chef/Clog); rumah sakit, kamar operasi, lab (Medic).

### 2.3 Aturan klaim sertifikasi (hard line)

- Jangan mengklaim EN ISO 20345 untuk AP Chef, AP Medic, atau lini yang belum terverifikasi.
- Klaim yang belum dikonfirmasi pabrik (AP Max EH/S3, HACCP, tahan autoclave) ditahan sampai ada konfirmasi tertulis.
- Status SNI 8877:2023 untuk AP Safety belum dikonfirmasi ke WGI. TKDN/P3DN belum siap untuk materi pemasaran.
- Klaim "40+ tahun" hanya merujuk WGI, bukan HOTS Trading.

---

## 3. Price List Internal AP Boots (Update 6 April 2026)

**Catatan membaca tabel:**
- Total **76 SKU** dalam 9 grup.
- Harga Baru = harga per pasang setelah kenaikan April 2026 (sumber: kolom Harga Baru, dalam rupiah).
- Harga Terendah = harga per pasang setelah "Discount PT" per grup (Dewasa/Terra/Anak/ORCA 18%, Safety 30%, Chef/Medic 40%, Bola 16%, Vantopel 15%). Ini adalah **batas bawah internal**.
- USD/pcs dihitung dengan kurs 17.500 (dibulatkan ke atas ke dolar bulat).
- Kolom MoQ dan Minimal Order Transaction di file sumber **kosong**; belum ada angka resmi di price list.
- Interpretasi "Discount PT" sebagai diskon maksimum untuk distributor/PT perlu dikonfirmasi ke Miss Susi.


### AP Boots Dewasa Group (28 SKU)

| SKU | Produk | Size | Isi/dus | Harga Baru/pasang | Disc. PT | Harga Terendah/pasang | Harga/dus | USD/pcs |
|---|---|---|---|---|---|---|---|---|
| APB-CL-01-MLT-42 | AP CLOGS ( WARNA) | 37 - 42 | 24 | Rp50.000 | 18% | Rp41.000 | Rp1.200.000 | $3,00 |
| APB-CL-02-MLT-42 | AP CLOGS ( WHITE, PINK ) | 37 - 42 | 24 | Rp51.000 | 18% | Rp41.820 | Rp1.224.000 | $3,00 |
| APB-AB-03-MLT-45 | AP ALLBIKE BLACK - RED/GREEN/ORANGE | 38 - 45 | 12 | Rp61.000 | 18% | Rp50.020 | Rp732.000 | $4,00 |
| APB-AB-04-BLK-45 | AP ALLBIKE GREY - BLACK | 38 - 45 | 12 | Rp61.000 | 18% | Rp50.020 | Rp732.000 | $4,00 |
| APB-AB-05-MLT-43 | AP ALLBIKE 2 BLACK - RED/GREEN/ORANGE | 39 - 43 | 12 | Rp61.000 | 18% | Rp50.020 | Rp732.000 | $4,00 |
| APB-AB-06-BLK-43 | AP ALLBIKE 2 GREY - BLACK | 39 - 43 | 12 | Rp61.000 | 18% | Rp50.020 | Rp732.000 | $4,00 |
| APB-BW-07-BLK-28 | AP BLACK ( I ) | 25. - 28 | 12 | Rp64.000 | 18% | Rp52.480 | Rp768.000 | $4,00 |
| APB-BW-08-WHT-28 | AP WHITE ( I ) | 25 - 28 | 12 | Rp75.000 | 18% | Rp61.500 | Rp900.000 | $5,00 |
| APB-BW-09-BLK-27 | AP BLACK ( II ) | 25 - 27 | 10 | Rp75.000 | 18% | Rp61.500 | Rp750.000 | $5,00 |
| APB-BW-10-BLK-27 | AP BLACK ( III ) & (V) | 24.- 27 | 12 | Rp67.000 | 18% | Rp54.940 | Rp804.000 | $4,00 |
| APB-GR-11-GRN-25 | 2005 GREEN | 23 - 25 | 18 | Rp61.000 | 18% | Rp50.020 | Rp1.098.000 | $4,00 |
| APB-GR-12-VAR-25 | 2005 + MOTIF | 23 - 25 | 18 | Rp80.000 | 18% | Rp65.600 | Rp1.440.000 | $5,00 |
| APB-GR-13-GRN-28 | 2007 GREEN | 25 - 28 | 12 | Rp80.000 | 18% | Rp65.600 | Rp960.000 | $5,00 |
| APB-GR-14-GRN-39 | 2011 GREEN | 36 - 39 | 12 | Rp80.000 | 18% | Rp65.600 | Rp960.000 | $5,00 |
| APB-GR-15-GRN-43 | 2017 GREEN | 37 - 43 | 10 | Rp102.000 | 18% | Rp83.640 | Rp1.020.000 | $6,00 |
| APB-GR-16-MLT-43 | 2017 GREEN LIME/TOSCA | 37 - 43 | 10 | Rp103.000 | 18% | Rp84.460 | Rp1.030.000 | $6,00 |
| APB-BW-17-BLK-43 | 9905 BLACK | 38 - 43 | 10 | Rp99.000 | 18% | Rp81.180 | Rp990.000 | $6,00 |
| APB-MT-18-BLK-44 | AP MOTO (I) BLACK / RED | 38 - 44 | 12 | Rp110.000 | 18% | Rp90.200 | Rp1.320.000 | $7,00 |
| APB-MT-19-BLK-45 | AP MOTO (II) BLACK / RED | 38 - 45 | 12 | Rp116.000 | 18% | Rp95.120 | Rp1.392.000 | $7,00 |
| APB-MT-20-BLK-45 | AP MOTO (III) BLACK / RED | 38 - 45 | 10 | Rp121.000 | 18% | Rp99.220 | Rp1.210.000 | $7,00 |
| APB-93-21-GRN-43 | 9303 GREEN | 38 - 43 | 10 | Rp113.000 | 18% | Rp92.660 | Rp1.130.000 | $7,00 |
| APB-93-22-GRN-45 | 9303 GREEN | 44 - 45 | 10 | Rp114.000 | 18% | Rp93.480 | Rp1.140.000 | $7,00 |
| APB-XT-23-GRN-43 | AP XT | 38 - 43 | 10 | Rp113.000 | 18% | Rp92.660 | Rp1.130.000 | $7,00 |
| APB-06-24-GRN-43 | 9506 GREEN | 37 - 43 | 10 | Rp127.000 | 18% | Rp104.140 | Rp1.270.000 | $8,00 |
| APB-GR-25-GRN-43 | 2003 GREEN | 37 - 43 | 10 | Rp132.000 | 18% | Rp108.240 | Rp1.320.000 | $8,00 |
| APB-GR-26-GRN-43 | 2006 GREEN | 38 - 43 | 10 | Rp134.000 | 18% | Rp109.880 | Rp1.340.000 | $8,00 |
| APB-BW-27-MLT-43 | 2015 GREEN/GREY/ORANGE/BLACK | 39 - 43 | 10 | Rp138.000 | 18% | Rp113.160 | Rp1.380.000 | $8,00 |
| APB-GR-28-MLT-43 | 2018 ULTRAFLEX GREEN/GREY/BLUE | 39 - 43 | 6 | Rp154.000 | 18% | Rp126.280 | Rp924.000 | $9,00 |

### AP Boots Safety Group (7 SKU)

| SKU | Produk | Size | Isi/dus | Harga Baru/pasang | Disc. PT | Harga Terendah/pasang | Harga/dus | USD/pcs |
|---|---|---|---|---|---|---|---|---|
| APB-S4-01-YLW-43 | TERRA SAFETY S4 YELLOW | 39 - 43 | 6 | Rp242.000 | 30% | Rp169.400 | Rp1.452.000 | $14,00 |
| APB-MG-02-YLW-43 | AP METAGUARD YELLOW | 39 - 43 | 6 | Rp253.000 | 30% | Rp177.100 | Rp1.518.000 | $15,00 |
| APB-S5-03-YLW-43 | AP BOOTS SAFETY S5 YELLOW | 39 - 43 | 6 | Rp275.000 | 30% | Rp192.500 | Rp1.650.000 | $16,00 |
| APB-S5-04-BLK-43 | AP BOOTS SAFETY S5 BLACK | 39 - 43 | 6 | Rp275.000 | 30% | Rp192.500 | Rp1.650.000 | $16,00 |
| APB-S5-05-YLW-46 | AP BOOTS SAFETY S5 YELLOW | 44 - 46 | 5 | Rp281.000 | 30% | Rp196.700 | Rp1.405.000 | $17,00 |
| APB-MX-06-BLK-43 | AP MAX BLACK/GREY | 39 - 43 | 6 | Rp297.000 | 30% | Rp207.900 | Rp1.782.000 | $17,00 |
| APB-MX-07-BLK-43 | AP MAX BROWN/BLACK | 39 - 43 | 6 | Rp297.000 | 30% | Rp207.900 | Rp1.782.000 | $17,00 |

### AP Terra Group (15 SKU)

| SKU | Produk | Size | Isi/dus | Harga Baru/pasang | Disc. PT | Harga Terendah/pasang | Harga/dus | USD/pcs |
|---|---|---|---|---|---|---|---|---|
| APB-TC-01-BLK-27 | TERRA ECO 1 BL | 25 - 27 | 12 | Rp62.000 | 18% | Rp50.840 | Rp744.000 | $4,00 |
| APB-TC-02-BLK-27 | TERRA ECO 2 BL | 25 - 27 | 10 | Rp72.000 | 18% | Rp59.040 | Rp720.000 | $5,00 |
| APB-TC-03-BLK-42 | TERRA ECO 3 BL | 38 - 42 | 10 | Rp92.000 | 18% | Rp75.440 | Rp920.000 | $6,00 |
| APB-TC-04-MLT-43 | TERRA ECO 3 GR/YL/OR | 38 - 43 | 10 | Rp98.000 | 18% | Rp80.360 | Rp980.000 | $6,00 |
| APB-TC-05-GRN-28 | TERRA ECO 5 GR | 25 - 28 | 12 | Rp72.000 | 18% | Rp59.040 | Rp864.000 | $5,00 |
| APB-TC-06-WHT-28 | TERRA ECO 5 WH | 25 - 28 | 12 | Rp83.000 | 18% | Rp68.060 | Rp996.000 | $5,00 |
| APB-T5-07-GRN-42 | TERRA 5 GR | 38 - 42 | 12 | Rp105.000 | 18% | Rp86.100 | Rp1.260.000 | $6,00 |
| APB-T3-08-BLK-42 | TERRA 3 BL/YL | 38 - 42 | 10 | Rp99.000 | 18% | Rp81.180 | Rp990.000 | $6,00 |
| APB-T3-09-GRN-42 | TERRA 3 GR - RED | 38 - 42 | 10 | Rp106.000 | 18% | Rp86.920 | Rp1.060.000 | $7,00 |
| APB-T2-10-GRN-27 | TERRA 2 GR | 25 - 27 | 10 | Rp107.000 | 18% | Rp87.740 | Rp1.070.000 | $7,00 |
| APB-TR-11-MLT-43 | TERRA GR/WH/YL | 38 - 43 | 10 | Rp113.000 | 18% | Rp92.660 | Rp1.130.000 | $7,00 |
| APB-TA-12-VAR-43 | TERRA ARMY | 40 - 43 | 10 | Rp132.000 | 18% | Rp108.240 | Rp1.320.000 | $8,00 |
| APB-TF-13-VAR-43 | TERRA FOREST | 40 - 43 | 10 | Rp132.000 | 18% | Rp108.240 | Rp1.320.000 | $8,00 |
| APB-TG-14-BLK-43 | TERRA GP BLACK | 38 - 43 | 10 | Rp64.000 | 18% | Rp52.480 | Rp640.000 | $4,00 |
| APB-TG-15-GRN-43 | TERRA GP GREEN | 38 - 43 | 10 | Rp75.000 | 18% | Rp61.500 | Rp750.000 | $5,00 |

### AP Chef Group (1 SKU)

| SKU | Produk | Size | Isi/dus | Harga Baru/pasang | Disc. PT | Harga Terendah/pasang | Harga/dus | USD/pcs |
|---|---|---|---|---|---|---|---|---|
| APB-CF-01-BLK-45 | AP CHEF BLACK/WHITE | 38 - 45 | 6 | Rp219.000 | 40% | Rp131.400 | Rp1.314.000 | $13,00 |

### AP Medic Group (1 SKU)

| SKU | Produk | Size | Isi/dus | Harga Baru/pasang | Disc. PT | Harga Terendah/pasang | Harga/dus | USD/pcs |
|---|---|---|---|---|---|---|---|---|
| APB-MD-01-MLT-45 | AP MEDIC BLACK/BLUE/GREEN/WHITE | 36 - 45 | 6 | Rp299.000 | 40% | Rp179.400 | Rp1.794.000 | $18,00 |

### AP Orca Group (1 SKU)

| SKU | Produk | Size | Isi/dus | Harga Baru/pasang | Disc. PT | Harga Terendah/pasang | Harga/dus | USD/pcs |
|---|---|---|---|---|---|---|---|---|
| APB-OR-01-GRN-43 | ORCA GR | 38 - 43 | 10 | Rp90.000 | 18% | Rp73.800 | Rp900.000 | $6,00 |

### AP Boots Anak Group (10 SKU)

| SKU | Produk | Size | Isi/dus | Harga Baru/pasang | Disc. PT | Harga Terendah/pasang | Harga/dus | USD/pcs |
|---|---|---|---|---|---|---|---|---|
| APB-AN-01-MLT-28 | AP KIDS MULTI | 22 - 28 | 24 | Rp41.000 | 18% | Rp33.620 | Rp984.000 | $3,00 |
| APB-AN-02-MLT-28 | AP KIDS STABILLO | 22 - 28 | 24 | Rp43.000 | 18% | Rp35.260 | Rp1.032.000 | $3,00 |
| APB-AN-03-VAR-20 | 9307 W | 15 - 20 | 24 | Rp42.000 | 18% | Rp34.440 | Rp1.008.000 | $3,00 |
| APB-AN-04-VAR-19 | GRANDPRIX | 17 - 19 | 24 | Rp43.000 | 18% | Rp35.260 | Rp1.032.000 | $3,00 |
| APB-AN-05-VAR-21 | 9309 W | 19 - 21 | 18 | Rp47.000 | 18% | Rp38.540 | Rp846.000 | $3,00 |
| APB-AN-06-VAR-24 | 2001 W | 22 - 24 | 18 | Rp64.000 | 18% | Rp52.480 | Rp1.152.000 | $4,00 |
| APB-AN-07-GRN-24 | 2001 GR | 22 - 24 | 18 | Rp66.000 | 18% | Rp54.120 | Rp1.188.000 | $4,00 |
| APB-AN-08-VAR-24 | 2001 ROOT N LEAVES | 22 - 24 | 18 | Rp83.000 | 18% | Rp68.060 | Rp1.494.000 | $5,00 |
| APB-AN-09-VAR-28 | AP SAFARI | 22 - 28 | 24 | Rp61.000 | 18% | Rp50.020 | Rp1.464.000 | $4,00 |
| APB-AN-10-VAR-28 | AP JASMINE | 22 - 28 | 24 | Rp61.000 | 18% | Rp50.020 | Rp1.464.000 | $4,00 |

### AP Boots Bola Group (7 SKU)

| SKU | Produk | Size | Isi/dus | Harga Baru/pasang | Disc. PT | Harga Terendah/pasang | Harga/dus | USD/pcs |
|---|---|---|---|---|---|---|---|---|
| APB-B1-01-BLK-42 | 961 / 967 BL | 37 - 42 | 24 | Rp237.000 | 16% | Rp199.080 | Rp5.688.000 | $14,00 |
| APB-B3-02-BLK-36 | 963 BL | 35 - 36 | 24 | Rp226.000 | 16% | Rp189.840 | Rp5.424.000 | $13,00 |
| APB-B3-03-WHT-43 | 963 / 965 WH | 37 - 43 | 24 | Rp390.000 | 16% | Rp327.600 | Rp9.360.000 | $23,00 |
| APB-B3-04-WHT-36 | 963 WH | 35 - 36 | 24 | Rp352.000 | 16% | Rp295.680 | Rp8.448.000 | $21,00 |
| APB-B3-05-VAR-43 | 963 CR | 37 - 43 | 24 | Rp396.000 | 16% | Rp332.640 | Rp9.504.000 | $23,00 |
| APB-B6-06-WHT-43 | 969 WH | 37 - 43 | 24 | Rp429.000 | 16% | Rp360.360 | Rp10.296.000 | $25,00 |
| APB-B6-07-BLK-43 | 969 BL | 37 - 43 | 24 | Rp341.000 | 16% | Rp286.440 | Rp8.184.000 | $20,00 |

### AP Boots Vantopel Group (6 SKU)

| SKU | Produk | Size | Isi/dus | Harga Baru/pasang | Disc. PT | Harga Terendah/pasang | Harga/dus | USD/pcs |
|---|---|---|---|---|---|---|---|---|
| APB-VT-01-BLK-42 | 985 BL | 37 - 42 | 24 | Rp237.000 | 15% | Rp201.450 | Rp5.688.000 | $14,00 |
| APB-VT-02-BLK-41 | 987/989 /991/995/997/1001 BL | 38 - 41 | 24 | Rp237.000 | 15% | Rp201.450 | Rp5.688.000 | $14,00 |
| APB-VT-03-BLK-41 | 999 BL | 38 - 41 | 24 | Rp259.000 | 15% | Rp220.150 | Rp6.216.000 | $15,00 |
| APB-VT-04-BLK-42 | 977 BL | 37 - 42 | 24 | Rp292.000 | 15% | Rp248.200 | Rp7.008.000 | $17,00 |
| APB-VT-05-BLK-41 | 1003 BL | 38 - 41 | 24 | Rp292.000 | 15% | Rp248.200 | Rp7.008.000 | $17,00 |
| APB-WK-06-BLK-42 | HOBBY & WORK BLACK/RED | 39 - 42 | 12 | Rp72.000 | 15% | Rp61.200 | Rp864.000 | $5,00 |


---

## 4. Struktur Harga, Diskon, dan Termin

Ada tiga sumber aturan yang **tidak sinkron** (detail di Bagian 9). Berikut masing-masing apa adanya.

### 4.1 Guideline Surat Menyurat (draft awal, building phase)

| Item | End User Industri | Distributor / Reseller |
|---|---|---|
| MOQ | Min. 10 pasang | Min. 50 boxes |
| Diskon | Maks. 5% | 10% (termin 30 hari); 15% bila cash ≤7 hari (10% + 5%) |
| Termin | Cash sebelum kirim / maks. 7 hari | Maks. 30 hari |
| Target margin | ≥ 25% | ≥ 15% |
| Retur | Tidak boleh | Tidak boleh, tidak ada konsinyasi |

Prinsip: harga, diskon, dan T&C tidak boleh disamakan antar kategori. Diskon hanya kompensasi cashflow, bukan hasil negosiasi bebas. Termin >30 hari tidak diperbolehkan untuk sementara. Invoice 1x per transaksi.

### 4.2 T&C Sales & Distribution AP Boots (versi revisi 2024)

| Parameter | Ketentuan |
|---|---|
| Margin supplier per kategori | Slow moving (Chef, Medic, Safety) hingga ~40%; Common (Terra, lini standar) ~18%; Fast moving ~15% |
| Diskon volume (basis karton) | <50 karton hingga 5%; 50-149 karton hingga 10%; ≥150 karton hingga 10% dengan evaluasi khusus |
| Maks. diskon per kategori | Slow moving 25-30%; Common 15-18%; Fast moving 10-12% |
| Cash | Tambahan insentif +5%, jatuh tempo maks. 7-10 hari kalender, prioritas produksi dan kirim |
| Kredit | Maks. 30 hari dengan persetujuan; PO pihak ketiga maks. 10 hari; transaksi kecil wajib tunai |
| Klaim kerusakan | Maks. 2x24 jam setelah barang diterima, wajib video unboxing; retur hanya cacat produksi |
| Perubahan harga | Pemberitahuan tertulis min. 7 hari; PO terkonfirmasi sebelum tanggal berlaku memakai harga lama |
| Pajak | Harga **belum termasuk PPN 11%**; pembeli wajib beri NPWP valid |
| Komisi mitra | Maks. 5%; bila margin HOTS ~15%, maks. 1%; dibayar setelah pembayaran lunas |
| Sampel | Min. 3 karton, diskon maks. 5%, tidak dapat dikembalikan, bukan konsinyasi |
| Penyimpanan | >3 bulan di gudang HOTS kena carrying cost |
| Bonus besar | Transaksi ≥ Rp10 miliar, bonus hingga 10%; target bulanan Rp4-8 miliar |
| Pembatalan | PO tidak bisa dibatalkan setelah packing/kirim; Special Order batal = denda 50% nilai PO |
| Audit | Transaksi ≥150 karton: margin HOTS bisa turun ke ~2%, evaluasi dan audit tiap 3 bulan |
| Wilayah | Dilarang jual di luar wilayah atau di bawah HET |
| Kerahasiaan | Struktur margin dan diskon sangat rahasia |

Versi General EN/ID (PDF terpisah) menambahkan: target margin bersih HOTS sekitar **3-4%**, dan <100 karton tidak berlaku diskon 10%.

### 4.3 Kebijakan dari Miss Susi (catatan kerja)

- Diskon AP Boots: pesanan ≥100 pasang maks. 15%; <100 pasang hanya 10%.
- Minimum order 6 dus; 1 dus = 1 ukuran.
- Pesanan khusus/custom dari pabrik umumnya MOQ sekitar 5.000 pasang.
- Kurs internal: IDR ke USD memakai **15.000** (selalu dibulatkan ke atas); USD ke IDR (misal hitung diskon bulk) memakai **20.000**. Keduanya sengaja dipadatkan di atas kurs BCA (~17.500-17.800) untuk melindungi margin.
- Syarat standar: bayar 100% di muka via transfer (BCA, PT Indo Sukses Semesta); franco gudang pabrik Surabaya dan gudang Jakarta; kirim ke gudang utama buyer (last mile tidak ditangani); harga sudah termasuk PPN 12%; lead time 2-6 hari kerja sejak pembayaran; opsi termin dengan T&C.
- Ongkir **tidak termasuk** di SPH distributor domestik (ditanggung buyer); pengiriman dari Jakarta atau Surabaya, mana yang lebih efisien.
- Dokumen difilekan per item/produk, bukan satu folder bersama.

---

## 5. SOP Kode Dokumen dan Surat Menyurat

### 5.1 Format kode

```
[JENIS DOKUMEN]/[KODE PARTNER]/[KATEGORI PRODUK]/[BULAN]/[TAHUN]/[NOMOR URUT]
Contoh: SQ/SAC-VN/APB-AGRI/02/26/014
```

Aturan: huruf kapital semua, tanpa spasi, bulan/tahun format MM/YY, nomor urut min. 3 digit. Penomoran berlaku **per jenis dokumen per bulan**. Revisi memakai suffix `-REV0`, `-REV1`, `-REV2` (contoh `SQ/SAC-VN/APB-AGRI/02/26/014-REV1`).

### 5.2 Jenis dokumen

| Kelompok | Kode |
|---|---|
| Core | RFQ (permintaan harga buyer), SQ (penawaran), PO, INV, PL (packing list) |
| Operasional | DO (surat jalan), GRN (bukti terima), CN (credit note), DN (debit note) |
| Legal/strategis | NDA, LOI, MOU, AGR |

Alur: **RFQ → SQ → PO → INV → PL/DO**. Nomor INV, PL, dan DO mengikuti nomor PO. RFQ dan SQ punya nomor sendiri.

### 5.3 Kode partner dan kategori

- Partner: `[INISIAL]-[NEGARA]`, contoh HTI-ID (HOTS Trading), WGI-ID (Waru Gunung), SAC-VN (Saigon Agri Corp).
- Kategori produk: APB-AGRI (agri), APB-MOTO (motor), APB-SAFE (safety industri), APB-FASH (fashion/umum), APB-GEN (general/campuran).

### 5.4 Template ringkas

- **RFQ (dari buyer):** produk, jumlah, spesifikasi, tujuan kirim, estimasi waktu.
- **SQ:** produk, harga (USD/pair), MOQ, lead time, terms (FOB/CIF), masa berlaku 14 hari.
- **Invoice:** produk, qty, harga, total, terms sesuai PO.
- **Quotation (struktur isi):** header (logo, nama, kontak), body (produk, spesifikasi, qty, harga satuan, total, skema diskon, termin), footer (masa berlaku 7-14 hari, pernyataan T&C singkat).

### 5.5 Template T&C ringkas

- **End user:** jual putus, tanpa retur/tukar, klaim kualitas maks. 3 hari setelah terima, bayar sesuai termin.
- **Distributor:** jual putus tanpa konsinyasi, tanpa retur/pembatalan, keterlambatan bayar memengaruhi harga dan kerja sama berikutnya, harga distributor confidential.

### 5.6 Kerangka Excel pricing (untuk dashboard)

Kolom wajib: harga beli/unit, biaya logistik, biaya operasional, total cost, target margin (%), harga jual sebelum diskon, diskon, harga jual final, skema pembayaran, status approval. Jika margin di bawah standar, status otomatis **NOT APPROVED**.

---

## 6. Model Bisnis B: B2B Export Enabler (Indo Sukses Semesta)

### 6.1 Konsep

HOTS bertindak sebagai **Supplier of Record**: menghubungkan pabrik sepatu lokal ke pasar global via Alibaba Gold Supplier (GGS) tanpa pabrik membayar biaya platform sendiri. Dilengkapi toko online, Odoo ERP privat, dan 5 pilar ekosistem: (1) info session dan mentoring ekspor gratis, (2) HOTS Export Community Network, (3) pendampingan ekspertis sektoral (uji lab ISO 20345, SNI/TKDN, logistik), (4) instant B2B marketing exposure, (5) manufaktur OEM/ODM white-label dengan proteksi IP.

Target: pabrik dan UMKM alas kaki, brand sendiri, dengan model B (HOTS sebagai supplier of record, pabrik tanpa akun Alibaba sendiri tetapi membayar fee berkala sebagai "business partner / as a service").

### 6.2 Paket langganan (basis tahunan)

| Paket | Kuota SKU | Harga | Setara/bulan | Margin HOTS (dokumen) | Catatan |
|---|---|---|---|---|---|
| Trial Nyobain | 1 | Rp660.000 (sekali) | - | 77,3% | Non-member |
| Member Entry | 2 | Rp5.800.000/thn | Rp483.333 | 16,4% | Harga terbaru (draf sosialisasi lama Rp5,5 juta) |
| Starter Standard | 6 | Rp7.500.000/thn | Rp625.000 | 25,3% | Re-instated; paket 5 SKU Rp6 juta dibatalkan |
| Growth | 12 | Rp12.500.000/thn | Rp1.041.667 | 47,2% | Best seller |
| Scale | 24 | Rp22.000.000/thn | Rp1.833.333 | 60,9% | Dedicated content manager |

### 6.3 Service charge ekspor (dihitung atas nilai setelah PPN 11%)

| Skema | Rate | Contoh: order Rp300 juta bruto (Rp267 juta after VAT) |
|---|---|---|
| Member regular deal | 2% | Rp5.340.000 |
| Non-member (ekspor mandiri via kanal HOTS) | 5% | Rp13.350.000 |
| Full Export Assistance, 1 barang | 15% | Rp40.050.000 |
| Full Export Assistance, >1 barang | 20% | Rp53.400.000 |

"1 barang" saat ini ditafsirkan sebagai 1 transaksi/nota (masih tentatif).

### 6.4 Biaya operasional dan proyeksi (dokumen model bisnis)

| Komponen | 2026 | Proyeksi 2027+ |
|---|---|---|
| Gaji tim BD dan operasional | Rp83,4 juta/thn | ~Rp135 juta |
| Operasional, transport, web | Rp6 juta/thn | ~Rp10 juta |
| **Fixed OPEX rutin** | **Rp89,4 juta/thn** (Rp7,45 juta/bln) | ~Rp145 juta |
| Alibaba GGS renewal | Rp33,88 juta/thn | berulang |
| **Total komitmen kas** | **Rp123,28 juta/thn** | ~Rp178,8 juta |

Skenario moderat 12 bulan: 5 Growth + 5 Starter Standard + 10 Trial = Rp106,6 juta (laba kotor Rp48,6 juta); service charge 4 deal Full Assistance 15% + 6 deal member 2% = Rp192,24 juta; total gross revenue Rp298,84 juta; EBITDA Rp151,44 juta; klaim ROI +122,84% vs komitmen kas.

### 6.5 Kontrol anti-bypass

1. Biaya gateway/transaksi Alibaba ditanggung pabrik mitra.
2. Non-circumvention dan NDA: pabrik tidak boleh kontak buyer langsung selama kontrak + 24 bulan sesudahnya.
3. Segmentasi informasi: buyer tidak tahu identitas pabrik, pabrik tidak terima kontak buyer.
4. Proteksi IP dan white-label atas cetakan/moulding dan merek buyer.
5. Payment satu pintu ke rekening PT Indo Sukses Semesta, diteruskan ke pabrik setelah dipotong service charge.
6. Odoo ERP Footwear: size and color grid (EU 38-45), repository sertifikasi SNI/TKDN/ISO, kalkulator multi-Incoterms (EXW/FOB/CIF).

### 6.6 Status eksekusi (per catatan terakhir)

- Odoo ERP dan dokumen model bisnis ini khusus untuk **pabrik/manufaktur member**, bukan untuk lini distribusi AP Boots.
- Tahap awal: seleksi dan screening pabrik dari data yang sudah dimiliki HOTS.
- Hambatan: komunikasi ke pabrik masih lewat Miss Susi; perlu checklist data pabrik yang reusable (syarat Alibaba, info kemampuan OEM, jawaban pertanyaan buyer).
- Dokumen yang masih diminta: scope of services rinci per tier dan per skema service charge, readiness checklist, PRD untuk ERP/program pabrik.
- Pertanyaan terbuka: kepatuhan wording terhadap TOS Alibaba, dan apakah form pengumpulan data pabrik dibangun di database sendiri atau cukup Excel.

---

## 7. Status Operasional Saat Ini

### 7.1 Alibaba GGS (prioritas eksekusi aktif)

- Storefront: hotstrading.trustpass.alibaba.com, GGS Basic Plus aktif.
- Evaluasi: impresi turun tetapi kualitas inquiry naik; skor RFQ 39/100; anomali traffic domestik tinggi di toko berorientasi ekspor.
- Gap: respons RFQ rendah, Green Pass dan Priority Quotes belum dipakai, belum ada iklan berbayar.
- Target listing: ~800 produk aktif (target dashboard 829); data produk dari Tokopedia dinilai berdampak ke views; upload massal lewat template native Alibaba.
- Perlu dibereskan: reconfigure kategori/keyword, upload sertifikat EN ISO 20345 (hanya untuk lini yang terverifikasi), foto produk prioritas, perbaikan Auto-reception/Smart RFQ (spesifikasi sempat salah; AP Boots berbahan PVC, bukan EVA).

### 7.2 CRM dan outreach

- Master_Leads (Google Sheets + AppSheet): ~190 lead Hot/Warm/Cold, auto-cold setelah 30 hari.
- Sekuens email 4 tahap: (1) izin saja, tanpa lampiran/harga; (2) profil + katalog; (3) SPH/quotation; (4) follow-up lunak.
- Enrichment: Hunter.io (utama), Apollo.io (alternatif). Volume awal 50 email/minggu.
- Pasar: Indonesia (konversi terkuat), Vietnam (prioritas ekspor), Filipina, Australia (peluang IA-CEPA 0% tarif; jalur cepat via rubber gumboots agri non-safety).
- Channel baru yang dieksplorasi: Facebook group B2B dan Amazon sellers (private label).

### 7.3 Pipeline vendor institusi (pasif, tanpa channel baru)

| Kanal | Status |
|---|---|
| PLN VMS | Verifikasi |
| PROCSI / Semen Indonesia | Verifikasi (deklarasi Non-PKP diajukan) |
| Jasa Marga DRJM | Tahap awal, dokumen disusun |
| Siloam E-Tender | Terblokir: NITKU dan SPK notariil |
| CIVD SKK Migas | Terblokir: STP Distributor Kemendag |
| Adhi Karya ELISA VMAN | Ditunda: menunggu laporan keuangan tahunan |
| Mayapada | Registrasi berjalan |
| Pengadaan.com | Terdaftar; target PT Satria Bahana Sarana dan Holding BUMN Karya |

**Blocker utama:** Surat Perjanjian Penunjukan Distributor (SPK) notariil dari WGI (tanda tangan Anton, notaris di Surabaya, lalu Susi di Jakarta). Satu dokumen ini membuka STP Kemendag, CIVD, dan Siloam sekaligus. Status Non-PKP adalah kendala struktural yang memengaruhi kelayakan kanal institusi.

### 7.4 Prinsip kerja

- Eksekusi sebelum registrasi: Alibaba dan CRM dulu, jangan tambah channel baru sebelum yang ada terbukti.
- Otomasi hanya untuk proses yang sudah terbukti; audit konversi funnel dulu.
- Framing MOQ: jangan tampilkan sebagai fleksibel; gunakan "jaminan kualitas dan harga terbaik dari jalur resmi".
- Konfirmasi dulu sebelum angka masuk dokumen formal; tandai ambiguitas.
- RFQ screening 4 faktor (kecocokan kategori, selisih harga vs price list, kualitas sinyal buyer, kecocokan qty/MOQ) menghasilkan GO / TRY / NO-GO.

---

## 8. Daftar Dokumen Pendukung

| Dokumen | Fungsi |
|---|---|
| Price List AP Boots (Apr 2026) | Harga resmi dan batas bawah internal |
| T&C Sales & Distribution (ID/EN, revisi 2024) | Aturan komersial distributor |
| T&C General EN/ID | Versi ringkas T&C |
| Guideline Surat Menyurat + SOP Kode Dokumen | Format dokumen, kode, template |
| New Business Model Indo Sukses Semesta | Blueprint model B (export enabler) |
| Brosur AP Chef/Clog, AP Medic, AP Safety | Materi penjualan |

---

## 9. Inkonsistensi Data yang Perlu Diputuskan

Ini bagian paling penting. Dokumen ini hanya merangkum, tidak menyelesaikan konflik berikut.

| # | Isu | Sumber yang bertentangan | Risiko | Rekomendasi |
|---|---|---|---|---|
| 1 | **Aturan diskon distributor** | SOP: MOQ 50 box, diskon 10%/15%. T&C: ≤5% (<50 karton), ≤10% (≥50 karton). Susi: 10%/15% berdasarkan 100 pasang. Price list: Discount PT 15-40% per grup | Sales memberi diskon berbeda ke buyer berbeda; margin bocor | Tetapkan satu matriks diskon per kategori produk dan satu sumber kebenaran |
| 2 | **Margin target** | SOP: ≥15% distributor, ≥25% end user. T&C General: margin bersih 3-4%, ~2% untuk ≥150 karton | Cek approval otomatis (NOT APPROVED) bisa menolak hampir semua deal distributor | Bedakan margin kotor vs bersih dan tulis definisinya |
| 3 | **PPN** | T&C: harga belum termasuk PPN 11%. Susi: harga sudah termasuk PPN 12%. Business model: basis 11%. Status Non-PKP | Salah faktur dan salah hitung service charge | Konfirmasi tarif dan status PKP ke konsultan pajak, lalu seragamkan |
| 4 | **Kurs** | Price list: 17.500. Kebijakan Susi: 15.000 (IDR ke USD, bulatkan atas) | Harga USD di SPH berbeda dari price list | Putuskan kurs resmi SPH ekspor dan tulis di price list |
| 5 | **Window klaim** | SOP end user: 3 hari. T&C distributor: 2x24 jam | Sengketa klaim | Satu aturan per segmen |
| 6 | **Retur** | SOP: tidak ada retur. T&C: retur hanya cacat produksi | Sama | Selaraskan wording |
| 7 | **Nomor telepon** | Header surat +62 811 6964 7711; brosur +62 811 9496 7711 | Buyer menghubungi nomor yang salah | Verifikasi nomor resmi |
| 8 | **Klaim sertifikasi di brosur** | Brosur Medic dan Safety memuat badge "ISO & EN 20345"; prinsip kerja melarang klaim untuk Chef/Medic yang belum terverifikasi | Risiko klaim palsu di materi pemasaran | Minta konfirmasi tertulis WGI sebelum brosur disebar |
| 9 | **Material AP Chef/Medic** | Brosur: RubbeTech "100% PVC-free". Catatan Alibaba: AP Boots berbahan PVC | Spesifikasi di listing bisa salah | Konfirmasi material per lini ke WGI |
| 10 | **Harga Member Entry** | Draf sosialisasi: Rp5,5 juta. Dokumen baru: Rp5,8 juta | Sosialisasi ke BD memakai angka lama | Revisi bagian 6 dokumen model bisnis (sudah dikonfirmasi Rp5,8 juta) |
| 11 | **Margin Member Entry 16,4% vs target** | Dokumen model bisnis: margin paket terendah 16,4% | Di bawah threshold 20% yang ditargetkan | Tinjau ulang atau jadikan paket akuisisi, bukan paket profit |
| 12 | **Perhitungan ROI** | EBITDA dihitung dengan mengurangi hanya fixed OPEX Rp89,4 juta; lalu ROI dibagi total komitmen kas Rp123,28 juta (yang memuat fee Alibaba) | Basis tidak konsisten; fee Alibaba tidak terpotong dari laba | Hitung ulang dengan fee Alibaba sebagai biaya, dan uji sensitivitas jumlah deal |
| 13 | **Asumsi skenario moderat** | 4 deal Full Assistance (15%) dari order Rp300 juta + 6 deal member dalam 12 bulan; 20 member baru dalam setahun | Asumsi volume belum divalidasi | Mulai dari pilot 3-5 pabrik, ukur konversi dulu |
| 14 | **Kepatuhan TOS Alibaba (model B)** | Pabrik tanpa akun sendiri, HOTS supplier of record | Risiko akun GGS jika dianggap resale/third-party listing | Cek ke account manager Alibaba sebelum sosialisasi |
| 15 | **Kolom MoQ di price list kosong** | Price list | Tidak ada acuan resmi di file | Isi dengan MoQ per grup (6 dus min per Susi) |

---

## 10. Langkah Berikutnya (Usulan Prioritas)

| Prioritas | Aksi | Dampak |
|---|---|---|
| Tinggi | Satukan matriks diskon, margin, PPN, kurs menjadi satu dokumen "Pricing Policy v1" yang disetujui Miss Susi | Menghapus konflik #1-#4 |
| Tinggi | Dorong SPK notariil WGI | Membuka 3 kanal institusi sekaligus |
| Tinggi | Konfirmasi sertifikasi dan material per lini ke WGI sebelum brosur dan listing diperbarui | Menghindari klaim keliru |
| Sedang | Selesaikan checklist data pabrik dan scope of services per tier | Syarat mulai screening pabrik |
| Sedang | Validasi TOS Alibaba untuk model B | Mencegah risiko akun |
| Rendah | Hitung ulang model ROI dengan skenario konservatif/moderat/optimis | Dasar keputusan investasi Odoo |

*Dokumen ini disusun dari file proyek dan catatan kerja per 15 Oktober 2026. Angka dan aturan bisa berubah; verifikasi ke sumber asli sebelum dipakai di dokumen eksternal.*
