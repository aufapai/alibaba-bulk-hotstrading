<?php
/**
 * HOTS TRADING - ALIBABA LISTING MASTER GENERATOR API
 * ====================================================
 * Endpoint untuk menghasilkan listing produk Alibaba lengkap sesuai standar Gold Supplier:
 * - SEO Keyword Research (Primary, Secondary, Long-tail, Intent)
 * - 5 Title Candidates (Maks 128 karakter) & Selected Title
 * - Product Story, Advantages (USPs), Applications & Customization Matrix
 * - Technical Specification Sheet & Packaging Logistics
 * - 15 B2B Buyer FAQs & Call To Actions
 * - Description Builder V6 HTML (Strict Alibaba Compatible)
 * - Baris Data 57-Kolom Resmi Alibaba Bulk Upload Template
 * 
 * URL: https://admin.hotstrading.com/api/generate_alibaba_listing.php?sku=APB-001
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') {
    http_response_code(200);
    exit;
}

require_once __DIR__ . '/../src/AlibabaExportController.php';

use Hots\Export\AlibabaExportController;

$controller = new AlibabaExportController();

// Mengambil parameter baik dari GET, POST form, atau JSON body
$input = $_GET;
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST') {
    $raw = file_get_contents('php://input');
    $jsonData = json_decode($raw, true);
    if (is_array($jsonData)) {
        $input = array_merge($input, $jsonData);
    } else {
        $input = array_merge($input, $_POST);
    }
}

// Pastikan minimal ada SKU atau data dasar
if (empty($input['sku']) && empty($input['model'])) {
    $input['sku'] = 'APB-001';
}

$listing = $controller->generateAlibabaFullListing($input);

echo json_encode($listing, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
