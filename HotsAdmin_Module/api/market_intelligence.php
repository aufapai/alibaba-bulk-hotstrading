<?php
/**
 * HOTS TRADING - 5 CONTINENTS MARKET INTELLIGENCE API
 * ====================================================
 * File: api/market_intelligence.php
 * Endpoint untuk intelijen pasar ekspor 5 benua (Q1-Q4) & 10 sudut industri Accio.
 * URL: https://admin.hotstrading.com/api/market_intelligence.php?quarter=Q4
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') {
    http_response_code(200);
    exit;
}

require_once __DIR__ . '/../src/AlibabaExportController.php';

use Hots\Export\AlibabaExportController;

$controller = new AlibabaExportController();
$quarter = isset($_GET['quarter']) ? strtoupper(trim($_GET['quarter'])) : 'Q4';

$intelligence = $controller->getMarketIntelligence($quarter);
$angles = $controller->getIndustryAngles();

$result = [
    'success' => true,
    'selected_quarter' => $quarter,
    'market_intelligence' => $intelligence['continents'],
    'industry_angles_matrix' => $angles
];

echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
