<?php
/**
 * HOTS TRADING - 4-SLOT AI PHOTO PROMPTS API
 * ==========================================
 * File: api/prompts.php
 * GET /api/prompts.php?product=AP+Max&sku=AP-MX-01&continent=Europe&country=Germany
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

require_once __DIR__ . '/../src/AlibabaExportController.php';

use Hots\Export\AlibabaExportController;

$controller = new AlibabaExportController();

$productName = $_GET['product'] ?? $_POST['product'] ?? 'AP Safety Boots';
$sku = $_GET['sku'] ?? $_POST['sku'] ?? 'APB-S5-01';
$continent = $_GET['continent'] ?? $_POST['continent'] ?? 'Europe';
$country = $_GET['country'] ?? $_POST['country'] ?? 'Germany';

$result = $controller->generate4SlotPhotoPrompts($productName, $sku, $continent, $country);

echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
