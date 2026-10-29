<?php
/**
 * HOTS TRADING - DATABASE DRIVER & DIAGNOSTIC WRAPPER
 * ==================================================
 * File: src/Database.php
 * Supports: MySQL / MariaDB (Primary) + SQLite (Local Debug Fallback)
 */

namespace Hots\Export;

use PDO;
use Exception;

class Database
{
    private static ?PDO $instance = null;
    private static array $config = [];
    private static array $diagnostics = [
        'driver' => 'none',
        'connected' => false,
        'message' => 'Not initialized',
        'details' => []
    ];

    public static function init(?array $customConfig = null): void
    {
        if ($customConfig) {
            self::$config = $customConfig;
        } elseif (empty(self::$config)) {
            $configFile = dirname(__DIR__) . '/config/config.php';
            if (file_exists($configFile)) {
                $appConfig = require $configFile;
                self::$config = $appConfig['db'] ?? [];
            }
        }
    }

    public static function getConnection(): ?PDO
    {
        if (self::$instance !== null) {
            return self::$instance;
        }

        self::init();

        $driver = self::$config['driver'] ?? 'mysql';
        $host = self::$config['host'] ?? 'localhost';
        $port = self::$config['port'] ?? 3306;
        $dbname = self::$config['database'] ?? 'hotj4796_hotstrading';
        $user = self::$config['username'] ?? 'hotj4796_user';
        $pass = self::$config['password'] ?? '';
        $charset = self::$config['charset'] ?? 'utf8mb4';

        // Candidate SQLite paths discovery
        $sqlitePath = self::$config['sqlite_path'] ?? '';
        if (!$sqlitePath || !file_exists($sqlitePath)) {
            $candidateSqlite = [
                dirname(__DIR__, 2) . '/Database/alibaba_master.db',
                'D:/Work/Hots/Product Input/Database/alibaba_master.db',
                'D:/Work/Hots/Webiste/Database/alibaba_master.db'
            ];
            foreach ($candidateSqlite as $cand) {
                if (file_exists($cand)) {
                    $sqlitePath = $cand;
                    break;
                }
            }
        }

        // 1. If explicitly configured for SQLite, connect directly without MySQL timeout
        if ($driver === 'sqlite') {
            if ($sqlitePath && file_exists($sqlitePath)) {
                try {
                    $pdo = new PDO("sqlite:" . $sqlitePath, null, null, [
                        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
                    ]);
                    self::$instance = $pdo;
                    self::$diagnostics = [
                        'driver' => 'sqlite',
                        'connected' => true,
                        'message' => 'Connected to Local SQLite database directly.',
                        'details' => ['sqlite_path' => $sqlitePath]
                    ];
                    return self::$instance;
                } catch (Exception $sqle) {
                    $sqliteError = $sqle->getMessage();
                }
            }
        }

        // 2. Try Primary MySQL / MariaDB Connection
        try {
            $dsn = "mysql:host={$host};port={$port};dbname={$dbname};charset={$charset}";
            $pdo = new PDO($dsn, $user, $pass, [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_TIMEOUT => 2
            ]);
            self::$instance = $pdo;
            self::$diagnostics = [
                'driver' => 'mysql',
                'connected' => true,
                'message' => 'Connected to MySQL / MariaDB database successfully.',
                'details' => [
                    'host' => $host,
                    'port' => $port,
                    'database' => $dbname,
                    'user' => $user
                ]
            ];
            return self::$instance;
        } catch (Exception $e) {
            $mysqlError = $e->getMessage();
        }

        // 3. Try Fallback Local SQLite (For Local Offline Debugging)
        if ($sqlitePath && file_exists($sqlitePath)) {
            try {
                $pdo = new PDO("sqlite:" . $sqlitePath, null, null, [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
                ]);
                self::$instance = $pdo;
                self::$diagnostics = [
                    'driver' => 'sqlite',
                    'connected' => true,
                    'message' => 'Connected to Local SQLite fallback database.',
                    'details' => [
                        'sqlite_path' => $sqlitePath,
                        'mysql_fallback_reason' => $mysqlError
                    ]
                ];
                return self::$instance;
            } catch (Exception $sqle) {
                // SQLite also failed
            }
        }

        // 4. Mark as Offline
        self::$diagnostics = [
            'driver' => 'none',
            'connected' => false,
            'message' => 'Database connection offline. Both MySQL and SQLite fallback failed.',
            'details' => [
                'mysql_error' => $mysqlError ?? 'Unknown MySQL error',
                'sqlite_checked' => $sqlitePath
            ]
        ];

        return null;
    }

    public static function getDiagnostics(): array
    {
        if (self::$instance === null) {
            self::getConnection();
        }
        return self::$diagnostics;
    }
}
