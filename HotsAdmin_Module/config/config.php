<?php
/**
 * HOTS TRADING - B2B EXPORT MODULE CONFIGURATION
 * ===============================================
 * File: config/config.php
 * Target: cPanel MariaDB / MySQL (`admin.hotstrading.com`) & Local Debug
 */

return [
    // Database Connection
    'db' => [
        'driver'    => getenv('DB_CONNECTION') ?: 'mysql',
        'host'      => getenv('DB_HOST') ?: 'localhost',
        'port'      => (int)(getenv('DB_PORT') ?: 3306),
        'database'  => getenv('DB_DATABASE') ?: 'hotj4796_hotstrading',
        'username'  => getenv('DB_USERNAME') ?: 'hotj4796_user',
        'password'  => getenv('DB_PASSWORD') ?: '',
        'charset'   => 'utf8mb4',
        // Optional SQLite path fallback when MySQL is not available in local debug
        'sqlite_path' => dirname(__DIR__, 2) . '/Database/alibaba_master.db'
    ],

    // Forex Cache & Currency Settings
    'forex' => [
        'cache_file' => __DIR__ . '/../cache/forex_cache.json',
        'cache_ttl_seconds' => 1800, // 30 minutes
        'fallback_rate' => 16250.00,
        'providers' => [
            'https://api.exchangerate-api.com/v4/latest/USD',
            'https://open.er-api.com/v6/latest/USD'
        ]
    ],

    // HOTS Export Business Rules & Packaging Standards
    'packaging' => [
        'default_pairs_per_carton' => 12,
        'carton_dimensions_cm' => '60 x 40 x 40 cm',
        'cbm_standard_12pairs' => 0.096,
        'container_20ft_effective_cbm' => 28.0,
        'container_40ft_hc_effective_cbm' => 68.0,
        'gross_weight_multiplier_per_pair' => 1.7
    ],

    // HOTS Service Fee Tier Policy
    'fees' => [
        'member_regular' => 0.02,       // 2.0%
        'non_member_mandiri' => 0.05,   // 5.0%
        'full_assistance' => 0.15       // 15.0%
    ],

    // Security & CORS
    'cors' => [
        'allowed_origins' => [
            'https://admin.hotstrading.com',
            'https://hotstrading.com',
            'http://localhost',
            'http://localhost:8000',
            'http://localhost:8888'
        ]
    ],

    // Environment mode: 'debug' | 'production'
    'app_env' => getenv('APP_ENV') ?: 'debug'
];
