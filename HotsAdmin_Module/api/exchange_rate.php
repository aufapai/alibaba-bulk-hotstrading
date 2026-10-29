<?php
/**
 * HOTS TRADING - LIVE EXCHANGE RATE API
 * =====================================
 * File: api/exchange_rate.php
 * GET /api/exchange_rate.php?refresh=1
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

require_once __DIR__ . '/../src/ForexService.php';

use Hots\Export\ForexService;

$forceRefresh = isset($_GET['refresh']) && ($_GET['refresh'] === '1' || $_GET['refresh'] === 'true');
$service = new ForexService();
$result = $service->getRate($forceRefresh);

echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
