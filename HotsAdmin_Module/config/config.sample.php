<?php
/**
 * HOTS TRADING - B2B EXPORT MODULE CONFIGURATION (SAMPLE TEMPLATE)
 * ================================================================
 * File: config/config.sample.php
 * Copy this file to `config.php` and set your credentials for deployment.
 */

return [
    'db' => [
        'driver'    => 'mysql',
        'host'      => 'localhost',
        'port'      => 3306,
        'database'  => 'cpanel_database_name',
        'username'  => 'cpanel_database_user',
        'password'  => 'cpanel_database_password',
        'charset'   => 'utf8mb4',
        'sqlite_path' => dirname(__DIR__, 2) . '/Database/alibaba_master.db'
    ],
    'forex' => [
        'cache_file' => __DIR__ . '/../cache/forex_cache.json',
        'cache_ttl_seconds' => 1800,
        'fallback_rate' => 16250.00,
        'providers' => [
            'https://api.exchangerate-api.com/v4/latest/USD',
            'https://open.er-api.com/v6/latest/USD'
        ]
    ],
    'packaging' => [
        'default_pairs_per_carton' => 12,
        'carton_dimensions_cm' => '60 x 40 x 40 cm',
        'cbm_standard_12pairs' => 0.096,
        'container_20ft_effective_cbm' => 28.0,
        'container_40ft_hc_effective_cbm' => 68.0,
        'gross_weight_multiplier_per_pair' => 1.7
    ],
    'fees' => [
        'member_regular' => 0.02,
        'non_member_mandiri' => 0.05,
        'full_assistance' => 0.15
    ],
    'cors' => [
        'allowed_origins' => [
            'https://admin.hotstrading.com',
            'http://localhost:8000'
        ]
    ],
    'app_env' => 'production'
];
