<?php
/**
 * HOTS TRADING - FLOW MCP PRODUCT JOBS API
 * =========================================
 * File: api/flow_jobs.php
 * Endpoint untuk menyajikan 424 AI Photo Generation jobs ke frontend / AI Agent.
 * URL: https://admin.hotstrading.com/api/flow_jobs.php?sku=APB-016&limit=10
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

require_once __DIR__ . '/../src/AlibabaExportController.php';

use Hots\Export\AlibabaExportController;

$controller = new AlibabaExportController();

$sku = isset($_GET['sku']) && trim($_GET['sku']) !== '' ? trim($_GET['sku']) : null;
$limit = isset($_GET['limit']) ? max(1, min(450, (int)$_GET['limit'])) : 50;

$result = $controller->getFlowJobsSummary($sku, $limit);

echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
