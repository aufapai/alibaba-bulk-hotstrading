<?php
/**
 * HOTS TRADING - SMART TOP PICK EXPORT GENERATOR API
 * ===================================================
 * File: api/smart_top_picks.php
 * Endpoint untuk menghasilkan paket ekspor top rekomendasi siap listing B2B.
 * URL: https://admin.hotstrading.com/api/smart_top_picks.php?country=Germany&angle=Civil+Construction&limit=3
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

$country = isset($_GET['country']) && trim($_GET['country']) !== '' ? trim($_GET['country']) : 'Germany';
$angle = isset($_GET['angle']) && trim($_GET['angle']) !== '' ? trim($_GET['angle']) : 'Civil Construction';
$limit = isset($_GET['limit']) ? max(1, min(20, (int)$_GET['limit'])) : 3;

$result = $controller->generateSmartTopPicks($country, $angle, $limit);

echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
