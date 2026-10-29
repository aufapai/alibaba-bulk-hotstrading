<?php
/**
 * HOTS TRADING - PRODUCTS CATALOG API
 * ===================================
 * File: api/products.php
 * GET /api/products.php?limit=50
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

require_once __DIR__ . '/../src/AlibabaExportController.php';

use Hots\Export\AlibabaExportController;

$controller = new AlibabaExportController();

$limit = isset($_GET['limit']) ? max(1, min(200, (int)$_GET['limit'])) : 50;
$products = $controller->getProductsCatalog($limit);

echo json_encode([
    'success' => true,
    'count' => count($products),
    'data' => $products
], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
