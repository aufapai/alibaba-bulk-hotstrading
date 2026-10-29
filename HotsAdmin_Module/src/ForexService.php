<?php
/**
 * HOTS TRADING - FOREX EXCHANGE RATE SERVICE
 * ==========================================
 * File: src/ForexService.php
 * Handles real-time forex rate fetching, file caching, and fallback protection.
 */

namespace Hots\Export;

class ForexService
{
    private string $cacheFile;
    private int $cacheTtl;
    private float $fallbackRate;
    private array $providers;

    public function __construct(?array $config = null)
    {
        if ($config === null) {
            $configFile = dirname(__DIR__) . '/config/config.php';
            $appConfig = file_exists($configFile) ? require $configFile : [];
            $config = $appConfig['forex'] ?? [];
        }

        $cacheDir = dirname(__DIR__) . '/cache';
        if (!is_dir($cacheDir)) {
            @mkdir($cacheDir, 0775, true);
        }

        $this->cacheFile = $config['cache_file'] ?? ($cacheDir . '/forex_cache.json');
        $this->cacheTtl = (int)($config['cache_ttl_seconds'] ?? 1800);
        $this->fallbackRate = (float)($config['fallback_rate'] ?? 16250.00);
        $this->providers = $config['providers'] ?? [
            'https://api.exchangerate-api.com/v4/latest/USD',
            'https://open.er-api.com/v6/latest/USD'
        ];
    }

    public function getRate(bool $forceRefresh = false): array
    {
        // 1. Check cache
        if (!$forceRefresh && file_exists($this->cacheFile)) {
            $age = time() - filemtime($this->cacheFile);
            if ($age < $this->cacheTtl) {
                $cached = json_decode(file_get_contents($this->cacheFile), true);
                if (!empty($cached['rate']) && is_numeric($cached['rate'])) {
                    $cached['is_cached'] = true;
                    $cached['cache_age_seconds'] = $age;
                    return $cached;
                }
            }
        }

        // 2. Fetch from live API providers
        foreach ($this->providers as $url) {
            $ctx = stream_context_create([
                'http' => [
                    'timeout' => 4,
                    'header' => "User-Agent: HOTS-Admin-Debug/2.0\r\nAccept: application/json\r\n"
                ]
            ]);

            $raw = @file_get_contents($url, false, $ctx);
            if ($raw) {
                $data = json_decode($raw, true);
                if (!empty($data['rates']['IDR'])) {
                    $rate = (float)$data['rates']['IDR'];
                    $payload = [
                        'success' => true,
                        'rate' => $rate,
                        'source' => 'Live Forex API (' . parse_url($url, PHP_URL_HOST) . ')',
                        'updated_at' => date('Y-m-d H:i:s'),
                        'is_cached' => false,
                        'cache_age_seconds' => 0
                    ];
                    @file_put_contents($this->cacheFile, json_encode($payload, JSON_PRETTY_PRINT));
                    return $payload;
                }
            }
        }

        // 3. Fallback
        return [
            'success' => false,
            'rate' => $this->fallbackRate,
            'source' => 'Baseline Fallback (Offline / API unreachable)',
            'updated_at' => date('Y-m-d H:i:s'),
            'is_cached' => false,
            'cache_age_seconds' => -1
        ];
    }
}
