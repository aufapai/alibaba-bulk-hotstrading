-- ==============================================================================
-- HOTS TRADING - ALIBABA & GLOBAL B2B EXPORT MODULE
-- Target Database: MariaDB / MySQL (`hotj4796_hotstrading`) & SQLite Bridge
-- Compatibility: admin.hotstrading.com & cPanel MySQL 10.11+
-- File: sql/database_schema.sql
-- ==============================================================================

-- 1. Tabel Ekstensi Ekspor Alibaba (Relasi 1:1 atau 1:M dengan tabel `products`)
CREATE TABLE IF NOT EXISTS `alibaba_export_listings` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `product_id` INT(11) NOT NULL COMMENT 'FK ke tabel products.id',
  `sku` VARCHAR(50) NOT NULL COMMENT 'SKU unik produk',
  `alibaba_product_title` VARCHAR(128) NOT NULL COMMENT 'Judul listing Accio 2026 (Max 128 char)',
  `category_group` VARCHAR(100) NOT NULL DEFAULT 'AP Safety Boots',
  `target_continent` VARCHAR(50) NOT NULL DEFAULT 'Europe',
  `target_country` VARCHAR(50) DEFAULT 'Germany',
  `target_industry_angle` VARCHAR(100) DEFAULT 'Heavy Industrial & Construction',
  
  -- Primary & Long-tail Keywords (Accio 2026 SOP)
  `primary_keyword_1` VARCHAR(100) NOT NULL,
  `primary_keyword_2` VARCHAR(100) DEFAULT NULL,
  `primary_keyword_3` VARCHAR(100) DEFAULT NULL,
  `longtail_keywords` TEXT DEFAULT NULL COMMENT 'JSON array kata kunci turunan',
  
  -- Penetapan Harga & Valas
  `base_price_idr` DECIMAL(12,2) NOT NULL COMMENT 'Harga dasar domestik IDR',
  `fob_price_usd` DECIMAL(10,2) NOT NULL COMMENT 'Harga ekspor FOB Tanjung Priok USD',
  `exchange_rate_used` DECIMAL(10,2) NOT NULL DEFAULT 16250.00 COMMENT 'Kurs saat kalkulasi',
  
  -- Spesifikasi Kemasan Karton & Logistik
  `pairs_per_carton` INT(11) NOT NULL DEFAULT 12 COMMENT 'Isi pasang per master karton',
  `carton_price_usd` DECIMAL(10,2) NOT NULL,
  `carton_price_idr` DECIMAL(12,2) NOT NULL,
  `carton_dimensions_cm` VARCHAR(50) DEFAULT '60 x 40 x 40',
  `cbm_per_carton` DECIMAL(6,4) DEFAULT 0.0960,
  `gross_weight_kg_per_carton` DECIMAL(6,2) DEFAULT 20.40,
  `capacity_20ft_cartons` INT(11) DEFAULT 291,
  `capacity_40ft_hc_cartons` INT(11) DEFAULT 708,
  
  -- 4-Slot AI Photo Prompts (Google Flow / Nano Banana SOP)
  `prompt_slot_1_hero` TEXT DEFAULT NULL COMMENT '3/4 upright view, pure white background RGB 255,255,255',
  `prompt_slot_2_side` TEXT DEFAULT NULL COMMENT '90-degree clean side profile view',
  `prompt_slot_3_tread` TEXT DEFAULT NULL COMMENT 'Outsole cleats & mud release grooves pattern',
  `prompt_slot_4_contextual` TEXT DEFAULT NULL COMMENT 'In-use working environment disesuaikan target negara',
  
  -- URL Gambar Terkurasi & Bersih (Anti-Gagal Upload)
  `image_slot_1` VARCHAR(500) DEFAULT NULL,
  `image_slot_2` VARCHAR(500) DEFAULT NULL,
  `image_slot_3` VARCHAR(500) DEFAULT NULL,
  `image_slot_4` VARCHAR(500) DEFAULT NULL,
  `image_slot_5` VARCHAR(500) DEFAULT NULL,
  `image_slot_6` VARCHAR(500) DEFAULT NULL,
  
  -- Status Sinkronisasi
  `export_status` ENUM('DRAFT', 'OPTIMIZED', 'READY_FOR_UPLOAD', 'UPLOADED', 'ISSUE') NOT NULL DEFAULT 'DRAFT',
  `last_error_message` TEXT DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_alibaba_sku` (`sku`),
  KEY `idx_alibaba_product_id` (`product_id`),
  CONSTRAINT `fk_alibaba_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Tabel Aturan Market Intelligence Kontinental Bulanan/Kuartalan
CREATE TABLE IF NOT EXISTS `alibaba_market_rules` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `continent` VARCHAR(50) NOT NULL,
  `top_countries` TEXT NOT NULL COMMENT 'JSON array negara target',
  `quarter` VARCHAR(10) NOT NULL COMMENT 'Q1, Q2, Q3, Q4',
  `seasonal_demand_trigger` VARCHAR(255) NOT NULL,
  `recommended_angle` VARCHAR(100) NOT NULL,
  `mandatory_certifications` VARCHAR(255) NOT NULL,
  `recommended_keywords` TEXT NOT NULL COMMENT 'JSON array',
  `is_active` TINYINT(1) DEFAULT 1,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_cont_quarter` (`continent`, `quarter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Tabel Log Audit Kegagalan & Pemulihan Bulk Upload Alibaba
CREATE TABLE IF NOT EXISTS `alibaba_upload_audits` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `batch_id` VARCHAR(100) NOT NULL COMMENT 'Contoh: 29229346989_377707',
  `sku` VARCHAR(50) NOT NULL,
  `error_code` VARCHAR(50) NOT NULL COMMENT 'IMAGE_DATA_ISSUE, PRODUCT_DELETED, dll',
  `raw_error_message` TEXT NOT NULL,
  `failed_image_url` TEXT DEFAULT NULL,
  `resolved_image_url` TEXT DEFAULT NULL,
  `resolution_source` VARCHAR(50) DEFAULT NULL COMMENT 'blibli_cdn, photobank, lazada_cdn',
  `status` ENUM('PENDING', 'RESOLVED', 'MANUAL_ATTENTION') DEFAULT 'RESOLVED',
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_audit_batch` (`batch_id`),
  KEY `idx_audit_sku` (`sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. View Terpadu Ringkasan Produk Sistem + Data Ekspor Alibaba
CREATE OR REPLACE VIEW `v_alibaba_product_catalog` AS
SELECT 
    p.id AS system_product_id,
    p.product_code AS system_sku,
    p.name AS product_name,
    p.category AS system_category,
    p.base_price AS price_idr,
    p.image_url AS system_image_url,
    p.status AS system_status,
    a.alibaba_product_title,
    a.target_continent,
    a.fob_price_usd,
    a.carton_price_usd,
    a.cbm_per_carton,
    a.export_status
FROM `products` p
LEFT JOIN `alibaba_export_listings` a ON p.id = a.product_id;
