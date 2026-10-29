<?php
/**
 * HOTS TRADING - CARTON & PACKAGING METRICS API
 * =============================================
 * File: api/calculate_carton.php
 * GET /api/calculate_carton.php?usd=5.50&pairs=12
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

require_once __DIR__ . '/../src/AlibabaExportController.php';

use Hots\Export\AlibabaExportController;

$controller = new AlibabaExportController();

$usd = isset($_GET['usd']) ? (float)$_GET['usd'] : 0.0;
$idr = isset($_GET['idr']) ? (float)$_GET['idr'] : 0.0;
$pairs = isset($_GET['pairs']) ? (int)$_GET['pairs'] : 12;
$rate = isset($_GET['rate']) && (float)$_GET['rate'] > 1000 ? (float)$_GET['rate'] : null;

$metrics = $controller->calculateCartonMetrics($usd, $idr, $pairs, $rate);

echo json_encode($metrics, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
