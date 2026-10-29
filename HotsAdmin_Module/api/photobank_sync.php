<?php
/**
 * HOTS TRADING - PHOTOBANK SYNCHRONIZATION API
 * ============================================
 * File: api/photobank_sync.php
 * Endpoint untuk memonitor status sinkronisasi folder Photobank dan manifest CSV.
 * URL: https://admin.hotstrading.com/api/photobank_sync.php
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

require_once __DIR__ . '/../src/AlibabaExportController.php';

use Hots\Export\AlibabaExportController;

$controller = new AlibabaExportController();
$summary = $controller->getPhotobankSyncSummary();

echo json_encode($summary, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
