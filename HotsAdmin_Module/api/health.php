<?php
/**
 * HOTS TRADING - API HEALTH & DIAGNOSTIC ENDPOINT
 * ===============================================
 * File: api/health.php
 * GET /api/health.php
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

require_once __DIR__ . '/../src/Database.php';
require_once __DIR__ . '/../src/ForexService.php';

use Hots\Export\Database;
use Hots\Export\ForexService;

$cacheDir = __DIR__ . '/../cache';
$isCacheWritable = is_writable($cacheDir) || (!file_exists($cacheDir) && is_writable(dirname($cacheDir)));

$dbDiag = Database::getDiagnostics();
$forex = new ForexService();
$forexData = $forex->getRate();

$response = [
    'status' => 'healthy',
    'timestamp' => date('Y-m-d H:i:s T'),
    'environment' => [
        'php_version' => PHP_VERSION,
        'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? 'CLI/Unknown',
        'pdo_drivers' => PDO::getAvailableDrivers(),
        'cache_directory_writable' => $isCacheWritable
    ],
    'database' => $dbDiag,
    'forex_service' => [
        'status' => $forexData['success'] ? 'online' : 'fallback',
        'current_rate' => $forexData['rate'],
        'source' => $forexData['source'],
        'is_cached' => $forexData['is_cached'] ?? false
    ]
];

echo json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
