<?php
/**
 * HOTS TRADING - B2B EXPORT MODULE & DEBUG DASHBOARD
 * ==================================================
 * Portal: https://admin.hotstrading.com/
 * File: index.php (Master Entrypoint & Debug UI)
 */

require_once __DIR__ . '/src/AlibabaExportController.php';
require_once __DIR__ . '/src/Database.php';

use Hots\Export\AlibabaExportController;
use Hots\Export\Database;

$controller = new AlibabaExportController();
$forex = $controller->getLiveExchangeRate();
$currentRate = (float)$forex['rate'];
$dbDiag = Database::getDiagnostics();
$products = $controller->getProductsCatalog(50);
$photobankSummary = $controller->getPhotobankSyncSummary();
$flowJobsSummary = $controller->getFlowJobsSummary(null, 5);
$marketIntel = $controller->getMarketIntelligence('Q4');
$industryAngles = $controller->getIndustryAngles();
$sampleTopPicks = $controller->generateSmartTopPicks('Germany', 'Civil Construction', 3);
$sampleListing = $controller->generateAlibabaFullListing(['sku' => 'APB-001', 'destination_country' => 'Germany', 'industry_angle' => 'Civil Construction']);
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HOTS Admin - B2B Alibaba Export Hub & Debug Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --hots-primary: #0f172a;
            --hots-dark: #070e1e;
            --hots-secondary: #f59e0b;
            --hots-secondary-hover: #d97706;
            --hots-bg: #f8fafc;
            --hots-card: #ffffff;
            --hots-border: #e2e8f0;
            --hots-text-main: #0f172a;
            --hots-text-muted: #64748b;
            --hots-success: #10b981;
            --hots-danger: #ef4444;
            --hots-info: #0284c7;
            --hots-purple: #8b5cf6;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            background: var(--hots-bg);
            color: var(--hots-text-main);
            line-height: 1.5;
        }

        /* Top Bar */
        .top-navbar {
            background: var(--hots-dark);
            color: #ffffff;
            padding: 14px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid var(--hots-secondary);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .top-navbar .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .top-navbar .brand-logo {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #f59e0b, #d97706);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            color: #fff;
            box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);
        }
        .top-navbar .brand-title {
            font-size: 1.15rem;
            font-weight: 800;
        }
        .top-navbar .brand-title span { color: var(--hots-secondary); }
        .top-navbar .brand-sub { font-size: 0.74rem; color: #94a3b8; }

        .badge-bar {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .rate-badge {
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.4);
            color: var(--hots-secondary);
            font-weight: 700;
            font-size: 0.82rem;
            padding: 6px 14px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .db-badge {
            font-size: 0.78rem;
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .db-badge.connected { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #10b981; }
        .db-badge.disconnected { background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #ef4444; }

        /* Container Layout */
        .main-container {
            max-width: 1440px;
            margin: 24px auto;
            padding: 0 24px;
        }

        /* Stat Grid */
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .stat-card {
            background: var(--hots-card);
            border: 1px solid var(--hots-border);
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            border-left: 4px solid var(--hots-secondary);
        }
        .stat-card.c-blue { border-left-color: var(--hots-info); }
        .stat-card.c-green { border-left-color: var(--hots-success); }
        .stat-card.c-purple { border-left-color: var(--hots-purple); }

        .stat-card .label { font-size: 0.76rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase; }
        .stat-card .val { font-size: 1.6rem; font-weight: 800; color: var(--hots-text-main); margin: 4px 0; }
        .stat-card .sub { font-size: 0.75rem; color: var(--hots-text-muted); }

        /* Navigation Tabs */
        .module-tabs {
            display: flex;
            gap: 8px;
            border-bottom: 2px solid var(--hots-border);
            margin-bottom: 24px;
            overflow-x: auto;
        }
        .module-tab {
            padding: 12px 20px;
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--hots-text-muted);
            background: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
        }
        .module-tab:hover { color: var(--hots-primary); }
        .module-tab.active {
            color: var(--hots-primary);
            border-bottom-color: var(--hots-secondary);
        }

        /* Card Panels */
        .panel {
            background: var(--hots-card);
            border: 1px solid var(--hots-border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
            display: none;
        }
        .panel.active { display: block; }

        .panel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 14px;
            border-bottom: 1px solid var(--hots-border);
        }
        .panel-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--hots-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Buttons & Forms */
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 16px;
            font-size: 0.84rem;
            font-weight: 700;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.15s ease;
        }
        .btn-primary { background: var(--hots-primary); color: #fff; }
        .btn-primary:hover { background: #1e293b; }
        .btn-amber { background: var(--hots-secondary); color: #fff; }
        .btn-amber:hover { background: var(--hots-secondary-hover); }
        .btn-secondary { background: #f1f5f9; color: var(--hots-text-main); border: 1px solid var(--hots-border); }
        .btn-secondary:hover { background: #e2e8f0; }

        .input-group {
            margin-bottom: 16px;
        }
        .input-group label {
            display: block;
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--hots-text-muted);
            margin-bottom: 6px;
            text-transform: uppercase;
        }
        .input-group input, .input-group select, .input-group textarea {
            width: 100%;
            padding: 10px 14px;
            border: 1px solid var(--hots-border);
            border-radius: 8px;
            font-size: 0.88rem;
            font-family: inherit;
        }
        .input-group input:focus, .input-group select:focus {
            outline: none;
            border-color: var(--hots-secondary);
        }

        /* Tables */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.84rem;
        }
        .data-table th {
            background: #f8fafc;
            padding: 12px 14px;
            font-weight: 700;
            color: var(--hots-text-muted);
            text-align: left;
            border-bottom: 2px solid var(--hots-border);
        }
        .data-table td {
            padding: 14px;
            border-bottom: 1px solid var(--hots-border);
            vertical-align: middle;
        }
        .data-table tr:hover { background: #f8fafc; }

        .thumb {
            width: 44px;
            height: 44px;
            object-fit: cover;
            border-radius: 8px;
            border: 1px solid var(--hots-border);
            background: #f8fafc;
        }

        .code-box {
            background: #0f172a;
            color: #38bdf8;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            padding: 16px;
            border-radius: 10px;
            overflow-x: auto;
            max-height: 380px;
            white-space: pre-wrap;
        }

        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        @media (max-width: 900px) {
            .grid-2 { grid-template-columns: 1fr; }
        }

        /* Smart Top Picks & Market Intel Styles */
        .filter-bar {
            background: #ffffff;
            border: 1px solid var(--hots-border);
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 24px;
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: flex-end;
        }
        .filter-bar .input-group {
            margin-bottom: 0;
            flex: 1;
            min-width: 180px;
        }
        .top-pick-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 20px;
        }
        .top-pick-card {
            background: #ffffff;
            border: 1px solid var(--hots-border);
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            display: flex;
            flex-direction: column;
        }
        .top-pick-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.06);
        }
        .top-pick-card-header {
            padding: 16px 20px;
            background: #f8fafc;
            border-bottom: 1px solid var(--hots-border);
            display: flex;
            gap: 14px;
            align-items: center;
        }
        .top-pick-thumb {
            width: 64px;
            height: 64px;
            object-fit: cover;
            border-radius: 10px;
            border: 1px solid var(--hots-border);
            background: #ffffff;
        }
        .top-pick-body {
            padding: 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        .price-tiers-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            background: #f8fafc;
            border: 1px solid var(--hots-border);
            border-radius: 10px;
            padding: 10px;
            text-align: center;
        }
        .tier-item .tier-qty {
            font-size: 0.68rem;
            font-weight: 700;
            color: var(--hots-text-muted);
            text-transform: uppercase;
        }
        .tier-item .tier-price {
            font-size: 0.92rem;
            font-weight: 800;
            color: #2563eb;
            margin-top: 2px;
        }
        .intel-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        .intel-card {
            background: #ffffff;
            border: 1px solid var(--hots-border);
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .intel-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--hots-border);
        }
        .quarter-tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .quarter-btn {
            padding: 8px 18px;
            border-radius: 20px;
            border: 1px solid var(--hots-border);
            background: #ffffff;
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--hots-text-muted);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .quarter-btn:hover {
            background: #f1f5f9;
        }
        .quarter-btn.active {
            background: var(--hots-primary);
            color: #ffffff;
            border-color: var(--hots-primary);
        }
        .tag-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
            background: #eff6ff;
            color: #1e40af;
            margin: 2px 4px 2px 0;
        }

        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }
        @media (max-width: 992px) {
            .grid-3 { grid-template-columns: 1fr; }
        }
        .sub-nav-tabs {
            display: flex;
            gap: 6px;
            border-bottom: 1px solid var(--hots-border);
            margin-bottom: 16px;
            overflow-x: auto;
        }
        .sub-nav-btn {
            padding: 8px 14px;
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--hots-text-muted);
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            cursor: pointer;
            white-space: nowrap;
        }
        .sub-nav-btn:hover { color: var(--hots-primary); }
        .sub-nav-btn.active {
            color: #2563eb;
            border-bottom-color: #2563eb;
        }
        .sub-panel { display: none; }
        .sub-panel.active { display: block; }
    </style>
</head>
<body>

    <!-- Top Navigation Bar -->
    <header class="top-navbar">
        <div class="brand">
            <div class="brand-logo">👢</div>
            <div>
                <div class="brand-title">HOTS <span>TRADING</span> B2B Export Module</div>
                <div class="brand-sub">Platform Integrasi Alibaba Gold Supplier & Multi-Marketplace • admin.hotstrading.com</div>
            </div>
        </div>
        <div class="badge-bar">
            <div class="rate-badge">
                <span>💵 Kurs Live:</span> 1 USD = Rp <?= number_format($currentRate, 2, ',', '.') ?>
            </div>
            <div class="db-badge <?= $dbDiag['connected'] ? 'connected' : 'disconnected' ?>">
                <span><?= $dbDiag['connected'] ? '🟢' : '🔴' ?></span>
                DB: <?= htmlspecialchars(strtoupper($dbDiag['driver'])) ?>
            </div>
            <a href="api/health.php" target="_blank" class="btn btn-secondary" style="font-size: 0.75rem; padding: 5px 10px;">
                🏥 Health Check
            </a>
        </div>
    </header>

    <div class="main-container">

        <!-- DB Status Banner -->
        <?php if (!$dbDiag['connected']): ?>
        <div style="background: #fffbeb; border: 1.5px solid #fde68a; border-radius: 12px; padding: 14px 18px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <strong style="color: #92400e;">ℹ️ Mode Debug Mandiri / Fallback Mock Aktif:</strong>
                <p style="font-size: 0.82rem; color: #78350f; margin-top: 2px;">
                    <?= htmlspecialchars($dbDiag['message']) ?> Database cPanel dapat dihubungkan melalui file <code>config/config.php</code> atau <code>.env</code>.
                </p>
            </div>
            <button class="btn btn-secondary" style="font-size: 0.75rem;" onclick="switchTab('transfer')">Lihat Panduan Setup</button>
        </div>
        <?php endif; ?>

        <!-- Stat Cards -->
        <div class="stat-grid">
            <div class="stat-card">
                <div class="label">Katalog Produk</div>
                <div class="val"><?= count($products) ?> SKU</div>
                <div class="sub">Tersedia untuk Ekspor Alibaba B2B</div>
            </div>
            <div class="stat-card c-blue">
                <div class="label">Kurs Valas Real-Time</div>
                <div class="val">Rp <?= number_format($currentRate, 0, ',', '.') ?></div>
                <div class="sub"><?= htmlspecialchars($forex['source']) ?></div>
            </div>
            <div class="stat-card c-green">
                <div class="label">Volume Standar Master Karton</div>
                <div class="val">0.096 CBM</div>
                <div class="sub">12 Pasang (60 x 40 x 40 cm)</div>
            </div>
            <div class="stat-card c-purple">
                <div class="label">Dukungan Kontinental</div>
                <div class="val">5 Benua</div>
                <div class="sub">Eropa, Amerika, ASEAN, Timur Tengah, Oseania</div>
            </div>
        </div>

        <!-- Module Tabs -->
        <div class="module-tabs">
            <button class="module-tab active" onclick="switchTab('catalog')">
                <span>📦</span> Katalog Produk
            </button>
            <button class="module-tab" onclick="switchTab('top-picks')">
                <span>⭐</span> Smart Top Pick Generator
            </button>
            <button class="module-tab" onclick="switchTab('intelligence')">
                <span>🌍</span> Intelijen Pasar 5 Benua
            </button>
            <button class="module-tab" onclick="switchTab('listing-generator')">
                <span>📤</span> Generator Listing & Bulk Export
            </button>
            <button class="module-tab" onclick="switchTab('calculator')">
                <span>🧮</span> Kalkulator Kemasan
            </button>
            <button class="module-tab" onclick="switchTab('prompts')">
                <span>🎯</span> Prompt Foto AI
            </button>
            <button class="module-tab" onclick="switchTab('photobank-sync')">
                <span>🔄</span> Sync Flow & Photobank
            </button>
            <button class="module-tab" onclick="switchTab('api-test')">
                <span>🛠️</span> API Debug Suite
            </button>
            <button class="module-tab" onclick="switchTab('transfer')">
                <span>📋</span> Checklist cPanel
            </button>
        </div>

        <!-- Tab 1: Product Catalog -->
        <div class="panel active" id="tab-catalog">
            <div class="panel-header">
                <div>
                    <h3 class="panel-title"><span>📦</span> Master Produk Siap Ekspor B2B</h3>
                    <p style="font-size: 0.8rem; color: var(--hots-text-muted); margin-top: 4px;">
                        Harga IDR otomatis dikonversikan ke estimasi harga FOB USD pelabuhan Tanjung Priok / Perak berdasarkan kurs live.
                    </p>
                </div>
                <div style="display: flex; gap: 10px;">
                    <button class="btn btn-secondary" onclick="window.location.reload()">🔄 Refresh</button>
                </div>
            </div>

            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 50px;">Foto</th>
                        <th>SKU Code</th>
                        <th>Nama Produk</th>
                        <th>Kategori</th>
                        <th>Harga Sistem (IDR)</th>
                        <th>Estimasi FOB (USD)</th>
                        <th>Carton USD (12 psg)</th>
                        <th>Status</th>
                        <th>Aksi</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($products as $p): 
                        $sku = htmlspecialchars($p['product_code'] ?? $p['sku'] ?? 'N/A');
                        $name = htmlspecialchars($p['name'] ?? $p['product_title'] ?? 'N/A');
                        $idr = (float)($p['base_price'] ?? $p['price_idr'] ?? 85000);
                        $usd = round($idr / $currentRate, 2);
                        $cartonUsd = round($usd * 12, 2);
                        $img = htmlspecialchars($p['image_url'] ?? $p['image_1'] ?? 'https://via.placeholder.com/44');
                        $status = htmlspecialchars($p['status'] ?? 'READY');
                    ?>
                    <tr>
                        <td><img src="<?= $img ?>" class="thumb" onerror="this.src='https://via.placeholder.com/44'"></td>
                        <td><strong><?= $sku ?></strong></td>
                        <td><strong><?= $name ?></strong></td>
                        <td><?= htmlspecialchars($p['category'] ?? 'Boots') ?></td>
                        <td style="font-weight: 700;">Rp <?= number_format($idr, 0, ',', '.') ?></td>
                        <td style="font-weight: 800; color: #2563eb;">$<?= number_format($usd, 2) ?></td>
                        <td style="font-weight: 700; color: #0f172a;">$<?= number_format($cartonUsd, 2) ?></td>
                        <td><span style="background: #ecfdf5; color: #047857; padding: 4px 8px; border-radius: 6px; font-weight: 700; font-size: 0.72rem;"><?= $status ?></span></td>
                        <td>
                            <button class="btn btn-secondary" style="font-size: 0.74rem; padding: 4px 8px;" onclick="loadCalculator(<?= $usd ?>, <?= $idr ?>, '<?= $sku ?>', '<?= addslashes($name) ?>')">
                                🧮 Hitung
                            </button>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>

        <!-- Tab: Smart Top Pick Generator -->
        <div class="panel" id="tab-top-picks">
            <div class="panel-header">
                <div>
                    <h3 class="panel-title"><span>⭐</span> Smart Top Pick Generator (Alibaba B2B Export)</h3>
                    <p style="font-size: 0.8rem; color: var(--hots-text-muted); margin-top: 4px;">
                        Kurasi produk ekspor otomatis berbasis regulasi negara tujuan, sudut industri Accio 2026, dan harga FOB kompetitif.
                    </p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn btn-secondary" onclick="copyAllTopPicksJson()">
                        <span>📋</span> Salin Semua JSON
                    </button>
                    <a href="api/smart_top_picks.php" target="_blank" class="btn btn-secondary">
                        <span>🔌</span> REST API
                    </a>
                </div>
            </div>

            <!-- Filter Controls Bar -->
            <div class="filter-bar">
                <div class="input-group">
                    <label>Negara Tujuan Ekspor</label>
                    <select id="tp-country">
                        <option value="Germany" selected>🇩🇪 Jerman (Eropa - CE / EN 20345)</option>
                        <option value="United States">🇺🇸 Amerika Serikat (ASTM F2413 / OSHA)</option>
                        <option value="Malaysia">🇲🇾 Malaysia (ASEAN - Sawit & Perkebunan)</option>
                        <option value="United Arab Emirates">🇦🇪 UAE / Dubai (Timur Tengah - Heat & Oil)</option>
                        <option value="Australia">🇦🇺 Australia (Oseania - Mining AS/NZS)</option>
                        <option value="United Kingdom">🇬🇧 Britania Raya (UKCA / S5 Safety)</option>
                        <option value="Singapore">🇸🇬 Singapura (Marine & Clean Logistics)</option>
                        <option value="Saudi Arabia">🇸🇦 Arab Saudi (SASO Standards)</option>
                        <option value="Japan">🇯🇵 Jepang (JIS T 8101 Compliance)</option>
                        <option value="Netherlands">🇳🇱 Belanda (Rotterdam Euro Port Hub)</option>
                    </select>
                </div>
                <div class="input-group">
                    <label>Sudut Industri (Accio 2026)</label>
                    <select id="tp-angle">
                        <option value="Civil Construction" selected>🏗️ Civil Construction</option>
                        <option value="Agriculture & Farming">🌾 Agriculture & Farming</option>
                        <option value="Oil & Gas Refinery">🛢️ Oil & Gas Refinery</option>
                        <option value="Mining & Quarrying">⛏️ Mining & Quarrying</option>
                        <option value="Fishery & Seafood">🐟 Fishery & Seafood</option>
                        <option value="Medical & Kitchen Hygiene">👨‍🍳 Medical & Kitchen Hygiene</option>
                        <option value="Motorcycle & Courier">🏍️ Motorcycle & Courier</option>
                        <option value="Chemical & Factory Manufacturing">🧪 Chemical & Factory</option>
                        <option value="Wholesale OEM Supply">📦 Wholesale OEM Supply</option>
                        <option value="All-Weather Rain Utility">🌧️ All-Weather Rain Utility</option>
                    </select>
                </div>
                <div class="input-group" style="max-width: 130px;">
                    <label>Jumlah Produk</label>
                    <select id="tp-limit">
                        <option value="3" selected>Top 3</option>
                        <option value="5">Top 5</option>
                        <option value="8">Top 8</option>
                        <option value="12">Top 12</option>
                    </select>
                </div>
                <div>
                    <button class="btn btn-amber" onclick="generateTopPicksWeb()" style="height: 42px;">
                        <span>⚡</span> Generate Paket Ekspor
                    </button>
                </div>
            </div>

            <!-- Status & Summary Indicator -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <div style="font-size: 0.85rem; color: #475569;">
                    Target: <strong id="tp-lbl-country" style="color: var(--hots-primary);">Germany</strong> • Sudut: <strong id="tp-lbl-angle" style="color: #2563eb;">Civil Construction</strong> • Total: <strong id="tp-lbl-count"><?= count($sampleTopPicks['packages'] ?? []) ?> Paket</strong>
                </div>
                <div style="font-size: 0.78rem; color: var(--hots-text-muted);">
                    Kurs Referensi: <strong>1 USD = Rp <?= number_format($currentRate, 0, ',', '.') ?></strong>
                </div>
            </div>

            <!-- Dynamic Top Pick Grid -->
            <div class="top-pick-grid" id="top-picks-results">
                <?php if (!empty($sampleTopPicks['packages'])): ?>
                    <?php foreach ($sampleTopPicks['packages'] as $pkg): ?>
                    <div class="top-pick-card">
                        <div class="top-pick-card-header">
                            <img src="<?= htmlspecialchars($pkg['image_url'] ?: 'https://via.placeholder.com/64') ?>" class="top-pick-thumb" onerror="this.src='https://via.placeholder.com/64'">
                            <div style="flex: 1; min-width: 0;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                    <span class="badge" style="background: #eff6ff; color: #1d4ed8; font-weight: 800; font-size: 0.72rem; padding: 2px 8px; border-radius: 4px;">
                                        #<?= $pkg['rank'] ?> • <?= htmlspecialchars($pkg['sku']) ?>
                                    </span>
                                    <span style="font-size: 0.72rem; font-weight: 700; color: #10b981; background: #ecfdf5; padding: 2px 6px; border-radius: 4px;">
                                        FOB $<?= number_format($pkg['unit_fob_usd'], 2) ?>
                                    </span>
                                </div>
                                <h4 style="font-size: 0.88rem; font-weight: 800; color: var(--hots-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                    <?= htmlspecialchars($pkg['original_name']) ?>
                                </h4>
                                <div style="font-size: 0.72rem; color: var(--hots-text-muted);">
                                    <?= htmlspecialchars($pkg['category']) ?>
                                </div>
                            </div>
                        </div>
                        <div class="top-pick-body">
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <span style="font-size: 0.72rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                                        Accio 2026 SEO Export Title
                                    </span>
                                    <button class="btn btn-secondary" style="font-size: 0.68rem; padding: 2px 8px;" onclick="copyTextDirect('<?= addslashes($pkg['optimized_b2b_title']) ?>')">
                                        Salin
                                    </button>
                                </div>
                                <div style="background: #f8fafc; border: 1px dashed var(--hots-border); border-radius: 8px; padding: 10px; font-size: 0.8rem; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                    <?= htmlspecialchars($pkg['optimized_b2b_title']) ?>
                                </div>
                            </div>

                            <!-- Tiered Pricing Matrix -->
                            <div>
                                <span style="font-size: 0.72rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
                                    Tiered FOB Pricing (USD / Pasang)
                                </span>
                                <div class="price-tiers-grid">
                                    <div class="tier-item">
                                        <div class="tier-qty">100 psg</div>
                                        <div class="tier-price">$<?= number_format($pkg['tiered_pricing']['tier_1_100_pairs'], 2) ?></div>
                                    </div>
                                    <div class="tier-item">
                                        <div class="tier-qty">500 psg</div>
                                        <div class="tier-price">$<?= number_format($pkg['tiered_pricing']['tier_101_500_pairs'], 2) ?></div>
                                    </div>
                                    <div class="tier-item">
                                        <div class="tier-qty">1.000 psg</div>
                                        <div class="tier-price">$<?= number_format($pkg['tiered_pricing']['tier_501_1000_pairs'], 2) ?></div>
                                    </div>
                                    <div class="tier-item">
                                        <div class="tier-qty">&gt;1.000 psg</div>
                                        <div class="tier-price" style="color: #059669;">$<?= number_format($pkg['tiered_pricing']['tier_above_1000_pairs'], 2) ?></div>
                                    </div>
                                </div>
                            </div>

                            <!-- Packaging & Logistics Specs -->
                            <div style="background: #f1f5f9; border-radius: 8px; padding: 10px 12px; font-size: 0.76rem; color: #334155; line-height: 1.6;">
                                <div style="display: flex; justify-content: space-between;">
                                    <span>Master Carton: <strong>12 Pasang ($<?= number_format($pkg['carton_price_usd'], 2) ?>)</strong></span>
                                    <span>Volume: <strong>0.096 CBM</strong></span>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                                    <span>Muatan 20ft: <strong><?= number_format($pkg['packaging']['carton_20ft_capacity']) ?> Karton</strong></span>
                                    <span>Muatan 40ft HC: <strong><?= number_format($pkg['packaging']['carton_40ft_capacity']) ?> Karton</strong></span>
                                </div>
                            </div>

                            <!-- Actions -->
                            <div style="display: flex; gap: 8px; margin-top: auto; padding-top: 8px;">
                                <button class="btn btn-secondary" style="flex: 1; font-size: 0.74rem; justify-content: center;" onclick="loadCalculator(<?= $pkg['unit_fob_usd'] ?>, <?= $pkg['unit_price_idr'] ?>, '<?= $pkg['sku'] ?>', '<?= addslashes($pkg['original_name']) ?>')">
                                    🧮 Hitung Karton
                                </button>
                                <button class="btn btn-primary" style="flex: 1; font-size: 0.74rem; justify-content: center;" onclick="copyTopPickJson(<?= htmlspecialchars(json_encode($pkg)) ?>)">
                                    📋 Salin Payload
                                </button>
                            </div>
                        </div>
                    </div>
                    <?php endforeach; ?>
                <?php endif; ?>
            </div>
        </div>

        <!-- Tab: Market Intelligence 5 Benua -->
        <div class="panel" id="tab-intelligence">
            <div class="panel-header">
                <div>
                    <h3 class="panel-title"><span>🌍</span> Intelijen Pasar 5 Benua & 10 Accio Industry Angles</h3>
                    <p style="font-size: 0.8rem; color: var(--hots-text-muted); margin-top: 4px;">
                        Panduan regulasi, tren musiman kuartal Q1-Q4, dan sudut penargetan buyer B2B global Alibaba 2026.
                    </p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <a href="api/market_intelligence.php?quarter=Q4" target="_blank" class="btn btn-secondary">
                        <span>🔌</span> Intel API
                    </a>
                </div>
            </div>

            <!-- Quarter Selector Tabs -->
            <div style="margin-bottom: 18px;">
                <span style="font-size: 0.78rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase; display: block; margin-bottom: 8px;">
                    Pilih Kuartal Musim Ekspor (Quarterly Seasonal Trigger):
                </span>
                <div class="quarter-tabs">
                    <button class="quarter-btn" onclick="changeQuarterIntel('Q1', this)">🌸 Q1 (Jan - Mar): Musim Dingin & Persiapan Konstruksi Musim Semi</button>
                    <button class="quarter-btn" onclick="changeQuarterIntel('Q2', this)">☀️ Q2 (Apr - Jun): Musim Panas & Pertanian / Industri Terbuka</button>
                    <button class="quarter-btn" onclick="changeQuarterIntel('Q3', this)">🍂 Q3 (Jul - Sep): Panen Raya & Persiapan Stok Akhir Tahun</button>
                    <button class="quarter-btn active" onclick="changeQuarterIntel('Q4', this)">❄️ Q4 (Okt - Des): Musim Hujan, Salju, Pergudangan & Logistik Global (Aktif)</button>
                </div>
            </div>

            <!-- 5 Continents Grid -->
            <h4 style="font-size: 0.95rem; font-weight: 800; color: var(--hots-primary); margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
                <span>🌐</span> Analisis Preferensi & Regulasi 5 Benua
            </h4>
            <div class="intel-grid" id="continents-grid">
                <?php if (!empty($marketIntel['continents'])): ?>
                    <?php 
                    $continentIcons = [
                        'Europe' => '🇪🇺',
                        'North America' => '🇺🇸',
                        'Southeast Asia' => '🌴',
                        'Middle East' => '🏜️',
                        'Oceania' => '🦘'
                    ];
                    foreach ($marketIntel['continents'] as $contKey => $c): 
                        $icon = $continentIcons[$contKey] ?? '🌍';
                    ?>
                    <div class="intel-card">
                        <div class="intel-card-header">
                            <div>
                                <span style="font-size: 1.3rem; margin-right: 6px;"><?= $icon ?></span>
                                <strong style="font-size: 0.95rem; color: var(--hots-primary);"><?= htmlspecialchars($c['continent']) ?></strong>
                            </div>
                            <span class="badge" style="background: #eff6ff; color: #1d4ed8; font-weight: 700; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">
                                <?= htmlspecialchars($c['recommended_angle']) ?>
                            </span>
                        </div>

                        <div style="font-size: 0.78rem; color: var(--hots-text-muted);">
                            <strong>Negara Kunci:</strong> <?= implode(', ', array_map('htmlspecialchars', $c['top_countries'] ?? [])) ?>
                        </div>

                        <div style="background: #f8fafc; border-left: 3px solid #2563eb; padding: 10px 12px; border-radius: 0 8px 8px 0; font-size: 0.8rem; color: #1e293b;">
                            <strong style="color: #2563eb; display: block; margin-bottom: 2px;">⚡ Pemicu Kebutuhan Musiman:</strong>
                            <?= htmlspecialchars($c['seasonal_demand_trigger']) ?>
                        </div>

                        <div style="font-size: 0.78rem;">
                            <strong style="color: var(--hots-text-main);">Regulasi & Sertifikasi:</strong><br>
                            <span class="tag-badge" style="background: #fef3c7; color: #92400e;">
                                📜 <?= htmlspecialchars($c['certifications']) ?>
                            </span>
                        </div>

                        <div style="font-size: 0.78rem;">
                            <strong style="color: var(--hots-text-main);">Kata Kunci Pencarian Buyer:</strong><br>
                            <div style="margin-top: 4px;">
                                <?php foreach ($c['recommended_keywords'] as $kw): ?>
                                    <span class="tag-badge">🔍 <?= htmlspecialchars($kw) ?></span>
                                <?php endforeach; ?>
                            </div>
                        </div>

                        <div style="font-size: 0.78rem; margin-top: auto; padding-top: 8px; border-top: 1px dashed var(--hots-border);">
                            <span style="color: var(--hots-text-muted);">Rekomendasi SKU AP Boots:</span>
                            <strong style="color: #059669;"><?= implode(', ', array_map('htmlspecialchars', $c['recommended_skus'] ?? [])) ?></strong>
                        </div>
                    </div>
                    <?php endforeach; ?>
                <?php endif; ?>
            </div>

            <!-- 10 Accio Industry Angles Section -->
            <div style="margin-top: 32px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <div>
                        <h4 style="font-size: 0.95rem; font-weight: 800; color: var(--hots-primary); display: flex; align-items: center; gap: 8px;">
                            <span>🎯</span> 10 Accio 2026 Industry Angles Matrix
                        </h4>
                        <p style="font-size: 0.78rem; color: var(--hots-text-muted); margin-top: 2px;">
                            Segmentasi vertikal industri untuk optimasi kata kunci dan klasifikasi produk pada algoritma Alibaba Accio AI.
                        </p>
                    </div>
                </div>

                <div class="grid-2">
                    <?php if (!empty($industryAngles)): ?>
                        <?php foreach ($industryAngles as $angle): ?>
                        <div style="background: #ffffff; border: 1px solid var(--hots-border); border-radius: 10px; padding: 14px; display: flex; gap: 12px; align-items: flex-start;">
                            <div style="width: 36px; height: 36px; border-radius: 8px; background: #f8fafc; border: 1px solid var(--hots-border); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0;">
                                <?= $angle['icon'] ?>
                            </div>
                            <div style="flex: 1; min-width: 0;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                    <strong style="font-size: 0.85rem; color: var(--hots-primary);"><?= htmlspecialchars($angle['name']) ?></strong>
                                    <span style="font-size: 0.7rem; color: var(--hots-text-muted); font-family: monospace;">#<?= htmlspecialchars($angle['id']) ?></span>
                                </div>
                                <p style="font-size: 0.78rem; color: #475569; margin-bottom: 6px;"><?= htmlspecialchars($angle['focus']) ?></p>
                                <div>
                                    <?php foreach (array_slice($angle['keywords'], 0, 3) as $kw): ?>
                                        <span class="tag-badge" style="font-size: 0.68rem; padding: 2px 6px;">🏷️ <?= htmlspecialchars($kw) ?></span>
                                    <?php endforeach; ?>
                                </div>
                            </div>
                        </div>
                        <?php endforeach; ?>
                    <?php endif; ?>
                </div>
            </div>
        </div>

        <!-- Tab: Alibaba Listing & Bulk Export Generator -->
        <div class="panel" id="tab-listing-generator">
            <div class="panel-header">
                <div>
                    <h3 class="panel-title"><span>📤</span> Alibaba Listing & Bulk Export Generator (57-Kolom & V6 HTML)</h3>
                    <p style="font-size: 0.8rem; color: var(--hots-text-muted); margin-top: 4px;">
                        Generator listing terverifikasi standar Gold Supplier & Description Builder V6 sesuai dokumen <code>Doc/ALIBABA_LISTING_GENERATOR_MASTER_PROMPT.md</code>.
                    </p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <a href="api/export_alibaba_bulk.php?format=csv" class="btn btn-amber">
                        <span>📥</span> Export Semua Produk (57-Kolom CSV)
                    </a>
                    <a href="api/generate_alibaba_listing.php?sku=APB-001" target="_blank" class="btn btn-secondary">
                        <span>🔌</span> JSON API
                    </a>
                </div>
            </div>

            <!-- Product Input Form (Sesuai schema ALIBABA_LISTING_GENERATOR_MASTER_PROMPT.md) -->
            <div style="background: #ffffff; border: 1px solid var(--hots-border); border-radius: 14px; padding: 20px; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid var(--hots-border);">
                    <h4 style="font-size: 0.92rem; font-weight: 800; color: var(--hots-primary); display: flex; align-items: center; gap: 8px;">
                        <span>📝</span> Input Data Produk (Manual atau Pilih dari Master SKU)
                    </h4>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 0.78rem; font-weight: 700; color: var(--hots-text-muted);">Muat Cepat:</span>
                        <select id="gen-sku-preset" onchange="loadPresetProduct(this.value)" style="padding: 6px 12px; border-radius: 8px; border: 1px solid var(--hots-border); font-size: 0.82rem; font-weight: 600;">
                            <?php foreach ($products as $pr): 
                                $s = $pr['product_code'] ?? $pr['sku'] ?? 'APB-001';
                                $n = $pr['name'] ?? $pr['product_title'] ?? 'AP Boots';
                            ?>
                                <option value="<?= htmlspecialchars($s) ?>"><?= htmlspecialchars($s) ?> - <?= htmlspecialchars($n) ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                </div>

                <div class="grid-3">
                    <!-- Column 1 -->
                    <div>
                        <div class="input-group">
                            <label>Brand</label>
                            <input type="text" id="gen-brand" value="AP Boots">
                        </div>
                        <div class="input-group">
                            <label>SKU Produk</label>
                            <input type="text" id="gen-sku" value="<?= htmlspecialchars($sampleListing['sku'] ?? 'APB-001') ?>">
                        </div>
                        <div class="input-group">
                            <label>Model Produk</label>
                            <input type="text" id="gen-model" value="<?= htmlspecialchars($sampleListing['model'] ?? 'Terra GP') ?>">
                        </div>
                        <div class="input-group">
                            <label>Varian Warna</label>
                            <input type="text" id="gen-color" value="Black / Hi-Viz Yellow">
                        </div>
                    </div>

                    <!-- Column 2 -->
                    <div>
                        <div class="input-group">
                            <label>Rentang Ukuran (Size Range)</label>
                            <input type="text" id="gen-size-range" value="EU 37-46 (US 5-12)">
                        </div>
                        <div class="input-group">
                            <label>Komposisi Material</label>
                            <input type="text" id="gen-material" value="Virgin PVC / Natural Nitrile Rubber Blend">
                        </div>
                        <div class="input-group">
                            <label>Sertifikasi Standar</label>
                            <input type="text" id="gen-certification" value="SNI 7079:2009, CE EN ISO 20345:2011, ISO 9001:2015">
                        </div>
                        <div class="input-group">
                            <label>Negara Asal (Origin) & MOQ</label>
                            <div style="display: flex; gap: 8px;">
                                <input type="text" id="gen-origin" value="Indonesia" style="flex: 2;">
                                <input type="number" id="gen-moq" value="12" style="flex: 1;" placeholder="MOQ">
                            </div>
                        </div>
                    </div>

                    <!-- Column 3 -->
                    <div>
                        <div class="input-group">
                            <label>Bidang Aplikasi (Applications)</label>
                            <input type="text" id="gen-application" value="Agriculture, Construction, Outdoor, Mining, Hiking">
                        </div>
                        <div class="input-group">
                            <label>Target Negara Ekspor</label>
                            <select id="gen-country">
                                <option value="Germany" selected>🇩🇪 Jerman (Eropa - CE / EN 20345)</option>
                                <option value="United States">🇺🇸 Amerika Serikat (ASTM F2413 / OSHA)</option>
                                <option value="Malaysia">🇲🇾 Malaysia (ASEAN - Sawit & Perkebunan)</option>
                                <option value="United Arab Emirates">🇦🇪 UAE / Dubai (Timur Tengah - Heat & Oil)</option>
                                <option value="Australia">🇦🇺 Australia (Oseania - Mining AS/NZS)</option>
                                <option value="United Kingdom">🇬🇧 Britania Raya (UKCA / S5 Safety)</option>
                                <option value="Singapore">🇸🇬 Singapura (Marine & Clean Logistics)</option>
                                <option value="Saudi Arabia">🇸🇦 Arab Saudi (SASO Standards)</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label>Sudut Industri (Accio Angle)</label>
                            <select id="gen-angle">
                                <option value="Civil Construction" selected>🏗️ Civil Construction</option>
                                <option value="Agriculture & Farming">🌾 Agriculture & Farming</option>
                                <option value="Oil & Gas Refinery">🛢️ Oil & Gas Refinery</option>
                                <option value="Mining & Quarrying">⛏️ Mining & Quarrying</option>
                                <option value="Fishery & Seafood">🐟 Fishery & Seafood</option>
                                <option value="Medical & Kitchen Hygiene">👨‍🍳 Medical & Kitchen Hygiene</option>
                                <option value="Motorcycle & Courier">🏍️ Motorcycle & Courier</option>
                                <option value="Chemical & Factory Manufacturing">🧪 Chemical & Factory</option>
                                <option value="Wholesale OEM Supply">📦 Wholesale OEM Supply</option>
                                <option value="All-Weather Rain Utility">🌧️ All-Weather Rain Utility</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label>Harga Satuan FOB USD / IDR</label>
                            <div style="display: flex; gap: 8px;">
                                <input type="number" step="0.01" id="gen-price-usd" value="<?= $sampleListing['fob_price_usd'] ?? 5.50 ?>" style="flex: 1;" placeholder="FOB USD">
                                <input type="number" step="1000" id="gen-price-idr" value="<?= $sampleListing['base_price_idr'] ?? 89000 ?>" style="flex: 1;" placeholder="IDR">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Action Buttons Bar -->
                <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 14px; padding-top: 14px; border-top: 1px dashed var(--hots-border);">
                    <button class="btn btn-amber" onclick="generateListingFromForm()">
                        <span>⚡</span> Generate Full Alibaba Listing
                    </button>
                    <button class="btn btn-secondary" onclick="downloadCurrentListingCsv()">
                        <span>📥</span> Download CSV 57-Kolom (SKU Ini)
                    </button>
                    <button class="btn btn-secondary" onclick="copyV6Html()">
                        <span>📋</span> Salin V6 HTML Siap-Paste
                    </button>
                    <button class="btn btn-secondary" onclick="copyFullListingJson()">
                        <span>📋</span> Salin JSON Lengkap
                    </button>
                </div>
            </div>

            <!-- Result Sub-Tabs Container -->
            <div style="background: #ffffff; border: 1px solid var(--hots-border); border-radius: 14px; padding: 20px;">
                <div class="sub-nav-tabs">
                    <button class="sub-nav-btn active" onclick="switchListingSubTab('seo', this)">🎯 Judul & SEO Keywords</button>
                    <button class="sub-nav-btn" onclick="switchListingSubTab('specs', this)">📋 Spesifikasi & USPs</button>
                    <button class="sub-nav-btn" onclick="switchListingSubTab('faq', this)">❓ 15 B2B Buyer FAQ</button>
                    <button class="sub-nav-btn" onclick="switchListingSubTab('preview', this)">👁️ Live Preview V6 HTML</button>
                    <button class="sub-nav-btn" onclick="switchListingSubTab('raw', this)">💻 Raw V6 HTML Code</button>
                    <button class="sub-nav-btn" onclick="switchListingSubTab('columns', this)">📊 Baris 57-Kolom Excel</button>
                </div>

                <!-- Sub-panel 1: SEO & Titles -->
                <div class="sub-panel active" id="sub-panel-seo">
                    <div style="margin-bottom: 18px;">
                        <span style="font-size: 0.76rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                            Judul Terpilih (Maksimal 128 Karakter Sesuai Standar Alibaba):
                        </span>
                        <div style="background: #f8fafc; border: 1.5px solid #bfdbfe; border-radius: 8px; padding: 12px 14px; margin-top: 6px; display: flex; justify-content: space-between; align-items: center;">
                            <strong id="out-selected-title" style="color: #1e3a8a; font-size: 0.95rem;">
                                <?= htmlspecialchars($sampleListing['selected_title'] ?? '') ?>
                            </strong>
                            <button class="btn btn-secondary" style="font-size: 0.72rem; padding: 4px 8px;" onclick="copyText('out-selected-title')">
                                Salin
                            </button>
                        </div>
                    </div>

                    <div style="margin-bottom: 18px;">
                        <span style="font-size: 0.76rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                            5 Kandidat Judul B2B Teroptimasi:
                        </span>
                        <div id="out-title-candidates" style="margin-top: 6px; display: flex; flex-direction: column; gap: 6px;">
                            <?php foreach ($sampleListing['title_candidates'] ?? [] as $idx => $cand): ?>
                                <div style="background: #f8fafc; border: 1px solid var(--hots-border); border-radius: 6px; padding: 8px 12px; font-size: 0.82rem; display: flex; justify-content: space-between; align-items: center;">
                                    <span><strong>#<?= $idx + 1 ?>:</strong> <?= htmlspecialchars($cand) ?></span>
                                    <span style="font-size: 0.7rem; color: #64748b;"><?= strlen($cand) ?>/128 char</span>
                                </div>
                            <?php endforeach; ?>
                        </div>
                    </div>

                    <div>
                        <span style="font-size: 0.76rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                            Matriks Kata Kunci SEO Alibaba:
                        </span>
                        <div id="out-seo-matrix" style="margin-top: 8px; display: flex; flex-direction: column; gap: 8px;">
                            <div style="background: #f8fafc; padding: 10px; border-radius: 8px; font-size: 0.8rem;">
                                <strong>Primary Keyword:</strong> <span class="tag-badge" id="out-kw-primary" style="background: #dbeafe; color: #1e40af; font-size: 0.78rem;">waterproof pvc rubber work boots</span>
                            </div>
                            <div style="background: #f8fafc; padding: 10px; border-radius: 8px; font-size: 0.8rem;">
                                <strong>Secondary Keywords:</strong>
                                <div id="out-kw-secondary" style="margin-top: 4px;">
                                    <?php foreach ($sampleListing['seo_keywords']['secondary_keywords'] ?? [] as $skw): ?>
                                        <span class="tag-badge"><?= htmlspecialchars($skw) ?></span>
                                    <?php endforeach; ?>
                                </div>
                            </div>
                            <div style="background: #f8fafc; padding: 10px; border-radius: 8px; font-size: 0.8rem;">
                                <strong>Long-Tail & Buyer Intent:</strong>
                                <div id="out-kw-longtail" style="margin-top: 4px;">
                                    <?php foreach ($sampleListing['seo_keywords']['long_tail_keywords'] ?? [] as $lkw): ?>
                                        <span class="tag-badge" style="background: #ecfdf5; color: #065f46;"><?= htmlspecialchars($lkw) ?></span>
                                    <?php endforeach; ?>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Sub-panel 2: Specs & USPs -->
                <div class="sub-panel" id="sub-panel-specs">
                    <div style="margin-bottom: 20px;">
                        <span style="font-size: 0.76rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                            6 Keunggulan Utama Produk (Unique Selling Propositions):
                        </span>
                        <div id="out-usps-list" style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                            <?php foreach ($sampleListing['usps'] ?? [] as $usp): ?>
                                <div style="background: #f8fafc; border-left: 3px solid #10b981; padding: 8px 12px; font-size: 0.82rem; color: #1e293b;">
                                    <?= htmlspecialchars($usp) ?>
                                </div>
                            <?php endforeach; ?>
                        </div>
                    </div>

                    <div>
                        <span style="font-size: 0.76rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                            Lembar Spesifikasi Teknis (Technical Specifications):
                        </span>
                        <table class="data-table" id="out-specs-table" style="margin-top: 8px;">
                            <tbody>
                                <?php foreach ($sampleListing['technical_specifications'] ?? [] as $k => $v): ?>
                                <tr>
                                    <td style="width: 35%; font-weight: 700; color: #475569;"><?= htmlspecialchars($k) ?></td>
                                    <td style="color: #0f172a;"><?= htmlspecialchars($v) ?></td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Sub-panel 3: 15 FAQs -->
                <div class="sub-panel" id="sub-panel-faq">
                    <span style="font-size: 0.76rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                        15 Tanya Jawab Buyer B2B Internasional (FAQ):
                    </span>
                    <div id="out-faqs-list" style="margin-top: 10px; display: flex; flex-direction: column; gap: 10px;">
                        <?php foreach ($sampleListing['faqs'] ?? [] as $idx => $f): ?>
                            <div style="background: #f8fafc; border: 1px solid var(--hots-border); border-radius: 8px; padding: 12px;">
                                <strong style="color: var(--hots-primary); font-size: 0.84rem;">Q<?= $idx + 1 ?>: <?= htmlspecialchars($f['q']) ?></strong>
                                <p style="font-size: 0.8rem; color: #475569; margin-top: 4px; line-height: 1.5;"><?= htmlspecialchars($f['a']) ?></p>
                            </div>
                        <?php endforeach; ?>
                    </div>
                </div>

                <!-- Sub-panel 4: Live Preview V6 HTML -->
                <div class="sub-panel" id="sub-panel-preview">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-size: 0.76rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                            Live Render Alibaba Description Builder V6:
                        </span>
                        <button class="btn btn-secondary" style="font-size: 0.72rem; padding: 3px 8px;" onclick="copyV6Html()">
                            📋 Salin HTML V6
                        </button>
                    </div>
                    <div id="out-html-preview" style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 20px; max-height: 550px; overflow-y: auto;">
                        <?= $sampleListing['description_v6_html'] ?? '' ?>
                    </div>
                </div>

                <!-- Sub-panel 5: Raw V6 HTML Code -->
                <div class="sub-panel" id="sub-panel-raw">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-size: 0.76rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                            Kode HTML Mentah Siap Paste ke Alibaba Description Builder:
                        </span>
                        <button class="btn btn-secondary" style="font-size: 0.72rem; padding: 3px 8px;" onclick="copyV6Html()">
                            📋 Salin Kode HTML
                        </button>
                    </div>
                    <pre class="code-box" id="out-raw-html" style="max-height: 500px;"><?= htmlspecialchars($sampleListing['description_v6_html'] ?? '') ?></pre>
                </div>

                <!-- Sub-panel 6: Baris 57 Kolom -->
                <div class="sub-panel" id="sub-panel-columns">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-size: 0.76rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                            Nilai Baris 57-Kolom Template Resmi Alibaba Bulk Upload:
                        </span>
                        <button class="btn btn-amber" style="font-size: 0.72rem; padding: 3px 10px;" onclick="downloadCurrentListingCsv()">
                            📥 Download Baris CSV
                        </button>
                    </div>
                    <div style="max-height: 480px; overflow-y: auto;">
                        <table class="data-table" id="out-columns-table">
                            <thead>
                                <tr>
                                    <th style="width: 50px;">No</th>
                                    <th>Nama Kolom Alibaba</th>
                                    <th>Nilai Ekspor</th>
                                </tr>
                            </thead>
                            <tbody id="out-columns-tbody">
                                <?php 
                                $colNames = $controller->get57ColumnsHeader();
                                $colValues = $sampleListing['bulk_upload_57_columns_row'] ?? [];
                                foreach ($colNames as $i => $cname): 
                                    $val = $colValues[$i] ?? '';
                                ?>
                                <tr>
                                    <td><strong><?= $i + 1 ?></strong></td>
                                    <td><code><?= htmlspecialchars($cname) ?></code></td>
                                    <td style="word-break: break-all; font-size: 0.8rem;"><?= htmlspecialchars(is_string($val) && strlen($val) > 100 ? substr($val, 0, 100) . '...' : (string)$val) ?></td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>
        </div>

        <!-- Tab 2: Calculator -->
        <div class="panel" id="tab-calculator">
            <div class="panel-header">
                <div>
                    <h3 class="panel-title"><span>🧮</span> Kalkulator Kemasan Karton & Muatan Kontainer</h3>
                    <p style="font-size: 0.8rem; color: var(--hots-text-muted); margin-top: 4px;">
                        Hitung kapasitas muat kontainer 20ft & 40ft HC serta simulasi fee layanan HOTS Trading (2% s/d 15%).
                    </p>
                </div>
            </div>

            <div class="grid-2">
                <div>
                    <div class="input-group">
                        <label>Harga Satuan USD (FOB)</label>
                        <input type="number" step="0.01" id="calc-usd" value="5.50" oninput="runCalculation()">
                    </div>
                    <div class="input-group">
                        <label>Atau Harga Satuan IDR</label>
                        <input type="number" step="1000" id="calc-idr" value="89000" oninput="runCalculationFromIdr()">
                    </div>
                    <div class="input-group">
                        <label>Isi Pasang per Master Karton</label>
                        <select id="calc-pairs" onchange="runCalculation()">
                            <option value="6">6 Pasang (Karton Kecil / Clogs)</option>
                            <option value="12" selected>12 Pasang (Standar AP Boots - 0.096 CBM)</option>
                            <option value="18">18 Pasang (Karton Sedang - 0.120 CBM)</option>
                            <option value="24">24 Pasang (Sepatu Pendek / Kasual - 0.146 CBM)</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label>Kurs USD/IDR Digunakan</label>
                        <input type="number" id="calc-rate" value="<?= $currentRate ?>" oninput="runCalculation()">
                    </div>
                </div>

                <div style="background: #f8fafc; border: 1px solid var(--hots-border); border-radius: 12px; padding: 20px;">
                    <h4 style="font-size: 0.95rem; font-weight: 800; color: var(--hots-primary); margin-bottom: 14px;">
                        📊 Hasil Estimasi Kemasan & Logistik:
                    </h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                        <div style="background: #fff; padding: 12px; border-radius: 8px; border: 1px solid var(--hots-border);">
                            <div style="font-size: 0.72rem; color: var(--hots-text-muted);">HARGA PER KARTON (USD)</div>
                            <div style="font-size: 1.25rem; font-weight: 800; color: #2563eb;" id="res-carton-usd">$66.00</div>
                        </div>
                        <div style="background: #fff; padding: 12px; border-radius: 8px; border: 1px solid var(--hots-border);">
                            <div style="font-size: 0.72rem; color: var(--hots-text-muted);">HARGA PER KARTON (IDR)</div>
                            <div style="font-size: 1.25rem; font-weight: 800; color: #0f172a;" id="res-carton-idr">Rp 1.068.000</div>
                        </div>
                        <div style="background: #fff; padding: 12px; border-radius: 8px; border: 1px solid var(--hots-border);">
                            <div style="font-size: 0.72rem; color: var(--hots-text-muted);">VOLUME KARTON (CBM)</div>
                            <div style="font-size: 1.1rem; font-weight: 800;" id="res-cbm">0.096 m³</div>
                        </div>
                        <div style="background: #fff; padding: 12px; border-radius: 8px; border: 1px solid var(--hots-border);">
                            <div style="font-size: 0.72rem; color: var(--hots-text-muted);">ESTIMASI BERAT KOTOR</div>
                            <div style="font-size: 1.1rem; font-weight: 800;" id="res-weight">20.4 kg</div>
                        </div>
                    </div>

                    <h5 style="font-size: 0.8rem; font-weight: 800; color: var(--hots-text-muted); margin-bottom: 8px; text-transform: uppercase;">
                        🚢 Kapasitas Kontainer Ekspor:
                    </h5>
                    <p style="font-size: 0.82rem; margin-bottom: 6px;">
                        • <strong>Kontainer 20ft:</strong> <span id="res-20ft" style="color: #2563eb; font-weight: 700;">291 Karton (3.492 Pasang)</span>
                    </p>
                    <p style="font-size: 0.82rem; margin-bottom: 16px;">
                        • <strong>Kontainer 40ft High Cube:</strong> <span id="res-40ft" style="color: #10b981; font-weight: 700;">708 Karton (8.496 Pasang)</span>
                    </p>

                    <h5 style="font-size: 0.8rem; font-weight: 800; color: var(--hots-text-muted); margin-bottom: 8px; text-transform: uppercase;">
                        💼 HOTS Trading Service Charges:
                    </h5>
                    <p style="font-size: 0.78rem; color: #475569;">
                        • <strong>Member Reguler (2%):</strong> <span id="res-fee-2" style="font-weight: 700;">$0.11 / pasang</span><br>
                        • <strong>Non-Member Mandiri (5%):</strong> <span id="res-fee-5" style="font-weight: 700;">$0.275 / pasang</span><br>
                        • <strong>Full Assistance (15%):</strong> <span id="res-fee-15" style="font-weight: 700;">$0.825 / pasang</span>
                    </p>
                </div>
            </div>
        </div>

        <!-- Tab 3: Prompts -->
        <div class="panel" id="tab-prompts">
            <div class="panel-header">
                <div>
                    <h3 class="panel-title"><span>🎯</span> 4-Slot AI Photo Prompt Generator</h3>
                    <p style="font-size: 0.8rem; color: var(--hots-text-muted); margin-top: 4px;">
                        Format prompt terstandarisasi untuk Gemini / Nano Banana AI Image generator sesuai standar Photo Guide Alibaba 2026.
                    </p>
                </div>
                <button class="btn btn-amber" onclick="generatePrompts()">⚡ Generate Prompts</button>
            </div>

            <div class="grid-2" style="margin-bottom: 20px;">
                <div class="input-group">
                    <label>Nama Produk</label>
                    <input type="text" id="prompt-product" value="AP Max Heavy Duty Safety Boots">
                </div>
                <div class="input-group">
                    <label>SKU Produk</label>
                    <input type="text" id="prompt-sku" value="AP-MX-01">
                </div>
                <div class="input-group">
                    <label>Target Benua Ekspor</label>
                    <select id="prompt-continent" onchange="updateCountryList()">
                        <option value="Europe" selected>Eropa (Sertifikasi CE & EN 20345)</option>
                        <option value="North America">Amerika Utara (ASTM F2413 & OSHA)</option>
                        <option value="Southeast Asia">Asia Tenggara (Perkebunan Sawit & Banjir)</option>
                        <option value="Middle East">Timur Tengah (Petrokimia & Hotel Higienis)</option>
                        <option value="Oceania">Oseania (Pertanian & Tambang Australia)</option>
                    </select>
                </div>
                <div class="input-group">
                    <label>Target Negara Spesifik</label>
                    <input type="text" id="prompt-country" value="Germany">
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 14px;">
                <div style="background: #f8fafc; border: 1px solid var(--hots-border); border-radius: 10px; padding: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <strong style="font-size: 0.82rem; color: var(--hots-primary);">📸 Slot 1: Hero E-Commerce (3/4 Upright, Pure White RGB 255,255,255)</strong>
                        <button class="btn btn-secondary" style="font-size: 0.72rem; padding: 3px 8px;" onclick="copyText('p-slot1')">📋 Salin</button>
                    </div>
                    <p id="p-slot1" style="font-size: 0.8rem; color: #334155;">Klik "Generate Prompts" untuk membuat prompt.</p>
                </div>

                <div style="background: #f8fafc; border: 1px solid var(--hots-border); border-radius: 10px; padding: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <strong style="font-size: 0.82rem; color: var(--hots-primary);">📐 Slot 2: Profil Samping Presisi (90-Degree Side Profile)</strong>
                        <button class="btn btn-secondary" style="font-size: 0.72rem; padding: 3px 8px;" onclick="copyText('p-slot2')">📋 Salin</button>
                    </div>
                    <p id="p-slot2" style="font-size: 0.8rem; color: #334155;">Klik "Generate Prompts" untuk membuat prompt.</p>
                </div>

                <div style="background: #f8fafc; border: 1px solid var(--hots-border); border-radius: 10px; padding: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <strong style="font-size: 0.82rem; color: var(--hots-primary);">🥾 Slot 3: Alur Sol & Cleats (Bottom Outsole Tread & Mud Cleats)</strong>
                        <button class="btn btn-secondary" style="font-size: 0.72rem; padding: 3px 8px;" onclick="copyText('p-slot3')">📋 Salin</button>
                    </div>
                    <p id="p-slot3" style="font-size: 0.8rem; color: #334155;">Klik "Generate Prompts" untuk membuat prompt.</p>
                </div>

                <div style="background: #f8fafc; border: 1px solid var(--hots-border); border-radius: 10px; padding: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <strong style="font-size: 0.82rem; color: var(--hots-primary);">🌍 Slot 4: Kontekstual In-Use (Suasana Lapangan Kerja Sesuai Negara)</strong>
                        <button class="btn btn-secondary" style="font-size: 0.72rem; padding: 3px 8px;" onclick="copyText('p-slot4')">📋 Salin</button>
                    </div>
                    <p id="p-slot4" style="font-size: 0.8rem; color: #334155;">Klik "Generate Prompts" untuk membuat prompt.</p>
                </div>
            </div>
        </div>

        <!-- Tab 4: API Debug Suite -->
        <div class="panel" id="tab-api-test">
            <div class="panel-header">
                <div>
                    <h3 class="panel-title"><span>🛠️</span> REST API Diagnostics & Testing Suite</h3>
                    <p style="font-size: 0.8rem; color: var(--hots-text-muted); margin-top: 4px;">
                        Uji endpoint API secara langsung untuk memastikan respon JSON valid sebelum dipanggil oleh frontend atau sistem external.
                    </p>
                </div>
            </div>

            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px;">
                <button class="btn btn-secondary" onclick="testApi('api/health.php')">GET /api/health.php</button>
                <button class="btn btn-secondary" onclick="testApi('api/exchange_rate.php')">GET /api/exchange_rate.php</button>
                <button class="btn btn-secondary" onclick="testApi('api/calculate_carton.php?usd=5.50&pairs=12')">GET /api/calculate_carton.php</button>
                <button class="btn btn-secondary" onclick="testApi('api/prompts.php?product=AP+Max&sku=AP-MX-01&continent=Europe')">GET /api/prompts.php</button>
                <button class="btn btn-secondary" onclick="testApi('api/products.php?limit=5')">GET /api/products.php</button>
            </div>

            <div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                    <span style="font-size: 0.78rem; font-weight: 700; color: var(--hots-text-muted);">LIVE JSON OUTPUT: <span id="api-tested-url" style="color: #2563eb;">-</span></span>
                    <button class="btn btn-secondary" style="font-size: 0.72rem; padding: 2px 8px;" onclick="copyText('api-output')">Salin JSON</button>
                </div>
                <pre class="code-box" id="api-output">// Klik salah satu tombol di atas untuk menguji API endpoint...</pre>
            </div>
        </div>

        <!-- Tab 5: Transfer Checklist -->
        <div class="panel" id="tab-transfer">
            <div class="panel-header">
                <div>
                    <h3 class="panel-title"><span>📋</span> Panduan Transfer ke Environment Debug / cPanel</h3>
                    <p style="font-size: 0.8rem; color: var(--hots-text-muted); margin-top: 4px;">
                        Langkah-langkah transfer folder modul ini ke server staging, cPanel hosting, atau localhost untuk didebug.
                    </p>
                </div>
            </div>

            <div style="line-height: 1.8; font-size: 0.86rem; color: #334155;">
                <h4 style="color: var(--hots-primary); font-weight: 800; margin-bottom: 8px;">1. Lokasi Folder di Server Target</h4>
                <p style="margin-bottom: 12px;">
                    Upload seluruh isi folder <code>HotsAdmin_Module/</code> ke direktori web Anda:
                    <br>• <strong>cPanel Live:</strong> <code>/home/username/public_html/admin/modules/HotsAdmin_Module/</code>
                    <br>• <strong>Local PHP Server:</strong> Cukup buka folder ini di terminal lalu jalankan <code>php -S localhost:8000</code>
                </p>

                <h4 style="color: var(--hots-primary); font-weight: 800; margin-bottom: 8px;">2. Konfigurasi Database</h4>
                <p style="margin-bottom: 12px;">
                    Buka file <code>config/config.php</code> di server atau buat file <code>.env</code> dengan kredensial database Anda:
                    <br><code>DB_HOST=localhost</code> | <code>DB_DATABASE=hotj4796_hotstrading</code> | <code>DB_USERNAME=hotj4796_user</code> | <code>DB_PASSWORD=...</code>
                </p>

                <h4 style="color: var(--hots-primary); font-weight: 800; margin-bottom: 8px;">3. Eksekusi Skrip SQL di phpMyAdmin</h4>
                <p style="margin-bottom: 12px;">
                    Jalankan skrip yang sudah disiapkan di folder <code>sql/</code> secara berurutan:
                    <br>1. <code>sql/database_schema.sql</code> (Membuat tabel <code>alibaba_export_listings</code>, <code>alibaba_market_rules</code>, view)
                    <br>2. <code>sql/seed_market_rules.sql</code> (Mengisi aturan 5 benua Q1-Q4)
                    <br>3. <code>sql/sample_products_seed.sql</code> (Opsional: mengisi data produk sampel jika database masih kosong)
                </p>

                <h4 style="color: var(--hots-primary); font-weight: 800; margin-bottom: 8px;">4. Izin Tulis Direktori Cache (Chmod)</h4>
                <p style="margin-bottom: 12px;">
                    Pastikan folder <code>cache/</code> memiliki izin tulis (chmod 775 atau 755) agar cache kurs valas <code>forex_cache.json</code> dapat diperbarui otomatis.
                </p>
            </div>
        </div>

        <!-- Tab 6: Flow MCP & Photobank Sync -->
        <div class="panel" id="tab-photobank-sync">
            <div class="panel-header">
                <div>
                    <h3 class="panel-title"><span>🔄</span> Hub Integrasi Google Flow MCP & Photobank</h3>
                    <p style="font-size: 0.8rem; color: var(--hots-text-muted); margin-top: 4px;">
                        Sinkronisasi data Product Input (106 SKU x 4 Slot Foto) dengan AI Image Generator (Google Flow) dan repositori resmi Photobank.
                    </p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn btn-primary" onclick="refreshPhotobankSync()">
                        <span>🔄</span> Refresh Status
                    </button>
                    <a href="api/photobank_sync.php" target="_blank" class="btn btn-secondary">
                        <span>🔌</span> JSON API
                    </a>
                </div>
            </div>

            <!-- Sync KPI Cards -->
            <div class="stat-grid" style="margin-bottom: 24px;">
                <div class="stat-card">
                    <div class="label">Total Job AI Foto</div>
                    <div class="val" id="sync-total-jobs"><?= $flowJobsSummary['total_jobs_in_catalog'] ?? 424 ?></div>
                    <div class="sub">106 SKU x 4 Slot E-Commerce</div>
                </div>
                <div class="stat-card c-green">
                    <div class="label">Foto Photobank Tersortir</div>
                    <div class="val" id="sync-total-files"><?= $photobankSummary['total_files_in_folders'] ?? 417 ?></div>
                    <div class="sub">Format WebP Siap Upload</div>
                </div>
                <div class="stat-card c-purple">
                    <div class="label">Kategori Photobank</div>
                    <div class="val">11 Folder</div>
                    <div class="sub">01 Safety sd 11 General</div>
                </div>
                <div class="stat-card c-blue">
                    <div class="label">Target Server Admin</div>
                    <div class="val" style="font-size: 1.15rem; word-break: break-all;">/photo-bank</div>
                    <div class="sub">admin.hotstrading.com</div>
                </div>
            </div>

            <div class="grid-2">
                <!-- Left: 11 Categories Status -->
                <div style="background: #ffffff; border: 1px solid var(--hots-border); border-radius: 12px; padding: 20px;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
                        <h4 style="font-size: 0.95rem; font-weight: 800; color: var(--hots-primary);">
                            📁 Distribusi 11 Kategori Photobank
                        </h4>
                        <span class="badge" style="background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">
                            Auto Match: SKU Prefix
                        </span>
                    </div>
                    <p style="font-size: 0.8rem; color: var(--hots-text-muted); margin-bottom: 14px;">
                        Setiap foto dikelompokkan dengan prefix SKU resmi agar saat diunggah ke Photobank langsung terdeteksi sebagai <strong>product</strong> (bukan unmatched).
                    </p>
                    <div style="max-height: 380px; overflow-y: auto;">
                        <table class="data-table" id="table-photobank-categories">
                            <thead>
                                <tr>
                                    <th>Folder Kategori</th>
                                    <th>Grup Kategori</th>
                                    <th style="text-align: right;">Jumlah File</th>
                                    <th style="text-align: center;">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php if (!empty($photobankSummary['categories'])): ?>
                                    <?php foreach ($photobankSummary['categories'] as $folder => $info): ?>
                                    <tr>
                                        <td><code><?= htmlspecialchars($folder) ?></code></td>
                                        <td style="font-weight: 600;"><?= htmlspecialchars($info['name']) ?></td>
                                        <td style="text-align: right; font-weight: 700; color: var(--hots-primary);"><?= $info['count'] ?></td>
                                        <td style="text-align: center;">
                                            <span class="badge" style="background: <?= $info['count'] > 0 ? '#ecfdf5' : '#fef2f2' ?>; color: <?= $info['count'] > 0 ? '#059669' : '#dc2626' ?>; border-radius: 4px; padding: 2px 6px; font-size: 0.7rem;">
                                                <?= $info['count'] > 0 ? 'READY' : 'EMPTY' ?>
                                            </span>
                                        </td>
                                    </tr>
                                    <?php endforeach; ?>
                                <?php endif; ?>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Right: Flow MCP Job Explorer -->
                <div style="background: #ffffff; border: 1px solid var(--hots-border); border-radius: 12px; padding: 20px;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
                        <h4 style="font-size: 0.95rem; font-weight: 800; color: var(--hots-primary);">
                            ⚡ Live Flow MCP Jobs Inspector
                        </h4>
                        <span class="badge" style="background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">
                            Port 8787 / 0 Credits
                        </span>
                    </div>
                    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                        <input type="text" id="flow-search-sku" placeholder="Cari SKU (misal: APB-016 atau APB-001)" class="form-control" style="flex: 1; padding: 8px 12px; border: 1px solid var(--hots-border); border-radius: 8px; font-size: 0.85rem;" value="APB-016">
                        <button class="btn btn-amber" onclick="searchFlowJobs()">
                            Cari Job
                        </button>
                    </div>
                    <div style="background: #0f172a; color: #f8fafc; border-radius: 8px; padding: 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; max-height: 330px; overflow: auto;" id="flow-job-preview">
                        <div style="color: #94a3b8;">Klik 'Cari Job' untuk melihat payload JSON terstruktur dari SKU terkait...</div>
                    </div>
                    <div style="margin-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.75rem; color: var(--hots-text-muted);">API Endpoint: <code>api/flow_jobs.php?sku=...</code></span>
                        <button class="btn btn-secondary" style="font-size: 0.75rem; padding: 4px 8px;" onclick="copyFlowJson()">
                            📋 Salin JSON
                        </button>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.module-tab').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            
            const targetPanel = document.getElementById('tab-' + tabId);
            if (targetPanel) {
                targetPanel.classList.add('active');
            }
            
            // Find matching tab button
            const btn = Array.from(document.querySelectorAll('.module-tab')).find(b => b.getAttribute('onclick').includes(tabId));
            if (btn) btn.classList.add('active');
        }

        function loadCalculator(usd, idr, sku, name) {
            document.getElementById('calc-usd').value = usd;
            document.getElementById('calc-idr').value = idr;
            document.getElementById('prompt-product').value = name;
            document.getElementById('prompt-sku').value = sku;
            switchTab('calculator');
            runCalculation();
        }

        function runCalculation() {
            const usd = parseFloat(document.getElementById('calc-usd').value) || 0;
            const pairs = parseInt(document.getElementById('calc-pairs').value) || 12;
            const rate = parseFloat(document.getElementById('calc-rate').value) || <?= $currentRate ?>;

            const calcIdr = Math.round(usd * rate);
            document.getElementById('calc-idr').value = calcIdr;

            const cartonUsd = (usd * pairs).toFixed(2);
            const cartonIdr = (calcIdr * pairs).toLocaleString('id-ID');

            let cbm = 0.0960;
            if (pairs > 12) cbm = pairs <= 18 ? 0.1200 : (0.0960 * (pairs / 12));
            const weight = (pairs * 1.7).toFixed(1);

            const cap20ft = Math.floor(28.0 / cbm);
            const cap40ft = Math.floor(68.0 / cbm);

            document.getElementById('res-carton-usd').textContent = '$' + cartonUsd;
            document.getElementById('res-carton-idr').textContent = 'Rp ' + cartonIdr;
            document.getElementById('res-cbm').textContent = cbm.toFixed(3) + ' m³';
            document.getElementById('res-weight').textContent = weight + ' kg';

            document.getElementById('res-20ft').textContent = `${cap20ft.toLocaleString('id-ID')} Karton (${(cap20ft * pairs).toLocaleString('id-ID')} Pasang)`;
            document.getElementById('res-40ft').textContent = `${cap40ft.toLocaleString('id-ID')} Karton (${(cap40ft * pairs).toLocaleString('id-ID')} Pasang)`;

            document.getElementById('res-fee-2').textContent = '$' + (usd * 0.02).toFixed(3) + ' / pasang';
            document.getElementById('res-fee-5').textContent = '$' + (usd * 0.05).toFixed(3) + ' / pasang';
            document.getElementById('res-fee-15').textContent = '$' + (usd * 0.15).toFixed(3) + ' / pasang';
        }

        function runCalculationFromIdr() {
            const idr = parseFloat(document.getElementById('calc-idr').value) || 0;
            const rate = parseFloat(document.getElementById('calc-rate').value) || <?= $currentRate ?>;
            const usd = (idr / rate).toFixed(2);
            document.getElementById('calc-usd').value = usd;
            runCalculation();
        }

        function updateCountryList() {
            const cont = document.getElementById('prompt-continent').value;
            const map = {
                'Europe': 'Germany',
                'North America': 'United States',
                'Southeast Asia': 'Malaysia',
                'Middle East': 'United Arab Emirates',
                'Oceania': 'Australia'
            };
            document.getElementById('prompt-country').value = map[cont] || 'Germany';
        }

        function generatePrompts() {
            const prod = document.getElementById('prompt-product').value;
            const sku = document.getElementById('prompt-sku').value;
            const cont = document.getElementById('prompt-continent').value;
            const country = document.getElementById('prompt-country').value;

            fetch(`api/prompts.php?product=${encodeURIComponent(prod)}&sku=${encodeURIComponent(sku)}&continent=${encodeURIComponent(cont)}&country=${encodeURIComponent(country)}`)
                .then(r => r.json())
                .then(d => {
                    if (d.prompts) {
                        document.getElementById('p-slot1').textContent = d.prompts.slot_1_hero;
                        document.getElementById('p-slot2').textContent = d.prompts.slot_2_side;
                        document.getElementById('p-slot3').textContent = d.prompts.slot_3_tread;
                        document.getElementById('p-slot4').textContent = d.prompts.slot_4_contextual;
                    }
                })
                .catch(err => {
                    alert('Gagal mengambil prompts: ' + err);
                });
        }

        function testApi(url) {
            document.getElementById('api-tested-url').textContent = url;
            document.getElementById('api-output').textContent = 'Memuat respons dari ' + url + '...';
            fetch(url)
                .then(r => r.json())
                .then(d => {
                    document.getElementById('api-output').textContent = JSON.stringify(d, null, 2);
                })
                .catch(e => {
                    document.getElementById('api-output').textContent = 'Error: ' + e;
                });
        }

        function copyText(elemId) {
            const t = document.getElementById(elemId).textContent;
            navigator.clipboard.writeText(t).then(() => {
                alert('Teks berhasil disalin ke clipboard!');
            });
        }

        // --- FLOW MCP & PHOTOBANK SYNC FUNCTIONS ---
        let currentFlowJsonData = null;

        function searchFlowJobs() {
            const sku = document.getElementById('flow-search-sku').value.trim();
            const preview = document.getElementById('flow-job-preview');
            preview.textContent = 'Memuat data job untuk SKU: ' + (sku || 'SEMUA') + '...';

            fetch(`api/flow_jobs.php?sku=${encodeURIComponent(sku)}&limit=10`)
                .then(r => r.json())
                .then(d => {
                    currentFlowJsonData = d;
                    preview.textContent = JSON.stringify(d, null, 2);
                })
                .catch(err => {
                    preview.textContent = 'Gagal memuat Flow jobs: ' + err;
                });
        }

        function copyFlowJson() {
            if (!currentFlowJsonData) {
                alert('Silakan cari job terlebih dahulu sebelum menyalin.');
                return;
            }
            navigator.clipboard.writeText(JSON.stringify(currentFlowJsonData, null, 2)).then(() => {
                alert('Payload JSON Flow MCP berhasil disalin!');
            });
        }

        function refreshPhotobankSync() {
            fetch('api/photobank_sync.php')
                .then(r => r.json())
                .then(d => {
                    if (d.success) {
                        document.getElementById('sync-total-files').textContent = d.total_files_in_folders;
                        alert('Status sinkronisasi diperbarui: ' + d.total_files_in_folders + ' file di 11 kategori Photobank.');
                    }
                })
                .catch(e => {
                    alert('Gagal memperbarui status: ' + e);
                });
        }

        // --- SMART TOP PICKS & MARKET INTELLIGENCE JS ---
        let currentTopPicksData = <?= json_encode($sampleTopPicks['packages'] ?? []) ?>;

        function copyTextDirect(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('Teks berhasil disalin ke clipboard:\n' + text);
            });
        }

        function copyTopPickJson(pkgObj) {
            navigator.clipboard.writeText(JSON.stringify(pkgObj, null, 2)).then(() => {
                alert('Payload JSON produk ' + (pkgObj.sku || '') + ' berhasil disalin!');
            });
        }

        function copyAllTopPicksJson() {
            if (!currentTopPicksData || currentTopPicksData.length === 0) {
                alert('Belum ada data paket rekomendasi.');
                return;
            }
            navigator.clipboard.writeText(JSON.stringify(currentTopPicksData, null, 2)).then(() => {
                alert('Seluruh paket rekomendasi (' + currentTopPicksData.length + ' produk) berhasil disalin ke clipboard!');
            });
        }

        function generateTopPicksWeb() {
            const country = document.getElementById('tp-country').value;
            const angle = document.getElementById('tp-angle').value;
            const limit = document.getElementById('tp-limit').value;
            const container = document.getElementById('top-picks-results');

            container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--hots-text-muted); font-size: 0.9rem;">⚡ Menghitung rekomendasi FOB dan menyusun judul Accio SEO untuk ' + escapeHtml(country) + '...</div>';

            fetch(`api/smart_top_picks.php?country=${encodeURIComponent(country)}&angle=${encodeURIComponent(angle)}&limit=${limit}`)
                .then(r => r.json())
                .then(d => {
                    if (d.success && d.packages) {
                        currentTopPicksData = d.packages;
                        document.getElementById('tp-lbl-country').textContent = d.destination_country;
                        document.getElementById('tp-lbl-angle').textContent = d.industry_angle;
                        document.getElementById('tp-lbl-count').textContent = d.total_generated + ' Paket';
                        renderTopPickCards(d.packages);
                    } else {
                        container.innerHTML = '<div style="grid-column: 1/-1; color: red; padding: 20px; text-align: center;">Gagal memuat rekomendasi.</div>';
                    }
                })
                .catch(err => {
                    container.innerHTML = '<div style="grid-column: 1/-1; color: red; padding: 20px; text-align: center;">Error: ' + escapeHtml(err) + '</div>';
                });
        }

        function renderTopPickCards(packages) {
            const container = document.getElementById('top-picks-results');
            if (!packages || packages.length === 0) {
                container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 30px;">Tidak ada produk yang cocok.</div>';
                return;
            }

            let html = '';
            packages.forEach(pkg => {
                const img = pkg.image_url || 'https://via.placeholder.com/64';
                const t1 = (pkg.tiered_pricing?.tier_1_100_pairs || pkg.unit_fob_usd).toFixed(2);
                const t2 = (pkg.tiered_pricing?.tier_101_500_pairs || (pkg.unit_fob_usd * 0.95)).toFixed(2);
                const t3 = (pkg.tiered_pricing?.tier_501_1000_pairs || (pkg.unit_fob_usd * 0.90)).toFixed(2);
                const t4 = (pkg.tiered_pricing?.tier_above_1000_pairs || (pkg.unit_fob_usd * 0.85)).toFixed(2);

                const c20 = pkg.packaging?.carton_20ft_capacity || 291;
                const c40 = pkg.packaging?.carton_40ft_capacity || 708;

                html += `
                <div class="top-pick-card">
                    <div class="top-pick-card-header">
                        <img src="${img}" class="top-pick-thumb" onerror="this.src='https://via.placeholder.com/64'">
                        <div style="flex: 1; min-width: 0;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                <span class="badge" style="background: #eff6ff; color: #1d4ed8; font-weight: 800; font-size: 0.72rem; padding: 2px 8px; border-radius: 4px;">
                                    #${pkg.rank} • ${escapeHtml(pkg.sku)}
                                </span>
                                <span style="font-size: 0.72rem; font-weight: 700; color: #10b981; background: #ecfdf5; padding: 2px 6px; border-radius: 4px;">
                                    FOB $${pkg.unit_fob_usd.toFixed(2)}
                                </span>
                            </div>
                            <h4 style="font-size: 0.88rem; font-weight: 800; color: var(--hots-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                ${escapeHtml(pkg.original_name)}
                            </h4>
                            <div style="font-size: 0.72rem; color: var(--hots-text-muted);">
                                ${escapeHtml(pkg.category || "Boots")}
                            </div>
                        </div>
                    </div>
                    <div class="top-pick-body">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <span style="font-size: 0.72rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase;">
                                    Accio 2026 SEO Export Title
                                </span>
                                <button class="btn btn-secondary" style="font-size: 0.68rem; padding: 2px 8px;" onclick="copyTextDirect('${escapeQuotes(pkg.optimized_b2b_title)}')">
                                    Salin
                                </button>
                            </div>
                            <div style="background: #f8fafc; border: 1px dashed var(--hots-border); border-radius: 8px; padding: 10px; font-size: 0.8rem; font-weight: 600; color: #1e293b; line-height: 1.4;">
                                ${escapeHtml(pkg.optimized_b2b_title)}
                            </div>
                        </div>

                        <div>
                            <span style="font-size: 0.72rem; font-weight: 700; color: var(--hots-text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
                                Tiered FOB Pricing (USD / Pasang)
                            </span>
                            <div class="price-tiers-grid">
                                <div class="tier-item">
                                    <div class="tier-qty">100 psg</div>
                                    <div class="tier-price">$${t1}</div>
                                </div>
                                <div class="tier-item">
                                    <div class="tier-qty">500 psg</div>
                                    <div class="tier-price">$${t2}</div>
                                </div>
                                <div class="tier-item">
                                    <div class="tier-qty">1.000 psg</div>
                                    <div class="tier-price">$${t3}</div>
                                </div>
                                <div class="tier-item">
                                    <div class="tier-qty">&gt;1.000 psg</div>
                                    <div class="tier-price" style="color: #059669;">$${t4}</div>
                                </div>
                            </div>
                        </div>

                        <div style="background: #f1f5f9; border-radius: 8px; padding: 10px 12px; font-size: 0.76rem; color: #334155; line-height: 1.6;">
                            <div style="display: flex; justify-content: space-between;">
                                <span>Master Carton: <strong>12 Pasang ($${pkg.carton_price_usd.toFixed(2)})</strong></span>
                                <span>Volume: <strong>0.096 CBM</strong></span>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                                <span>Muatan 20ft: <strong>${c20} Karton</strong></span>
                                <span>Muatan 40ft HC: <strong>${c40} Karton</strong></span>
                            </div>
                        </div>

                        <div style="display: flex; gap: 8px; margin-top: auto; padding-top: 8px;">
                            <button class="btn btn-secondary" style="flex: 1; font-size: 0.74rem; justify-content: center;" onclick="loadCalculator(${pkg.unit_fob_usd}, ${pkg.unit_price_idr}, '${escapeQuotes(pkg.sku)}', '${escapeQuotes(pkg.original_name)}')">
                                🧮 Hitung Karton
                            </button>
                            <button class="btn btn-primary" style="flex: 1; font-size: 0.74rem; justify-content: center;" onclick="copyTopPickJson(${escapeQuotes(JSON.stringify(pkg))})">
                                📋 Salin Payload
                            </button>
                        </div>
                    </div>
                </div>
                `;
            });

            container.innerHTML = html;
        }

        function changeQuarterIntel(quarter, btnElem) {
            document.querySelectorAll('.quarter-btn').forEach(b => b.classList.remove('active'));
            if (btnElem) btnElem.classList.add('active');

            fetch(`api/market_intelligence.php?quarter=${quarter}`)
                .then(r => r.json())
                .then(d => {
                    if (d.success && d.continents) {
                        renderContinentsGrid(d.continents);
                    }
                })
                .catch(err => {
                    alert('Gagal memuat intelijen pasar: ' + err);
                });
        }

        function renderContinentsGrid(continents) {
            const grid = document.getElementById('continents-grid');
            const icons = {
                'Europe': '🇪🇺',
                'North America': '🇺🇸',
                'Southeast Asia': '🌴',
                'Middle East': '🏜️',
                'Oceania': '🦘'
            };

            let html = '';
            for (const [key, c] of Object.entries(continents)) {
                const icon = icons[key] || '🌍';
                const countries = (c.top_countries || []).join(', ');
                const keywords = (c.recommended_keywords || []).map(k => `<span class="tag-badge">🔍 ${escapeHtml(k)}</span>`).join('');
                const skus = (c.recommended_skus || []).join(', ');

                html += `
                <div class="intel-card">
                    <div class="intel-card-header">
                        <div>
                            <span style="font-size: 1.3rem; margin-right: 6px;">${icon}</span>
                            <strong style="font-size: 0.95rem; color: var(--hots-primary);">${escapeHtml(c.continent)}</strong>
                        </div>
                        <span class="badge" style="background: #eff6ff; color: #1d4ed8; font-weight: 700; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">
                            ${escapeHtml(c.recommended_angle || '')}
                        </span>
                    </div>

                    <div style="font-size: 0.78rem; color: var(--hots-text-muted);">
                        <strong>Negara Kunci:</strong> ${escapeHtml(countries)}
                    </div>

                    <div style="background: #f8fafc; border-left: 3px solid #2563eb; padding: 10px 12px; border-radius: 0 8px 8px 0; font-size: 0.8rem; color: #1e293b;">
                        <strong style="color: #2563eb; display: block; margin-bottom: 2px;">⚡ Pemicu Kebutuhan Musiman:</strong>
                        ${escapeHtml(c.seasonal_demand_trigger)}
                    </div>

                    <div style="font-size: 0.78rem;">
                        <strong style="color: var(--hots-text-main);">Regulasi & Sertifikasi:</strong><br>
                        <span class="tag-badge" style="background: #fef3c7; color: #92400e;">
                            📜 ${escapeHtml(c.certifications)}
                        </span>
                    </div>

                    <div style="font-size: 0.78rem;">
                        <strong style="color: var(--hots-text-main);">Kata Kunci Pencarian Buyer:</strong><br>
                        <div style="margin-top: 4px;">
                            ${keywords}
                        </div>
                    </div>

                    <div style="font-size: 0.78rem; margin-top: auto; padding-top: 8px; border-top: 1px dashed var(--hots-border);">
                        <span style="color: var(--hots-text-muted);">Rekomendasi SKU AP Boots:</span>
                        <strong style="color: #059669;">${escapeHtml(skus)}</strong>
                    </div>
                </div>
                `;
            }
            grid.innerHTML = html;
        }

        function escapeHtml(text) {
            if (!text) return '';
            return text.toString()
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

        function escapeQuotes(text) {
            if (!text) return '';
            return text.toString().replace(/'/g, "\\'").replace(/"/g, '&quot;');
        }

        // --- ALIBABA LISTING MASTER GENERATOR JS ---
        let currentListingData = <?= json_encode($sampleListing ?? []) ?>;

        function switchListingSubTab(subId, btn) {
            document.querySelectorAll('.sub-nav-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.sub-panel').forEach(p => p.classList.remove('active'));
            if (btn) btn.classList.add('active');
            const target = document.getElementById('sub-panel-' + subId);
            if (target) target.classList.add('active');
        }

        function loadPresetProduct(sku) {
            fetch(`api/generate_alibaba_listing.php?sku=${encodeURIComponent(sku)}`)
                .then(r => r.json())
                .then(d => {
                    if (d.success) {
                        currentListingData = d;
                        document.getElementById('gen-brand').value = d.brand || 'AP Boots';
                        document.getElementById('gen-sku').value = d.sku || sku;
                        document.getElementById('gen-model').value = d.model || '';
                        document.getElementById('gen-price-usd').value = d.fob_price_usd || 5.50;
                        document.getElementById('gen-price-idr').value = d.base_price_idr || 89000;
                        updateListingView(d);
                    }
                })
                .catch(err => {
                    alert('Gagal memuat data produk: ' + err);
                });
        }

        function generateListingFromForm() {
            const payload = {
                brand: document.getElementById('gen-brand').value,
                sku: document.getElementById('gen-sku').value,
                model: document.getElementById('gen-model').value,
                color: document.getElementById('gen-color').value,
                size_range: document.getElementById('gen-size-range').value,
                material: document.getElementById('gen-material').value,
                certification: document.getElementById('gen-certification').value,
                origin: document.getElementById('gen-origin').value,
                moq: document.getElementById('gen-moq').value,
                application: document.getElementById('gen-application').value,
                destination_country: document.getElementById('gen-country').value,
                industry_angle: document.getElementById('gen-angle').value,
                fob_price_usd: document.getElementById('gen-price-usd').value,
                base_price_idr: document.getElementById('gen-price-idr').value
            };

            fetch('api/generate_alibaba_listing.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(r => r.json())
            .then(d => {
                if (d.success) {
                    currentListingData = d;
                    updateListingView(d);
                    alert('Listing Alibaba berhasil di-generate secara lengkap!');
                } else {
                    alert('Gagal menghasilkan listing.');
                }
            })
            .catch(err => {
                alert('Error: ' + err);
            });
        }

        function updateListingView(d) {
            // Selected Title
            document.getElementById('out-selected-title').textContent = d.selected_title || '';

            // Candidates
            let candHtml = '';
            (d.title_candidates || []).forEach((c, idx) => {
                candHtml += `
                <div style="background: #f8fafc; border: 1px solid var(--hots-border); border-radius: 6px; padding: 8px 12px; font-size: 0.82rem; display: flex; justify-content: space-between; align-items: center;">
                    <span><strong>#${idx + 1}:</strong> ${escapeHtml(c)}</span>
                    <span style="font-size: 0.7rem; color: #64748b;">${c.length}/128 char</span>
                </div>`;
            });
            document.getElementById('out-title-candidates').innerHTML = candHtml;

            // SEO Keywords
            if (d.seo_keywords) {
                document.getElementById('out-kw-primary').textContent = d.seo_keywords.primary_keyword || '';
                document.getElementById('out-kw-secondary').innerHTML = (d.seo_keywords.secondary_keywords || []).map(k => `<span class="tag-badge">${escapeHtml(k)}</span>`).join('');
                document.getElementById('out-kw-longtail').innerHTML = (d.seo_keywords.long_tail_keywords || []).map(k => `<span class="tag-badge" style="background: #ecfdf5; color: #065f46;">${escapeHtml(k)}</span>`).join('');
            }

            // USPs
            let uspHtml = '';
            (d.usps || []).forEach(u => {
                uspHtml += `<div style="background: #f8fafc; border-left: 3px solid #10b981; padding: 8px 12px; font-size: 0.82rem; color: #1e293b;">${escapeHtml(u)}</div>`;
            });
            document.getElementById('out-usps-list').innerHTML = uspHtml;

            // Tech Specs
            let specsHtml = '';
            for (const [k, v] of Object.entries(d.technical_specifications || {})) {
                specsHtml += `<tr><td style="width: 35%; font-weight: 700; color: #475569;">${escapeHtml(k)}</td><td style="color: #0f172a;">${escapeHtml(v)}</td></tr>`;
            }
            document.getElementById('out-specs-table').innerHTML = `<tbody>${specsHtml}</tbody>`;

            // FAQs
            let faqHtml = '';
            (d.faqs || []).forEach((f, idx) => {
                faqHtml += `
                <div style="background: #f8fafc; border: 1px solid var(--hots-border); border-radius: 8px; padding: 12px;">
                    <strong style="color: var(--hots-primary); font-size: 0.84rem;">Q${idx + 1}: ${escapeHtml(f.q)}</strong>
                    <p style="font-size: 0.8rem; color: #475569; margin-top: 4px; line-height: 1.5;">${escapeHtml(f.a)}</p>
                </div>`;
            });
            document.getElementById('out-faqs-list').innerHTML = faqHtml;

            // HTML Preview & Raw Code
            document.getElementById('out-html-preview').innerHTML = d.description_v6_html || '';
            document.getElementById('out-raw-html').textContent = d.description_v6_html || '';

            // 57 Column Row
            let colRowsHtml = '';
            const colValues = d.bulk_upload_57_columns_row || [];
            const colNames = <?= json_encode($controller->get57ColumnsHeader()) ?>;
            colNames.forEach((cname, i) => {
                const val = colValues[i] !== undefined ? colValues[i] : '';
                const displayVal = (typeof val === 'string' && val.length > 100) ? val.substring(0, 100) + '...' : val;
                colRowsHtml += `<tr><td><strong>${i + 1}</strong></td><td><code>${escapeHtml(cname)}</code></td><td style="word-break: break-all; font-size: 0.8rem;">${escapeHtml(displayVal)}</td></tr>`;
            });
            document.getElementById('out-columns-tbody').innerHTML = colRowsHtml;
        }

        function downloadCurrentListingCsv() {
            const sku = document.getElementById('gen-sku').value.trim();
            const country = document.getElementById('gen-country').value;
            window.location.href = `api/export_alibaba_bulk.php?format=csv&sku=${encodeURIComponent(sku)}&country=${encodeURIComponent(country)}`;
        }

        function copyV6Html() {
            if (!currentListingData || !currentListingData.description_v6_html) {
                alert('Silakan generate listing terlebih dahulu.');
                return;
            }
            navigator.clipboard.writeText(currentListingData.description_v6_html).then(() => {
                alert('Alibaba Description Builder V6 HTML berhasil disalin ke clipboard! Siap di-paste ke Alibaba Supplier Center.');
            });
        }

        function copyFullListingJson() {
            if (!currentListingData) {
                alert('Silakan generate listing terlebih dahulu.');
                return;
            }
            navigator.clipboard.writeText(JSON.stringify(currentListingData, null, 2)).then(() => {
                alert('Data JSON lengkap listing berhasil disalin ke clipboard!');
            });
        }

        // Initialize prompts and Flow search on load
        generatePrompts();
        searchFlowJobs();
    </script>
</body>
</html>
