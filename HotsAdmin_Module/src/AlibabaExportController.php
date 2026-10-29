<?php
/**
 * HOTS TRADING - B2B EXPORT MODULE CONTROLLER
 * ===========================================
 * File: src/AlibabaExportController.php
 * Target: cPanel MariaDB / MySQL System Integration (`admin.hotstrading.com`)
 */

namespace Hots\Export;

use PDO;
use Exception;

require_once __DIR__ . '/Database.php';
require_once __DIR__ . '/ForexService.php';

class AlibabaExportController
{
    private ?PDO $pdo;
    private ForexService $forexService;
    private array $packagingConfig;
    private array $feeConfig;

    public function __construct(?PDO $pdo = null)
    {
        $configFile = dirname(__DIR__) . '/config/config.php';
        $appConfig = file_exists($configFile) ? require $configFile : [];

        $this->packagingConfig = $appConfig['packaging'] ?? [
            'default_pairs_per_carton' => 12,
            'carton_dimensions_cm' => '60 x 40 x 40 cm',
            'cbm_standard_12pairs' => 0.096,
            'container_20ft_effective_cbm' => 28.0,
            'container_40ft_hc_effective_cbm' => 68.0,
            'gross_weight_multiplier_per_pair' => 1.7
        ];

        $this->feeConfig = $appConfig['fees'] ?? [
            'member_regular' => 0.02,
            'non_member_mandiri' => 0.05,
            'full_assistance' => 0.15
        ];

        $this->pdo = $pdo ?? Database::getConnection();
        $this->forexService = new ForexService($appConfig['forex'] ?? null);
    }

    /**
     * Mengambil kurs live USD/IDR dari ForexService.
     */
    public function getLiveExchangeRate(bool $forceRefresh = false): array
    {
        return $this->forexService->getRate($forceRefresh);
    }

    /**
     * Kalkulasi kemasan karton, CBM, kapasitas kontainer 20ft & 40ft HC, dan fee HOTS.
     */
    public function calculateCartonMetrics(float $usd = 0.0, float $idr = 0.0, int $pairs = 12, ?float $customRate = null): array
    {
        $pairs = $pairs > 0 ? $pairs : $this->packagingConfig['default_pairs_per_carton'];
        $forex = $this->getLiveExchangeRate();
        $rate = ($customRate && $customRate > 1000) ? $customRate : (float)$forex['rate'];

        if ($usd > 0) {
            $calcIdr = round($usd * $rate);
        } else {
            $calcIdr = $idr > 0 ? $idr : 85000.0;
            $usd = round($calcIdr / $rate, 2);
        }

        $cartonUsd = round($usd * $pairs, 2);
        $cartonIdr = round($calcIdr * $pairs);

        // Volume kubikasi CBM (60 x 40 x 40 cm = 0.096 m3 per 12 pasang)
        $cbm = ($pairs <= 12) ? 0.0960 : (($pairs <= 18) ? 0.1200 : round(0.0960 * ($pairs / 12), 4));
        $grossWeightKg = round($pairs * $this->packagingConfig['gross_weight_multiplier_per_pair'], 1);

        $effective20ft = $this->packagingConfig['container_20ft_effective_cbm'];
        $effective40ft = $this->packagingConfig['container_40ft_hc_effective_cbm'];

        $cap20ftCtns = (int)($effective20ft / $cbm);
        $cap40ftCtns = (int)($effective40ft / $cbm);

        $memberFeePct = $this->feeConfig['member_regular'];
        $nonMemberFeePct = $this->feeConfig['non_member_mandiri'];
        $fullFeePct = $this->feeConfig['full_assistance'];

        return [
            'success' => true,
            'unit_price_usd' => $usd,
            'unit_price_idr' => $calcIdr,
            'carton_price_usd' => $cartonUsd,
            'carton_price_idr' => $cartonIdr,
            'pairs_per_carton' => $pairs,
            'specs' => [
                'cbm_per_carton' => $cbm,
                'carton_dimensions_cm' => $this->packagingConfig['carton_dimensions_cm'],
                'gross_weight_kg_per_carton' => $grossWeightKg
            ],
            'container_capacity' => [
                'container_20ft_cartons' => $cap20ftCtns,
                'container_20ft_pairs' => $cap20ftCtns * $pairs,
                'container_40ft_hc_cartons' => $cap40ftCtns,
                'container_40ft_hc_pairs' => $cap40ftCtns * $pairs
            ],
            'hots_export_charges' => [
                'member_regular' => [
                    'rate' => ($memberFeePct * 100) . '%',
                    'fee_per_pair_usd' => round($usd * $memberFeePct, 3),
                    'fee_per_pair_idr' => round($calcIdr * $memberFeePct)
                ],
                'non_member_mandiri' => [
                    'rate' => ($nonMemberFeePct * 100) . '%',
                    'fee_per_pair_usd' => round($usd * $nonMemberFeePct, 3),
                    'fee_per_pair_idr' => round($calcIdr * $nonMemberFeePct)
                ],
                'full_assistance' => [
                    'rate' => ($fullFeePct * 100) . '%',
                    'fee_per_pair_usd' => round($usd * $fullFeePct, 3),
                    'fee_per_pair_idr' => round($calcIdr * $fullFeePct)
                ]
            ],
            'forex' => [
                'usd_idr_rate' => $rate,
                'source' => $forex['source'],
                'is_cached' => $forex['is_cached'] ?? false
            ]
        ];
    }

    /**
     * Menghasilkan prompt foto 4-slot standar Alibaba Photo Guide disesuaikan konteks negara tujuan.
     */
    public function generate4SlotPhotoPrompts(string $productName, string $sku, string $continent = 'Europe', string $country = 'Germany'): array
    {
        $sceneMap = [
            'Europe' => "a European industrial construction site in Germany on a wet cold autumn morning with steel beams and yellow safety tape",
            'North America' => "a North American civil engineering worksite in Texas with concrete structures and heavy machinery in outdoor daylight",
            'Southeast Asia' => "a tropical oil palm plantation in Malaysia with muddy terrain and puddles during monsoon rain",
            'Middle East' => "a modern luxury hotel culinary preparation center in Abu Dhabi with slip-resistant hygienic flooring",
            'Oceania' => "an Australian civil construction worksite and mining facility under clear outdoor daylight"
        ];

        $scene = $sceneMap[$continent] ?? $sceneMap['Europe'];

        return [
            'success' => true,
            'product_name' => $productName,
            'sku' => $sku,
            'target_continent' => $continent,
            'target_country' => $country,
            'prompts' => [
                'slot_1_hero' => "Using the attached reference photos, create a professional e-commerce product photo of the exact same {$productName} (SKU: {$sku}). Keep the product exactly identical to the reference: same silhouette, material texture, sole cleats, and brand marking. Single product, 3/4 front view standing upright, centered, occupying 85% of frame. Pure white seamless background (RGB 255,255,255), crisp studio lighting with subtle natural contact shadow only. Square 1:1, sharp focus, 1600x1600. No promotional overlays, no text, no props.",
                'slot_2_side' => "Using the attached reference photos, create a product photograph of the exact same {$productName} from a clean 90-degree side profile view. Maintain exact proportions, shaft height, and heel curve. Pure white seamless background (RGB 255,255,255), even studio lighting, centered, occupying 85% of frame, subtle natural ground shadow. Square 1:1, sharp focus, zero text or logos.",
                'slot_3_tread' => "Using the attached reference photos, create a product photograph of the exact same {$productName} showing the bottom outsole tread pattern and anti-slip cleat structure. Show high detail of deep mud-release grooves and slip-resistant rubber texture. Pure white background (RGB 255,255,255), professional product studio lighting. Square 1:1, sharp focus.",
                'slot_4_contextual' => "Using the attached reference photos, create a realistic commercial contextual in-use photograph of the exact same {$productName} worn by an adult worker in {$scene}. Ground-level camera angle focusing on the boots in authentic working conditions. Natural realistic lighting, believable environmental texture, true-to-life colors. Square 1:1, cinematic high resolution. No artificial text or platform badges."
            ]
        ];
    }

    /**
     * Mengambil daftar produk dari database sistem (MySQL atau SQLite) dengan fallback sample.
     */
    public function getProductsCatalog(int $limit = 50): array
    {
        $products = [];
        if ($this->pdo) {
            try {
                // Check if products table exists
                $stmt = $this->pdo->query("SELECT id, product_code, name, description, category, base_price, image_url, images, moq, status FROM products ORDER BY id DESC LIMIT {$limit}");
                $products = $stmt->fetchAll();
            } catch (Exception $e) {
                // If table columns differ (e.g. SQLite alibaba_master products table)
                try {
                    $stmt = $this->pdo->query("SELECT id, sku AS product_code, product_title AS name, category, price_idr AS base_price, image_1 AS image_url, status FROM products ORDER BY id DESC LIMIT {$limit}");
                    $products = $stmt->fetchAll();
                } catch (Exception $sqle) {
                    $products = [];
                }
            }
        }

        // If no products in DB yet, provide curated AP Boots sample fixtures for testing
        if (empty($products)) {
            $products = $this->getMockSampleProducts();
        }

        return $products;
    }

    public function getMockSampleProducts(): array
    {
        return [
            [
                'id' => 1,
                'product_code' => 'AP-MX-01',
                'name' => 'AP Max Safety Boots',
                'category' => 'Safety Footwear',
                'base_price' => 311000,
                'image_url' => 'https://hotstrading.com/backend/uploads/img_69b103b6d13604.65623585.webp',
                'status' => 'APPROVED',
                'description' => 'EN 20345 Steel Toe Cap 200J Heavy Industrial Safety Boots'
            ],
            [
                'id' => 2,
                'product_code' => 'APB-S5-03',
                'name' => 'AP Boots Safety S5 Yellow',
                'category' => 'Safety Footwear',
                'base_price' => 288000,
                'image_url' => 'https://hotstrading.com/backend/uploads/img_69b103892830b6.06120358.webp',
                'status' => 'APPROVED',
                'description' => 'Steel Toe + Steel Midsole + 3M Scotchlite Reflective Strip'
            ],
            [
                'id' => 3,
                'product_code' => 'AP-MD-01',
                'name' => 'AP Medic Hospital & Lab',
                'category' => 'Medical & Hygienic',
                'base_price' => 344000,
                'image_url' => 'https://hotstrading.com/backend/uploads/img_69b1040d6a9f04.41646303.webp',
                'status' => 'APPROVED',
                'description' => 'Rubbertech Anti-Microbial Autoclave Resistant 120°C'
            ],
            [
                'id' => 4,
                'product_code' => 'APB-CF-01',
                'name' => 'AP Chef Professional Kitchen Clogs',
                'category' => 'HORECA Footwear',
                'base_price' => 125000,
                'image_url' => 'https://hotstrading.com/backend/uploads/img_69b1040d6a9f04.41646303.webp',
                'status' => 'APPROVED',
                'description' => 'Oil & Grease Resistant Outsole with Ergonomic Insole'
            ],
            [
                'id' => 5,
                'product_code' => 'AP-AB-01',
                'name' => 'AP All Bike Commuter Shoes',
                'category' => 'Casual & Biker',
                'base_price' => 63000,
                'image_url' => 'https://hotstrading.com/backend/uploads/img_69b103e26a3455.45462166.webp',
                'status' => 'APPROVED',
                'description' => 'Waterproof Commuter Shoes with Aerodynamic Air Vents'
            ]
        ];
    }

    /**
     * Mendapatkan ringkasan sinkronisasi folder Photobank dan manifest CSV.
     */
    public function getPhotobankSyncSummary(): array
    {
        $projectRoot = dirname(dirname(__DIR__));
        $photobankDir = $projectRoot . '/Output/Photobank_Siap_Upload';
        $manifestPath = $photobankDir . '/DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv';

        $categories = [
            '01_Safety_Boots' => ['name' => 'AP Safety Boots', 'count' => 0],
            '02_Terra_Series' => ['name' => 'AP Terra Series', 'count' => 0],
            '03_Orca_Series' => ['name' => 'AP Orca Series', 'count' => 0],
            '04_Chef_Series' => ['name' => 'AP Chef Series', 'count' => 0],
            '05_Medic_Series' => ['name' => 'AP Medic Series', 'count' => 0],
            '06_Biker_Casual' => ['name' => 'AP Biker & Casual', 'count' => 0],
            '07_Classic_Boots' => ['name' => 'AP Classic Boots', 'count' => 0],
            '08_Kids_Boots' => ['name' => 'AP Kids Boots', 'count' => 0],
            '09_Sandals_Clogs' => ['name' => 'AP Sandals & Clogs', 'count' => 0],
            '10_Kasual_Sneakers' => ['name' => 'AP Kasual Sneakers', 'count' => 0],
            '11_General_Lifestyle_Boots' => ['name' => 'General & Lifestyle', 'count' => 0],
        ];

        $totalFiles = 0;
        if (is_dir($photobankDir)) {
            foreach ($categories as $catFolder => &$meta) {
                $subDir = $photobankDir . '/' . $catFolder;
                if (is_dir($subDir)) {
                    $files = array_diff(scandir($subDir), ['.', '..']);
                    $cnt = 0;
                    foreach ($files as $f) {
                        if (preg_match('/\.(webp|jpg|jpeg|png)$/i', $f)) {
                            $cnt++;
                        }
                    }
                    $meta['count'] = $cnt;
                    $totalFiles += $cnt;
                }
            }
            unset($meta);
        }

        $manifestEntries = 0;
        if (file_exists($manifestPath)) {
            $lines = file($manifestPath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            $manifestEntries = max(0, count($lines) - 1);
        }

        return [
            'success' => true,
            'photobank_dir_exists' => is_dir($photobankDir),
            'manifest_exists' => file_exists($manifestPath),
            'total_files_in_folders' => $totalFiles,
            'manifest_recorded_entries' => $manifestEntries,
            'categories' => $categories,
            'target_url' => 'https://admin.hotstrading.com/photo-bank',
            'last_sync_timestamp' => date('Y-m-d H:i:s')
        ];
    }

    /**
     * Mengambil daftar job Flow MCP dari file JSON yang dihasilkan oleh Product Input.
     */
    public function getFlowJobsSummary(?string $skuFilter = null, int $limit = 50): array
    {
        $projectRoot = dirname(dirname(__DIR__));
        $jsonFile = $projectRoot . '/Output/flow_product_input_jobs.json';

        if (!file_exists($jsonFile)) {
            return [
                'success' => false,
                'message' => 'File flow_product_input_jobs.json belum diekspor. Jalankan python run_flow_photobank.py --export-json.',
                'total_jobs' => 0,
                'jobs' => []
            ];
        }

        $raw = file_get_contents($jsonFile);
        $data = json_decode($raw, true) ?? [];
        $allJobs = $data['jobs'] ?? [];

        if ($skuFilter) {
            $allJobs = array_filter($allJobs, function ($j) use ($skuFilter) {
                return stripos($j['sku'] ?? '', $skuFilter) !== false || stripos($j['product_name'] ?? '', $skuFilter) !== false;
            });
            $allJobs = array_values($allJobs);
        }

        $limitedJobs = array_slice($allJobs, 0, $limit);

        return [
            'success' => true,
            'total_jobs_in_catalog' => $data['total_jobs'] ?? count($allJobs),
            'total_products' => $data['total_products'] ?? 0,
            'returned_count' => count($limitedJobs),
            'filter_sku' => $skuFilter,
            'jobs' => $limitedJobs
        ];
    }

    /**
     * Intelijen pasar 5 benua (Eropa, Amerika, ASEAN, Timur Tengah, Oseania) berdasarkan kuartal.
     */
    public function getMarketIntelligence(string $quarter = 'Q4'): array
    {
        $intelligence = [
            'Europe' => [
                'continent' => 'Europe',
                'top_countries' => ['Germany', 'United Kingdom', 'Netherlands', 'France', 'Poland'],
                'quarter' => $quarter,
                'seasonal_demand_trigger' => 'Late Autumn rain, early frost & wet mud operations. Year-end PPE procurement.',
                'recommended_angle' => 'Civil Construction',
                'certifications' => 'CE EN ISO 20345 (S4/S5), Oeko-Tex Standard 100',
                'recommended_keywords' => ['safety boots S5', 'waterproof work boots', 'steel toe safety boots', 'EN 20345 boots'],
                'recommended_skus' => ['APB-016', 'APB-019', 'APB-015']
            ],
            'North America' => [
                'continent' => 'North America',
                'top_countries' => ['United States', 'Canada', 'Mexico'],
                'quarter' => $quarter,
                'seasonal_demand_trigger' => 'Pre-winter storm preparation, outdoor construction foundations & logistics.',
                'recommended_angle' => 'Civil Construction',
                'certifications' => 'ASTM F2413-18, OSHA Standard Compliance',
                'recommended_keywords' => ['industrial rubber boots', 'steel toe work boots', 'mud boots waterproof', 'heavy duty rain boots'],
                'recommended_skus' => ['APB-016', 'APB-024', 'APB-007']
            ],
            'Southeast Asia' => [
                'continent' => 'Southeast Asia',
                'top_countries' => ['Malaysia', 'Thailand', 'Philippines', 'Vietnam', 'Singapore'],
                'quarter' => $quarter,
                'seasonal_demand_trigger' => 'Peak monsoon tropical rainy season & palm oil plantation mud terrain.',
                'recommended_angle' => 'Agriculture & Farming',
                'certifications' => 'SNI (Standar Nasional Indonesia), TKDN > 50%',
                'recommended_keywords' => ['waterproof rubber boots', 'anti slip boots', 'plantation boots', 'heavy duty pvc boots'],
                'recommended_skus' => ['APB-007', 'APB-008', 'APB-001', 'APB-006']
            ],
            'Middle East' => [
                'continent' => 'Middle East',
                'top_countries' => ['United Arab Emirates', 'Saudi Arabia', 'Qatar', 'Kuwait'],
                'quarter' => $quarter,
                'seasonal_demand_trigger' => 'Mega infrastructure foundations, oil & gas maintenance yards, luxury hotel kitchen prep.',
                'recommended_angle' => 'Oil & Gas Refinery',
                'certifications' => 'ISO 9001/14001, Heat Resistant Outsole Test',
                'recommended_keywords' => ['safety boots Dubai', 'oil resistant boots', 'slip resistant kitchen clogs', 'industrial gumboots'],
                'recommended_skus' => ['APB-021', 'APB-016', 'APB-022']
            ],
            'Oceania' => [
                'continent' => 'Oceania',
                'top_countries' => ['Australia', 'New Zealand'],
                'quarter' => $quarter,
                'seasonal_demand_trigger' => 'Spring transition to summer. Heavy agricultural harvesting & mining expeditions.',
                'recommended_angle' => 'Mining & Quarrying',
                'certifications' => 'AS/NZS 2210.3, Slip Resistance Class SRC',
                'recommended_keywords' => ['mining safety boots', 'agricultural work boots', 'gumboots steel cap', 'waterproof farm boots'],
                'recommended_skus' => ['APB-024', 'APB-016', 'APB-015']
            ]
        ];

        return [
            'success' => true,
            'quarter' => $quarter,
            'continents' => $intelligence
        ];
    }

    /**
     * 10 Matriks Sudut Industri (Accio Industry Angles)
     */
    public function getIndustryAngles(): array
    {
        return [
            ['id' => 'agriculture', 'name' => 'Agriculture & Farming', 'icon' => '🌾', 'focus' => 'Perkebunan kelapa sawit, sawah, kehutanan, tanah berlumpur', 'keywords' => ['plantation boots', 'farm gumboots', 'agricultural waterproof boots', 'anti-mud footwear']],
            ['id' => 'construction', 'name' => 'Civil Construction', 'icon' => '🏗️', 'focus' => 'Proyek gedung, pengecoran beton, jalan raya, infrastruktur', 'keywords' => ['construction safety boots', 'steel toe work boots', 'heavy duty rain boots', 'civil safety footwear']],
            ['id' => 'oil_gas', 'name' => 'Oil & Gas Refinery', 'icon' => '🛢️', 'focus' => 'Kilang minyak lepas pantai, instalasi petrochemical, anti-slip minyak', 'keywords' => ['oil resistant boots', 'petrochemical safety shoes', 'anti-chemical gumboots', 'fuel resistant footwear']],
            ['id' => 'mining', 'name' => 'Mining & Quarrying', 'icon' => '⛏️', 'focus' => 'Pertambangan batubara, nikel, emas, area berkerikil tajam', 'keywords' => ['mining safety boots', 'quarry heavy boots', 'high puncture resistant boots', 'durable gumboots']],
            ['id' => 'fishery', 'name' => 'Fishery & Seafood', 'icon' => '🐟', 'focus' => 'Dermaga perikanan, cold storage, pengolahan hasil laut', 'keywords' => ['fishery boots waterproof', 'commercial fish market boots', 'cold storage slip resistant', 'marine boots']],
            ['id' => 'hygiene', 'name' => 'Medical & Kitchen Hygiene', 'icon' => '👨‍🍳', 'focus' => 'Dapur restoran (HORECA), rumah sakit, cleanroom farmasi', 'keywords' => ['chef work shoes', 'hospital hygienic clogs', 'anti-bacterial footwear', 'kitchen slip resistant clogs']],
            ['id' => 'courier', 'name' => 'Motorcycle & Courier', 'icon' => '🏍️', 'focus' => 'Kurir ekspedisi, pengendara motor komuter saat musim hujan', 'keywords' => ['motorcycle riding boots', 'commuter rain shoes', 'courier waterproof boots', 'breathable riding shoes']],
            ['id' => 'chemical', 'name' => 'Chemical & Factory Manufacturing', 'icon' => '🧪', 'focus' => 'Pabrik manufaktur kimia, asam/alkali ringan, lantai pabrik basah', 'keywords' => ['chemical resistant boots', 'factory floor boots', 'anti-static work shoes', 'industrial protective footwear']],
            ['id' => 'wholesale', 'name' => 'Wholesale OEM Supply', 'icon' => '📦', 'focus' => 'Distributor B2B, importir kontainer, re-branding private label', 'keywords' => ['bulk safety boots', 'OEM factory boots wholesale', 'container load rain boots', 'factory direct supplier']],
            ['id' => 'rainwear', 'name' => 'All-Weather Rain Utility', 'icon' => '🌧️', 'focus' => 'Utilitas harian banjir, cuaca ekstrem, aktivitas outdoor', 'keywords' => ['all weather rain boots', 'waterproof utility boots', 'durable rain footwear', 'monsoon emergency boots']]
        ];
    }

    /**
     * Smart Top Pick Generator: Membuat paket rekomendasi ekspor siap listing B2B.
     */
    public function generateSmartTopPicks(string $country = 'Germany', string $angle = 'Civil Construction', int $limit = 3): array
    {
        $products = $this->getProductsCatalog(100);
        $rate = (float)$this->getLiveExchangeRate()['rate'];

        $selected = array_slice($products, 0, $limit);
        $packages = [];

        foreach ($selected as $idx => $p) {
            $sku = $p['product_code'] ?? ($p['sku'] ?? 'APB-' . str_pad($idx + 1, 3, '0', STR_PAD_LEFT));
            $name = $p['name'] ?? $p['product_title'];
            $baseIdr = (float)($p['base_price'] ?? 150000);
            $usd = round($baseIdr / $rate, 2);

            $metrics = $this->calculateCartonMetrics($usd, $baseIdr, 12, $rate);

            // Accio 2026 SEO Title
            $cleanName = preg_replace('/^(ap\s*boots?|sepatu\s*boot?)\s*/i', '', $name);
            $seoTitle = "AP Boots {$cleanName} Waterproof PVC Anti-Slip {$angle} Work Boots for {$country} Market";
            if (strlen($seoTitle) > 128) {
                $seoTitle = substr($seoTitle, 0, 125) . '...';
            }

            $packages[] = [
                'rank' => $idx + 1,
                'sku' => $sku,
                'original_name' => $name,
                'optimized_b2b_title' => $seoTitle,
                'destination_country' => $country,
                'industry_angle' => $angle,
                'category' => $p['category'] ?? "Shoes & Accessories > Men's Shoes > Boots",
                'image_url' => $p['image_url'] ?? '',
                'unit_fob_usd' => $usd,
                'unit_price_idr' => $baseIdr,
                'carton_price_usd' => $metrics['carton_price_usd'],
                'packaging' => [
                    'pairs_per_carton' => 12,
                    'cbm_per_carton' => 0.096,
                    'carton_20ft_capacity' => $metrics['container_capacity']['container_20ft_cartons'],
                    'carton_40ft_capacity' => $metrics['container_capacity']['container_40ft_hc_cartons']
                ],
                'tiered_pricing' => [
                    'tier_1_100_pairs' => $usd,
                    'tier_101_500_pairs' => round($usd * 0.95, 2),
                    'tier_501_1000_pairs' => round($usd * 0.90, 2),
                    'tier_above_1000_pairs' => round($usd * 0.85, 2)
                ],
                'hots_fee_estimate' => $metrics['hots_export_charges']['member_regular']
            ];
        }

        return [
            'success' => true,
            'destination_country' => $country,
            'industry_angle' => $angle,
            'total_generated' => count($packages),
            'exchange_rate_used' => $rate,
            'packages' => $packages
        ];
    }

    /**
     * Header resmi 57 kolom template bulk upload Alibaba 2026.
     */
    public function get57ColumnsHeader(): array
    {
        return [
            '* Product title',
            '* Product image 1',
            'Product image 2',
            'Product image 3',
            'Product image 4',
            'Product image 5',
            'Product image 6',
            'Product description',
            'Place of origin',
            'Brand name',
            'Category',
            'Product attribute name 1',
            'Product attribute value 1',
            'Product attribute name 2',
            'Product attribute value 2',
            'Product attribute name 3',
            'Product attribute value 3',
            'Product attribute name 4',
            'Product attribute value 4',
            'Product attribute name 5',
            'Product attribute value 5',
            'Sell product by',
            'Batch quantity',
            'Unit',
            'Currency',
            'Pricing type',
            'Inventory',
            'SPU ID (Model number)',
            'SKU code',
            'SKU pricing',
            'SKU attribute name 1',
            'SKU attribute value 1',
            'SKU attribute name 2',
            'SKU attribute value 2',
            'SKU attribute name 3',
            'SKU attribute value 3',
            'SKU attribute name 4',
            'SKU attribute value 4',
            'Tiered pricing 1',
            'MOQ 1',
            'Tiered pricing 2',
            'MOQ 2',
            'Tiered pricing 3',
            'MOQ 3',
            'Range pricing (Lower)',
            'Range pricing (Higher)',
            '* Gross weight (KG)',
            '* Shipping template name',
            '* Shipping quantity 1',
            '* Estimated shipping lead time 1',
            'Shipping quantity 2',
            'Estimated shipping lead time 2',
            'Shipping quantity 3',
            'Estimated shipping lead time 3',
            'Product size-Length',
            'Product size-Width',
            'Product size-Height'
        ];
    }

    /**
     * Generate Full Alibaba Listing sesuai schema Doc/ALIBABA_LISTING_GENERATOR_MASTER_PROMPT.md
     */
    public function generateAlibabaFullListing(array $input): array
    {
        $rate = (float)$this->getLiveExchangeRate()['rate'];

        // Ambil SKU dan coba cari dari database jika ada
        $sku = trim($input['sku'] ?? 'APB-001');
        $dbProduct = null;
        if ($this->pdo) {
            try {
                $stmt = $this->pdo->prepare("SELECT * FROM products WHERE product_code = ? OR sku = ? LIMIT 1");
                $stmt->execute([$sku, $sku]);
                $dbProduct = $stmt->fetch();
            } catch (Exception $e) {
                // Ignore
            }
        }

        // Resolusi input dasar
        $brand = !empty($input['brand']) ? trim($input['brand']) : 'AP Boots';
        $model = !empty($input['model']) ? trim($input['model']) : ($dbProduct['name'] ?? $dbProduct['product_title'] ?? 'Terra GP');
        $color = !empty($input['color']) ? trim($input['color']) : ($dbProduct['color'] ?? 'Black / Hi-Viz Yellow');
        $sizeRange = !empty($input['size_range']) ? trim($input['size_range']) : ($dbProduct['size_range'] ?? 'EU 37-46 (US 5-12)');
        $material = !empty($input['material']) ? trim($input['material']) : 'Virgin PVC / Natural Nitrile Rubber Blend';
        $certification = !empty($input['certification']) ? trim($input['certification']) : 'SNI 7079:2009, CE EN ISO 20345:2011, ISO 9001:2015';
        $origin = !empty($input['origin']) ? trim($input['origin']) : 'Indonesia';
        $moq = !empty($input['moq']) ? max(1, (int)$input['moq']) : 12;
        $oem = !empty($input['oem']) ? trim($input['oem']) : 'Available (Custom Logo, Colors & Master Carton)';
        $application = !empty($input['application']) ? trim($input['application']) : 'Civil Construction, Agriculture & Palm Oil, Heavy Mining, Oil & Gas, Food Hygiene';
        $destCountry = !empty($input['destination_country']) ? trim($input['destination_country']) : 'Germany';
        $industryAngle = !empty($input['industry_angle']) ? trim($input['industry_angle']) : 'Civil Construction';
        $category = !empty($input['category']) ? trim($input['category']) : "Shoes & Accessories > Men's Shoes > Boots";

        // Perhitungan Harga
        $baseIdr = isset($input['base_price_idr']) && (float)$input['base_price_idr'] > 0 
            ? (float)$input['base_price_idr'] 
            : (float)($dbProduct['base_price'] ?? $dbProduct['price_idr'] ?? 115000);
        
        $fobPriceUsd = isset($input['fob_price_usd']) && (float)$input['fob_price_usd'] > 0
            ? (float)$input['fob_price_usd']
            : round($baseIdr / $rate, 2);

        // Images handling (up to 6 unique images)
        $images = [];
        if (!empty($input['images']) && is_array($input['images'])) {
            $images = array_values(array_filter($input['images']));
        }
        if (empty($images) && $dbProduct) {
            foreach (['image_url', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6'] as $imgKey) {
                if (!empty($dbProduct[$imgKey]) && !in_array($dbProduct[$imgKey], $images)) {
                    $images[] = $dbProduct[$imgKey];
                }
            }
        }
        if (empty($images)) {
            $images = [
                'https://p16-images-comn-sg.tokopedia-static.net/tos-alisg-i-aphluv4xwc-sg/69b103b6d13604.65623585~tplv-aphluv4xwc-origin.webp',
                'https://p16-images-comn-sg.tokopedia-static.net/tos-alisg-i-aphluv4xwc-sg/69b103892830b6.06120358~tplv-aphluv4xwc-origin.webp'
            ];
        }

        // 1. SEO Keyword Research (sesuai spesifikasi)
        $seoKeywords = [
            'primary_keyword' => "waterproof pvc rubber work boots",
            'secondary_keywords' => [
                "industrial safety gumboots",
                "construction rain boots",
                "anti slip farm work boots",
                "factory export safety shoes",
                "oil resistant pvc boots",
                "indonesia rubber boot manufacturer"
            ],
            'long_tail_keywords' => [
                "heavy duty waterproof pvc boots for construction",
                "wholesale industrial pvc gumboots supplier indonesia",
                "anti penetration slip resistant work boots bulk order",
                "food hygiene waterproof kitchen boots CE certified",
                "oil and chemical resistant work boots factory direct"
            ],
            'buyer_intent_keywords' => ["buy factory direct", "wholesale rubber boots", "bulk order gumboots", "oem supplier indonesia"],
            'commercial_keywords' => ["OEM branding", "private label custom logo", "custom color mold boots"],
            'export_keywords' => ["Indonesia manufacturer exporter", "FOB Jakarta Tanjung Priok port", "container load boots"],
            'wholesale_keywords' => ["low MOQ 12 pairs", "20ft container load", "distributor tier pricing"]
        ];

        // 2. 5 Title Candidates (max 128 characters)
        $cleanModel = preg_replace('/^(ap\s*boots?|sepatu\s*boot?)\s*/i', '', $model);
        $titleCandidates = [
            "AP Boots {$cleanModel} Waterproof PVC Anti-Slip {$industryAngle} Work Boots for {$destCountry}",
            "Indonesia AP Boots {$cleanModel} Heavy Duty Industrial Safety Gumboots Factory Export",
            "AP Boots {$cleanModel} Oil Resistant Slip Resistant Work Boots Wholesale Manufacturer",
            "Wholesale AP Boots {$cleanModel} Protective Waterproof Footwear for {$industryAngle}",
            "AP Boots {$cleanModel} S5 Heavy Duty Work Rain Boots {$certification}"
        ];
        // Pastikan tidak melebihi 128 char
        foreach ($titleCandidates as &$tc) {
            $len = function_exists('mb_strlen') ? mb_strlen($tc) : strlen($tc);
            if ($len > 128) {
                $tc = (function_exists('mb_substr') ? mb_substr($tc, 0, 125) : substr($tc, 0, 125)) . '...';
            }
        }
        unset($tc);
        $selectedTitle = $titleCandidates[0];

        // 3. Product Advantages (USPs)
        $usps = [
            "100% Seamless Monolithic Injection Molding — Zero seam puncture or water leakage risk under extreme wet conditions.",
            "Heavy-Duty Flex Resistance — Surpasses 150,000 continuous flex cycles at -10°C to 50°C without cracking.",
            "High-Traction Deep Cleated Outsole — Self-cleaning mud-release lugs providing certified SRC anti-slip grip.",
            "Hydrocarbon & Mild Acid Resistance — Specialized PVC compound resists agricultural fertilizers, crude oil, and detergents.",
            "Ergonomic Ankle & Arch Support — Contoured footbed engineered to reduce worker fatigue over continuous 10-hour shifts.",
            "Direct Indonesian Factory Pricing — Zero middlemen, guaranteeing maximum profit margin for regional distributors."
        ];

        // 4. Technical Specifications Table Data
        $techSpecs = [
            'Product Name' => "AP Boots {$model}",
            'Brand' => $brand,
            'Model Number' => $model,
            'SPU ID / SKU' => $sku,
            'Outsole Material' => 'Virgin PVC / Heavy-Duty Nitrile Rubber Blend',
            'Upper Material' => '100% Waterproof Injection Molded PVC',
            'Lining Material' => 'Quick-Dry Polyester Fabric (Anti-Bacterial treated)',
            'Construction Method' => 'Direct Monolithic Injection Molding',
            'Available Colors' => $color,
            'Size Range' => $sizeRange,
            'Weight per Pair' => 'Approx. 1.65 - 1.75 kg (Size EU 42)',
            'Boot Height' => '36 - 38 cm (Knee High Protection)',
            'Certifications' => $certification,
            'Country of Origin' => $origin,
            'Primary Application' => $application,
            'Export Master Carton' => '12 Pairs per Heavy-Duty 5-Ply Corrugated Carton',
            'Carton Dimensions' => '60.0 x 42.0 x 38.0 cm (Volume: 0.096 CBM)',
            'MOQ' => "{$moq} Pairs / Standard Assorted Sizes",
            'OEM / ODM' => $oem,
            'Incoterms' => 'FOB Tanjung Priok (Jakarta) / Tanjung Perak (Surabaya), CIF, CFR',
            'HS Code' => '6401.92.00 (Waterproof Footwear with Outer Soles and Uppers of Plastics/Rubber)'
        ];

        // 5. Industry Applications
        $applications = [
            ['title' => 'Civil & Infrastructure Construction', 'desc' => 'Concrete casting, muddy trench excavation, road paving, and structural scaffolding.'],
            ['title' => 'Palm Oil & Tropical Agriculture', 'desc' => 'Harvester foot protection against palm frond thorns, waterlogged peatland, and marsh terrain.'],
            ['title' => 'Oil, Gas & Petrochemical Refineries', 'desc' => 'Refinery ground maintenance, chemical plant drainage, and oily machinery servicing.'],
            ['title' => 'Heavy Mining & Quarrying', 'desc' => 'Open-pit coal, nickel, and gravel quarries requiring tear-resistant and puncture-resistant soles.'],
            ['title' => 'Food Processing & Commercial Kitchens', 'desc' => 'Slaughterhouses, seafood cold storage, and hygienic food production lines.'],
            ['title' => 'All-Weather Emergency & Flood Response', 'desc' => 'Municipal drainage maintenance, urban flash floods, and monsoon rescue operations.']
        ];

        // 6. Packaging & Logistics
        $cartonCbm = 0.096;
        $cartonGrossWt = 20.4;
        $cap20ftCartons = 291;
        $cap40ftHcCartons = 708;
        $packaging = [
            'pairs_per_carton' => 12,
            'carton_length_cm' => 60.0,
            'carton_width_cm' => 42.0,
            'carton_height_cm' => 38.0,
            'cbm_per_carton' => $cartonCbm,
            'gross_weight_kg' => $cartonGrossWt,
            'net_weight_kg' => 19.2,
            'container_20ft_cartons' => $cap20ftCartons,
            'container_20ft_pairs' => $cap20ftCartons * 12,
            'container_40ft_hc_cartons' => $cap40ftHcCartons,
            'container_40ft_hc_pairs' => $cap40ftHcCartons * 12,
            'shipping_port' => 'Port of Tanjung Priok, Jakarta, Indonesia',
            'lead_time_days' => ['100_pairs' => 7, '500_pairs' => 14, '1000_pairs' => 30]
        ];

        // 7. Tiered FOB Pricing Matrix
        $pricingMatrix = [
            'tier_1' => ['qty' => '100 - 499 Pairs', 'fob_usd' => $fobPriceUsd, 'discount' => 'Base Export Price'],
            'tier_2' => ['qty' => '500 - 999 Pairs', 'fob_usd' => round($fobPriceUsd * 0.95, 2), 'discount' => '5% Volume Rebate'],
            'tier_3' => ['qty' => '1,000 - 2,999 Pairs', 'fob_usd' => round($fobPriceUsd * 0.90, 2), 'discount' => '10% Container Tier'],
            'tier_4' => ['qty' => '≥ 3,000 Pairs (FCL)', 'fob_usd' => round($fobPriceUsd * 0.85, 2), 'discount' => '15% Direct Factory VIP Tier']
        ];

        // 8. 15 B2B Buyer FAQs
        $faqs = [
            ['q' => 'Are you a direct footwear manufacturer or a trading company?', 'a' => 'We are PT Indo Sukses Semesta (HOTS Trading), the authorized global export partner for AP Boots Indonesia. Goods ship direct from our ISO 9001 certified manufacturing facilities.'],
            ['q' => 'What is the Minimum Order Quantity (MOQ)?', 'a' => 'Our standard MOQ is 12 pairs (1 master carton) for in-stock export models. For custom OEM branding or custom colors, the MOQ starts at 500 pairs.'],
            ['q' => 'Can you provide free samples for quality evaluation?', 'a' => 'Yes, 1 pair of sample boots can be provided. The sample is free, with express courier freight collected or reimbursed upon initial bulk container order.'],
            ['q' => 'What export certifications do your boots comply with?', 'a' => 'Our boots carry Indonesian National Standards (SNI 7079), select models hold CE EN ISO 20345:2011 S5 certificates, and all PVC materials comply with EU REACH requirements.'],
            ['q' => 'What sizes and color options are available?', 'a' => 'Standard export size range covers EU 37 to 46 (US Men 5 to 12). Custom pantone colors are available for bulk orders of 1,000 pairs or more.'],
            ['q' => 'Can we print our own brand logo on the boot or carton?', 'a' => 'Yes. We offer OEM silk-screen printing, thermal transfer logos, custom embossed badges, and fully customized master carton export packaging.'],
            ['q' => 'What are your standard export Incoterms and payment terms?', 'a' => 'We operate under FOB Tanjung Priok (Jakarta), CFR, or CIF worldwide. Payment is standard 30% T/T deposit upon order confirmation and 70% balance against Bill of Lading copy, or confirmed Irrevocable L/C at sight.'],
            ['q' => 'What is your average production lead time?', 'a' => 'For stock items: 5 to 7 business days. For 20ft/40ft container production orders: 20 to 30 calendar days upon deposit receipt.'],
            ['q' => 'How many pairs can fit into a 20ft and 40ft High Cube container?', 'a' => 'A standard 20ft container loads approximately 291 master cartons (3,492 pairs). A 40ft High Cube container loads up to 708 master cartons (8,496 pairs).'],
            ['q' => 'Are these boots chemical and oil resistant?', 'a' => 'Yes. Our specialized PVC/nitrile formulation provides certified resistance to animal fats, engine oils, common commercial detergents, and mild industrial acids.'],
            ['q' => 'How are the boots packaged for ocean freight?', 'a' => 'Each pair is packed in an individual protective polybag with size tags, then packed 12 pairs per heavy-duty 5-ply corrugated export master carton with desiccant silica gel packs.'],
            ['q' => 'What is the HS Code for customs import clearance?', 'a' => 'The international Harmonized System (HS) code is 6401.92.00 (Waterproof Footwear with Outer Soles and Uppers of Plastics/Rubber).'],
            ['q' => 'Do you support third-party pre-shipment inspections?', 'a' => 'Absolutely. We welcome SGS, Intertek, TÜV Rheinland, or your designated inspection agency to conduct full pre-shipment quality audits.'],
            ['q' => 'Can we mix different models and sizes within a single container order?', 'a' => 'Yes, multi-model consolidated container loading (LCL/FCL) is fully supported across our entire AP Boots catalog.'],
            ['q' => 'How do I start placing an order or requesting an official quotation?', 'a' => 'Simply click "Contact Supplier" or send an inquiry with your destination port, required quantities, and target delivery window. Our export team responds within 4 hours.']
        ];

        // 9. Call to Action (3 variants)
        $cta = [
            'short' => "Send your inquiry now for fast FOB Tanjung Priok quotation and immediate sample dispatch.",
            'standard' => "Partner directly with Indonesia's premier rubber & PVC footwear manufacturer. Inquire today for factory-direct bulk pricing, OEM customization catalogs, and full container logistics support.",
            'full' => "Ready to scale your industrial footwear distribution with verified high-margin AP Boots? Contact our Dedicated B2B Export Desk at PT Indo Sukses Semesta (admin@hotstrading.com). Guaranteed response within 4 hours with official proforma invoice and freight calculations."
        ];

        // 10. Generate Description Builder V6 HTML (Strict Alibaba Compatible)
        $v6Html = $this->buildDescriptionV6Html([
            'title' => $selectedTitle,
            'model' => $model,
            'brand' => $brand,
            'sku' => $sku,
            'dest_country' => $destCountry,
            'industry_angle' => $industryAngle,
            'images' => $images,
            'usps' => $usps,
            'tech_specs' => $techSpecs,
            'applications' => $applications,
            'packaging' => $packaging,
            'pricing_matrix' => $pricingMatrix,
            'faqs' => $faqs,
            'cta' => $cta
        ]);

        // 11. Official 57-Column Mapping Row
        $bulkRow = [
            $selectedTitle,                     // 1: * Product title
            $images[0] ?? '',                   // 2: * Product image 1
            $images[1] ?? '',                   // 3: Product image 2
            $images[2] ?? '',                   // 4: Product image 3
            $images[3] ?? '',                   // 5: Product image 4
            $images[4] ?? '',                   // 6: Product image 5
            $images[5] ?? '',                   // 7: Product image 6
            $v6Html,                            // 8: Product description
            $origin,                            // 9: Place of origin
            $brand,                             // 10: Brand name
            $category,                          // 11: Category
            "Outsole Material",                 // 12: Attribute name 1
            "PVC / Rubber",                     // 13: Attribute value 1
            "Upper Material",                   // 14: Attribute name 2
            "PVC",                              // 15: Attribute value 2
            "Season",                           // 16: Attribute name 3
            "All Seasons",                      // 17: Attribute value 3
            "Feature",                          // 18: Attribute name 4
            "100% Waterproof, Anti-Slip, Heavy-Duty", // 19: Attribute value 4
            "Gender",                           // 20: Attribute name 5
            "Men / Unisex",                     // 21: Attribute value 5
            "piece",                            // 22: Sell product by
            "",                                 // 23: Batch quantity
            "Pair/Pairs",                       // 24: Unit
            "USD",                              // 25: Currency
            "Tiered pricing",                   // 26: Pricing type
            5000,                               // 27: Inventory
            $model,                             // 28: SPU ID (Model number)
            $sku,                               // 29: SKU code
            $fobPriceUsd,                       // 30: SKU pricing
            "Color",                            // 31: SKU attribute name 1
            $color,                             // 32: SKU attribute value 1
            "Size",                             // 33: SKU attribute name 2
            $sizeRange,                         // 34: SKU attribute value 2
            "", "", "", "",                     // 35-38: Attribute 3 & 4
            $fobPriceUsd,                       // 39: Tiered pricing 1
            100,                                // 40: MOQ 1
            round($fobPriceUsd * 0.95, 2),      // 41: Tiered pricing 2
            500,                                // 42: MOQ 2
            round($fobPriceUsd * 0.90, 2),      // 43: Tiered pricing 3
            1000,                               // 44: MOQ 3
            round($fobPriceUsd * 0.85, 2),      // 45: Range pricing (Low)
            $fobPriceUsd,                       // 46: Range pricing (High)
            $cartonGrossWt / 12,                // 47: * Gross weight (KG) per pair
            "Default Shipping Template",        // 48: * Shipping template name
            100,                                // 49: Shipping quantity 1
            7,                                  // 50: Estimated shipping lead time 1
            500,                                // 51: Shipping quantity 2
            14,                                 // 52: Estimated shipping lead time 2
            1000,                               // 53: Shipping quantity 3
            30,                                 // 54: Estimated shipping lead time 3
            60.0,                               // 55: Product size-Length
            42.0,                               // 56: Product size-Width
            38.0                                // 57: Product size-Height
        ];

        return [
            'success' => true,
            'sku' => $sku,
            'brand' => $brand,
            'model' => $model,
            'fob_price_usd' => $fobPriceUsd,
            'base_price_idr' => $baseIdr,
            'exchange_rate_used' => $rate,
            'selected_title' => $selectedTitle,
            'title_candidates' => $titleCandidates,
            'seo_keywords' => $seoKeywords,
            'usps' => $usps,
            'technical_specifications' => $techSpecs,
            'applications' => $applications,
            'packaging' => $packaging,
            'pricing_matrix' => $pricingMatrix,
            'faqs' => $faqs,
            'cta' => $cta,
            'images' => $images,
            'description_v6_html' => $v6Html,
            'bulk_upload_57_columns_row' => $bulkRow
        ];
    }

    /**
     * Membangun HTML kompatibel 100% dengan Alibaba Description Builder V6.
     * Menggunakan strictly table, tr, td, font, b, p, br, img.
     */
    public function buildDescriptionV6Html(array $data): string
    {
        $title = htmlspecialchars($data['title'] ?? 'AP Boots Industrial Footwear');
        $model = htmlspecialchars($data['model'] ?? 'Terra GP');
        $sku = htmlspecialchars($data['sku'] ?? 'APB-001');
        $dest = htmlspecialchars($data['dest_country'] ?? 'Global');
        $angle = htmlspecialchars($data['industry_angle'] ?? 'Industrial & Safety');
        $images = $data['images'] ?? [];

        $html = '';

        // 1. Header Banner
        $html .= '<table width="100%" cellpadding="14" cellspacing="0" border="0" bgcolor="#0f172a">';
        $html .= '<tr><td align="center">';
        $html .= '<font color="#f59e0b" size="2"><b>★ PT INDO SUKSES SEMESTA • AP BOOTS OFFICIAL EXPORT ★</b></font><br>';
        $html .= '<font color="#ffffff" size="4"><b>' . $title . '</b></font><br>';
        $html .= '<font color="#94a3b8" size="2">Target Market: ' . $dest . ' | Industry Focus: ' . $angle . ' | Model: ' . $model . ' (' . $sku . ')</font>';
        $html .= '</td></tr></table><br>';

        // 2. Product Story & Overview
        $html .= '<table width="100%" cellpadding="10" cellspacing="0" border="0" bgcolor="#f8fafc" style="border: 1px solid #e2e8f0;">';
        $html .= '<tr><td>';
        $html .= '<p><font color="#0f172a" size="3"><b>ENGINEERED FOR HEAVY-DUTY INDUSTRIAL PERFORMANCE</b></font></p>';
        $html .= '<p><font color="#334155" size="2">AP Boots is Indonesia\'s #1 recognized safety & waterproof footwear brand with over 40 years of continuous manufacturing heritage. Specifically formulated with high-tensile virgin PVC and nitrile rubber compounds, model <b>' . $model . '</b> delivers superior chemical resistance, 100% seamless waterproof integrity, and heavy-duty puncture protection designed to satisfy demanding B2B safety standards in the <b>' . $dest . '</b> region.</font></p>';
        $html .= '</td></tr></table><br>';

        // 3. Product Gallery (Images)
        if (!empty($images)) {
            $html .= '<table width="100%" cellpadding="6" cellspacing="0" border="0">';
            $html .= '<tr><td colspan="2" bgcolor="#0f172a"><font color="#ffffff" size="3"><b>&nbsp;📸 OFFICIAL COMMERCIAL STUDIO PRODUCT GALLERY</b></font></td></tr>';
            $html .= '<tr>';
            $colCount = 0;
            foreach (array_slice($images, 0, 4) as $imgUrl) {
                if ($colCount > 0 && $colCount % 2 == 0) {
                    $html .= '</tr><tr>';
                }
                $html .= '<td width="50%" align="center" style="border: 1px solid #e2e8f0; padding: 10px;">';
                $html .= '<img src="' . htmlspecialchars($imgUrl) . '" width="100%" alt="' . $title . '" />';
                $html .= '</td>';
                $colCount++;
            }
            if ($colCount % 2 != 0) {
                $html .= '<td width="50%">&nbsp;</td>';
            }
            $html .= '</tr></table><br>';
        }

        // 4. Product Advantages (USPs)
        $html .= '<table width="100%" cellpadding="10" cellspacing="0" border="0" bgcolor="#ffffff" style="border: 1px solid #e2e8f0;">';
        $html .= '<tr><td bgcolor="#0f172a"><font color="#ffffff" size="3"><b>&nbsp;🏆 WHY GLOBAL BUYERS CHOOSE AP BOOTS ' . strtoupper($model) . '</b></font></td></tr>';
        $html .= '<tr><td><table width="100%" cellpadding="6" cellspacing="0" border="0">';
        foreach ($data['usps'] ?? [] as $usp) {
            $html .= '<tr>';
            $html .= '<td width="28" valign="top" align="center"><font color="#10b981" size="3"><b>✔</b></font></td>';
            $html .= '<td><font color="#334155" size="2">' . htmlspecialchars($usp) . '</font></td>';
            $html .= '</tr>';
        }
        $html .= '</table></td></tr></table><br>';

        // 5. Technical Specifications Table
        $html .= '<table width="100%" cellpadding="8" cellspacing="0" border="0" style="border: 1px solid #cbd5e1;">';
        $html .= '<tr><td colspan="2" bgcolor="#0f172a"><font color="#ffffff" size="3"><b>&nbsp;📋 TECHNICAL SPECIFICATIONS SHEET</b></font></td></tr>';
        $rowBg = false;
        foreach ($data['tech_specs'] ?? [] as $k => $v) {
            $bg = $rowBg ? '#f8fafc' : '#ffffff';
            $html .= '<tr bgcolor="' . $bg . '">';
            $html .= '<td width="35%" style="border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0;"><font color="#64748b" size="2"><b>' . htmlspecialchars($k) . '</b></font></td>';
            $html .= '<td width="65%" style="border-bottom: 1px solid #e2e8f0;"><font color="#0f172a" size="2">' . htmlspecialchars($v) . '</font></td>';
            $html .= '</tr>';
            $rowBg = !$rowBg;
        }
        $html .= '</table><br>';

        // 6. Industrial Applications
        $html .= '<table width="100%" cellpadding="8" cellspacing="0" border="0" style="border: 1px solid #cbd5e1;">';
        $html .= '<tr><td colspan="2" bgcolor="#0f172a"><font color="#ffffff" size="3"><b>&nbsp;🏭 RECOMMENDED INDUSTRIAL APPLICATIONS</b></font></td></tr>';
        $rowBg = false;
        foreach ($data['applications'] ?? [] as $app) {
            $bg = $rowBg ? '#f8fafc' : '#ffffff';
            $html .= '<tr bgcolor="' . $bg . '">';
            $html .= '<td width="35%" style="border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0;"><font color="#2563eb" size="2"><b>' . htmlspecialchars($app['title']) . '</b></font></td>';
            $html .= '<td width="65%" style="border-bottom: 1px solid #e2e8f0;"><font color="#475569" size="2">' . htmlspecialchars($app['desc']) . '</font></td>';
            $html .= '</tr>';
            $rowBg = !$rowBg;
        }
        $html .= '</table><br>';

        // 7. Packaging & Container Loading
        $p = $data['packaging'] ?? [];
        $html .= '<table width="100%" cellpadding="10" cellspacing="0" border="0" bgcolor="#f1f5f9" style="border: 1px solid #cbd5e1;">';
        $html .= '<tr><td bgcolor="#0f172a"><font color="#ffffff" size="3"><b>&nbsp;📦 EXPORT PACKAGING & CONTAINER LOGISTICS DATA</b></font></td></tr>';
        $html .= '<tr><td>';
        $html .= '<table width="100%" cellpadding="6" cellspacing="0" border="0">';
        $html .= '<tr>';
        $html .= '<td width="50%"><font color="#334155" size="2"><b>Master Carton Capacity:</b> 12 Pairs / Carton<br><b>Carton Dimensions:</b> 60.0 x 42.0 x 38.0 cm<br><b>Volume per Carton:</b> 0.096 CBM<br><b>Gross Weight:</b> 20.4 KG per Carton</font></td>';
        $html .= '<td width="50%"><font color="#334155" size="2"><b>20ft GP Container Load:</b> ~291 Cartons (3,492 Pairs)<br><b>40ft High Cube Container:</b> ~708 Cartons (8,496 Pairs)<br><b>Port of Loading:</b> Tanjung Priok, Jakarta, Indonesia<br><b>HS Code:</b> 6401.92.00</font></td>';
        $html .= '</tr></table>';
        $html .= '</td></tr></table><br>';

        // 8. Frequently Asked Questions (FAQ)
        $html .= '<table width="100%" cellpadding="10" cellspacing="0" border="0" style="border: 1px solid #cbd5e1;">';
        $html .= '<tr><td bgcolor="#0f172a"><font color="#ffffff" size="3"><b>&nbsp;❓ FREQUENTLY ASKED QUESTIONS (B2B BUYER FAQ)</b></font></td></tr>';
        $html .= '<tr><td><table width="100%" cellpadding="6" cellspacing="0" border="0">';
        foreach (array_slice($data['faqs'] ?? [], 0, 10) as $f) {
            $html .= '<tr><td>';
            $html .= '<p><font color="#0f172a" size="2"><b>Q: ' . htmlspecialchars($f['q']) . '</b></font><br>';
            $html .= '<font color="#475569" size="2">A: ' . htmlspecialchars($f['a']) . '</font></p>';
            $html .= '</td></tr>';
        }
        $html .= '</table></td></tr></table><br>';

        // 9. Call to Action / Footer Contact
        $html .= '<table width="100%" cellpadding="14" cellspacing="0" border="0" bgcolor="#0f172a">';
        $html .= '<tr><td align="center">';
        $html .= '<font color="#f59e0b" size="3"><b>READY TO PARTNER DIRECTLY WITH INDONESIA\'S LEADING BOOT FACTORY?</b></font><br><br>';
        $html .= '<font color="#ffffff" size="2">' . htmlspecialchars($data['cta']['standard'] ?? 'Contact our B2B Export team today.') . '</font><br><br>';
        $html .= '<table cellpadding="8" cellspacing="0" border="0" bgcolor="#f59e0b"><tr><td><font color="#0f172a" size="2"><b>▶ SEND INQUIRY / REQUEST PROFORMA INVOICE NOW</b></font></td></tr></table>';
        $html .= '</td></tr></table>';

        return $html;
    }

    /**
     * Export seluruh atau sebagian katalog ke CSV 57-kolom resmi Alibaba Bulk Upload.
     */
    public function exportAlibabaBulkCsv(array $skus = [], string $destinationCountry = 'Global', int $limit = 50): string
    {
        $headers = $this->get57ColumnsHeader();
        
        $output = fopen('php://temp', 'r+');
        // Tulis UTF-8 BOM agar Excel menampilkan aksen dan teks dengan benar
        fwrite($output, "\xEF\xBB\xBF");
        
        // Tulis baris header
        fputcsv($output, $headers);

        // Ambil produk
        $products = [];
        if (!empty($skus)) {
            foreach ($skus as $s) {
                $listing = $this->generateAlibabaFullListing([
                    'sku' => $s,
                    'destination_country' => $destinationCountry
                ]);
                fputcsv($output, $listing['bulk_upload_57_columns_row']);
            }
        } else {
            $catalog = $this->getProductsCatalog($limit);
            foreach ($catalog as $p) {
                $sku = $p['product_code'] ?? ($p['sku'] ?? 'APB-001');
                $listing = $this->generateAlibabaFullListing([
                    'sku' => $sku,
                    'model' => $p['name'] ?? $p['product_title'] ?? 'AP Boots',
                    'base_price_idr' => $p['base_price'] ?? $p['price_idr'] ?? 115000,
                    'destination_country' => $destinationCountry,
                    'images' => !empty($p['image_url']) ? [$p['image_url']] : []
                ]);
                fputcsv($output, $listing['bulk_upload_57_columns_row']);
            }
        }

        rewind($output);
        $csvContent = stream_get_contents($output);
        fclose($output);

        return $csvContent;
    }
}
