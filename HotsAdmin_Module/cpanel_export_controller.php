<?php
/**
 * HOTS TRADING - B2B EXPORT MODULE CONTROLLER
 * ===========================================
 * Namespace: Hots\Export
 * Target: cPanel MariaDB / MySQL System Integration (`admin.hotstrading.com`)
 */

namespace Hots\Export;

use PDO;
use Exception;

class AlibabaExportController
{
    private $pdo;
    private $forexCachePath;

    public function __construct(?PDO $pdo = null)
    {
        $this->forexCachePath = __DIR__ . '/forex_cache.json';

        if ($pdo) {
            $this->pdo = $pdo;
        } else {
            $host = getenv('DB_HOST') ?: 'localhost';
            $dbname = getenv('DB_DATABASE') ?: 'hotj4796_hotstrading';
            $user = getenv('DB_USERNAME') ?: 'hotj4796_user';
            $pass = getenv('DB_PASSWORD') ?: '';

            try {
                $this->pdo = new PDO("mysql:host={$host};dbname={$dbname};charset=utf8mb4", $user, $pass, [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
                ]);
            } catch (Exception $e) {
                // Graceful fallback if offline
                $this->pdo = null;
            }
        }
    }

    /**
     * Mengambil kurs live USD/IDR dari API pasar valas publik dengan caching 30 menit.
     */
    public function getLiveExchangeRate(): array
    {
        if (file_exists($this->forexCachePath) && (time() - filemtime($this->forexCachePath) < 1800)) {
            $cached = json_decode(file_get_contents($this->forexCachePath), true);
            if (!empty($cached['rate'])) return $cached;
        }

        $endpoints = [
            "https://api.exchangerate-api.com/v4/latest/USD",
            "https://open.er-api.com/v6/latest/USD"
        ];

        foreach ($endpoints as $url) {
            $ctx = stream_context_create(["http" => ["timeout" => 3, "header" => "User-Agent: HOTS-Admin/2.0\r\n"]]);
            $raw = @file_get_contents($url, false, $ctx);
            if ($raw) {
                $data = json_decode($raw, true);
                if (!empty($data['rates']['IDR'])) {
                    $payload = [
                        'rate' => (float)$data['rates']['IDR'],
                        'source' => 'Live Google / Forex Market Sync',
                        'updated_at' => date('Y-m-d H:i:s')
                    ];
                    @file_put_contents($this->forexCachePath, json_encode($payload));
                    return $payload;
                }
            }
        }

        return [
            'rate' => 16250.00,
            'source' => 'Fallback Market Baseline',
            'updated_at' => date('Y-m-d H:i:s')
        ];
    }

    /**
     * Kalkulasi komprehensif kemasan karton, CBM, muatan kontainer, dan skema fee HOTS.
     */
    public function calculateCartonMetrics(float $usd = 0.0, float $idr = 0.0, int $pairs = 12, ?float $customRate = null): array
    {
        $forex = $this->getLiveExchangeRate();
        $rate = ($customRate && $customRate > 1000) ? $customRate : $forex['rate'];

        if ($usd > 0) {
            $calcIdr = round($usd * $rate);
        } else {
            $calcIdr = $idr > 0 ? $idr : 85000.0;
            $usd = round($calcIdr / $rate, 2);
        }

        $cartonUsd = round($usd * $pairs, 2);
        $cartonIdr = round($calcIdr * $pairs);

        // Standar volume dimensi karton alas kaki (60 x 40 x 40 cm = 0.096 m3)
        $cbm = ($pairs <= 12) ? 0.096 : (($pairs <= 18) ? 0.120 : 0.146);
        $grossWeightKg = round($pairs * 1.7, 1);

        // Kapasitas muat kontainer (20ft = 28 CBM volume efektif, 40ft HC = 68 CBM volume efektif)
        $cap20ftCtns = (int)(28.0 / $cbm);
        $cap40ftCtns = (int)(68.0 / $cbm);

        return [
            'success' => true,
            'unit_price_usd' => $usd,
            'unit_price_idr' => $calcIdr,
            'carton_price_usd' => $cartonUsd,
            'carton_price_idr' => $cartonIdr,
            'pairs_per_carton' => $pairs,
            'specs' => [
                'cbm_per_carton' => $cbm,
                'carton_dimensions_cm' => '60 x 40 x 40 cm',
                'gross_weight_kg_per_carton' => $grossWeightKg
            ],
            'container_capacity' => [
                'container_20ft_cartons' => $cap20ftCtns,
                'container_20ft_pairs' => $cap20ftCtns * $pairs,
                'container_40ft_hc_cartons' => $cap40ftCtns,
                'container_40ft_hc_pairs' => $cap40ftCtns * $pairs
            ],
            'hots_export_charges' => [
                'member_regular_2pct' => [
                    'rate' => '2.0%',
                    'fee_per_pair_usd' => round($usd * 0.02, 3),
                    'fee_per_pair_idr' => round($calcIdr * 0.02)
                ],
                'non_member_mandiri_5pct' => [
                    'rate' => '5.0%',
                    'fee_per_pair_usd' => round($usd * 0.05, 3),
                    'fee_per_pair_idr' => round($calcIdr * 0.05)
                ],
                'full_assistance_15pct' => [
                    'rate' => '15.0%',
                    'fee_per_pair_usd' => round($usd * 0.15, 3),
                    'fee_per_pair_idr' => round($calcIdr * 0.15)
                ]
            ],
            'forex' => [
                'usd_idr_rate' => $rate,
                'source' => $forex['source']
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
            'slot_1_hero' => "Using the attached reference photos, create a professional e-commerce product photo of the exact same {$productName} (SKU: {$sku}). Keep the product exactly identical to the reference: same silhouette, material texture, sole cleats, and brand marking. Single product, 3/4 front view standing upright, centered, occupying 85% of frame. Pure white seamless background (RGB 255,255,255), crisp studio lighting with subtle natural contact shadow only. Square 1:1, sharp focus, 1600x1600. No promotional overlays, no text, no props.",
            'slot_2_side' => "Using the attached reference photos, create a product photograph of the exact same {$productName} from a clean 90-degree side profile view. Maintain exact proportions, shaft height, and heel curve. Pure white seamless background (RGB 255,255,255), even studio lighting, centered, occupying 85% of frame, subtle natural ground shadow. Square 1:1, sharp focus, zero text or logos.",
            'slot_3_tread' => "Using the attached reference photos, create a product photograph of the exact same {$productName} showing the bottom outsole tread pattern and anti-slip cleat structure. Show high detail of deep mud-release grooves and slip-resistant rubber texture. Pure white background (RGB 255,255,255), professional product studio lighting. Square 1:1, sharp focus.",
            'slot_4_contextual' => "Using the attached reference photos, create a realistic commercial contextual in-use photograph of the exact same {$productName} worn by an adult worker in {$scene}. Ground-level camera angle focusing on the boots in authentic working conditions. Natural realistic lighting, believable environmental texture, true-to-life colors. Square 1:1, cinematic high resolution. No artificial text or platform badges."
        ];
    }
}
