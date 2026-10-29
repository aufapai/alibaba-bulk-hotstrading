<?php
/**
 * HOTS TRADING - ALIBABA 57-COLUMN BULK EXPORT GENERATOR
 * =======================================================
 * Endpoint untuk men-download file CSV 57-kolom resmi Alibaba Bulk Upload:
 * - Format: Standard Alibaba Default Template (57 Columns)
 * - Encoding: UTF-8 dengan BOM (kompatibel penuh dengan Microsoft Excel)
 * - Output: Langsung memicu prompt download di browser jika format=csv (default)
 * 
 * URL Contoh:
 * - Download CSV Seluruh Katalog: https://admin.hotstrading.com/api/export_alibaba_bulk.php
 * - Download CSV SKU Tertentu: https://admin.hotstrading.com/api/export_alibaba_bulk.php?skus=APB-001,APB-016
 * - Mode JSON: https://admin.hotstrading.com/api/export_alibaba_bulk.php?format=json
 */

require_once __DIR__ . '/../src/AlibabaExportController.php';

use Hots\Export\AlibabaExportController;

$controller = new AlibabaExportController();

$format = strtolower(trim($_GET['format'] ?? 'csv'));
$country = trim($_GET['country'] ?? 'Global');
$limit = isset($_GET['limit']) ? max(1, min(200, (int)$_GET['limit'])) : 50;

$skus = [];
if (!empty($_GET['skus'])) {
    $skus = array_values(array_filter(array_map('trim', explode(',', $_GET['skus']))));
} elseif (!empty($_GET['sku'])) {
    $skus = [trim($_GET['sku'])];
}

if ($format === 'json') {
    header('Content-Type: application/json; charset=utf-8');
    header('Access-Control-Allow-Origin: *');

    $headers = $controller->get57ColumnsHeader();
    $rows = [];
    if (!empty($skus)) {
        foreach ($skus as $s) {
            $l = $controller->generateAlibabaFullListing(['sku' => $s, 'destination_country' => $country]);
            $rows[] = $l['bulk_upload_57_columns_row'];
        }
    } else {
        $catalog = $controller->getProductsCatalog($limit);
        foreach ($catalog as $p) {
            $s = $p['product_code'] ?? ($p['sku'] ?? 'APB-001');
            $l = $controller->generateAlibabaFullListing([
                'sku' => $s,
                'model' => $p['name'] ?? $p['product_title'] ?? 'AP Boots',
                'base_price_idr' => $p['base_price'] ?? $p['price_idr'] ?? 115000,
                'destination_country' => $country,
                'images' => !empty($p['image_url']) ? [$p['image_url']] : []
            ]);
            $rows[] = $l['bulk_upload_57_columns_row'];
        }
    }

    echo json_encode([
        'success' => true,
        'format' => 'json',
        'columns_count' => count($headers),
        'total_rows' => count($rows),
        'headers' => $headers,
        'rows' => $rows
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
    exit;
}

// Default: Direct File Download as CSV (57 Kolom)
$csvData = $controller->exportAlibabaBulkCsv($skus, $country, $limit);
$filename = 'Alibaba_Bulk_Upload_Export_' . date('Ymd_His') . '.csv';

header('Content-Type: text/csv; charset=UTF-8');
header('Content-Disposition: attachment; filename="' . $filename . '"');
header('Content-Length: ' . strlen($csvData));
header('Pragma: no-cache');
header('Expires: 0');

echo $csvData;
exit;
