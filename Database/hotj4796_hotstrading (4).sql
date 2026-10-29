-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 06, 2026 at 02:45 PM
-- Server version: 10.11.15-MariaDB-cll-lve
-- PHP Version: 8.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotj4796_hotstrading`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity_logs`
--

CREATE TABLE `activity_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  `action` varchar(100) NOT NULL,
  `entity_type` varchar(50) DEFAULT NULL,
  `entity_id` int(11) DEFAULT NULL,
  `entity_name` varchar(255) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `details` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `activity_logs`
--

INSERT INTO `activity_logs` (`id`, `user_id`, `user_email`, `action`, `entity_type`, `entity_id`, `entity_name`, `ip_address`, `user_agent`, `details`, `created_at`) VALUES
(1, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.225.86', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36', '{\"ip\":\"202.65.225.86\"}', '2026-03-04 04:56:15'),
(2, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.225.86', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.225.86\"}', '2026-03-04 04:57:22'),
(3, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.225.86', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.225.86\"}', '2026-03-04 06:23:21'),
(4, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.225.86', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.225.86\"}', '2026-03-04 07:33:04'),
(5, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.192\"}', '2026-03-05 02:57:08'),
(6, 1, 'admin@hotstrading.com', 'LOGOUT', 'user', 1, NULL, '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-05 02:58:22'),
(7, NULL, 'aufahots@gmail.com', 'REGISTER', 'user', 58, 'PT Maju Jaya Semesta', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"role\":\"MANUFACTURER\"}', '2026-03-05 03:23:49'),
(8, 48, 'hotstrading11@gmail.com', 'LOGIN', 'user', 48, 'HOTS Trading Super', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.192\"}', '2026-03-05 03:24:38'),
(9, 48, 'hotstrading11@gmail.com', 'LOGOUT', 'user', 48, NULL, '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-05 03:26:31'),
(10, 48, 'hotstrading11@gmail.com', 'LOGIN', 'user', 48, 'HOTS Trading Super', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.192\"}', '2026-03-05 03:38:09'),
(11, 48, 'hotstrading11@gmail.com', 'LOGIN', 'user', 48, 'HOTS Trading Super', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.192\"}', '2026-03-05 04:32:52'),
(12, 48, 'hotstrading11@gmail.com', 'LOGOUT', 'user', 48, NULL, '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-05 04:32:56'),
(13, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.192\"}', '2026-03-05 04:34:19'),
(14, NULL, 'aufahots@gmail.com', 'REGISTER', 'user', 60, 'PT Maju Jaya Semesta', '202.65.239.192', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36', '{\"role\":\"DISTRIBUTOR\"}', '2026-03-05 05:15:44'),
(15, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.192\"}', '2026-03-05 06:44:35'),
(16, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.192\"}', '2026-03-05 06:46:02'),
(17, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.192\"}', '2026-03-05 08:23:28'),
(18, NULL, 'aufahots@gmail.com', 'EMAIL_VERIFIED', 'user', 60, 'PT Maju Jaya Semesta', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-05 08:25:04'),
(19, NULL, 'aufahots@gmail.com', 'LOGIN', 'user', 60, 'PT Maju Jaya Semesta', '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.192\"}', '2026-03-05 08:25:13'),
(20, 1, 'admin@hotstrading.com', 'LOGOUT', 'user', 1, NULL, '202.65.239.192', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-05 08:43:34'),
(21, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 03:07:18'),
(22, 1, 'admin@hotstrading.com', 'LOGOUT', 'user', 1, NULL, '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-06 03:21:58'),
(23, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 03:32:21'),
(24, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 03:33:03'),
(25, 1, 'admin@hotstrading.com', 'LOGOUT', 'user', 1, NULL, '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-06 03:34:20'),
(26, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 04:00:18'),
(27, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 04:06:17'),
(28, 28, 'warehouse@apboots.com', 'LOGOUT', 'user', 28, NULL, '202.65.239.195', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36', NULL, '2026-03-06 04:33:11'),
(29, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 04:34:13'),
(30, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 04:35:50'),
(31, 28, 'warehouse@apboots.com', 'LOGOUT', 'user', 28, NULL, '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-06 04:53:38'),
(32, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 04:53:44'),
(33, 1, 'admin@hotstrading.com', 'LOGOUT', 'user', 1, NULL, '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-06 04:53:48'),
(34, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 04:54:11'),
(35, 1, 'admin@hotstrading.com', 'LOGOUT', 'user', 1, NULL, '202.65.239.195', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36', NULL, '2026-03-06 04:56:07'),
(36, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.195', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 04:56:15'),
(37, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.195', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 05:59:29'),
(38, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.195', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36', '{\"ip\":\"202.65.239.195\"}', '2026-03-06 08:22:56'),
(39, 1, 'admin@hotstrading.com', 'LOGOUT', 'user', 1, NULL, '202.65.239.195', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36', NULL, '2026-03-06 08:23:33'),
(40, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.154', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.154\"}', '2026-03-10 08:35:39'),
(41, 1, 'admin@hotstrading.com', 'LOGOUT', 'user', 1, NULL, '202.65.239.154', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-10 08:36:47'),
(42, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.154', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.154\"}', '2026-03-10 08:37:32'),
(43, 1, 'admin@hotstrading.com', 'LOGOUT', 'user', 1, NULL, '202.65.239.154', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-10 08:37:39'),
(44, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '202.65.239.154', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.154\"}', '2026-03-10 08:38:30'),
(45, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.239.154', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.154\"}', '2026-03-11 05:47:47'),
(46, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.239.154', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.239.154\"}', '2026-03-11 07:04:48'),
(47, 28, 'warehouse@apboots.com', 'LOGOUT', 'user', 28, NULL, '202.65.239.154', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-11 07:04:53'),
(48, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '116.254.97.43', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"116.254.97.43\"}', '2026-03-12 02:32:20'),
(49, 1, 'admin@hotstrading.com', 'LOGIN', 'user', 1, 'HOTS Trading', '116.254.97.43', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"116.254.97.43\"}', '2026-03-12 02:54:54'),
(50, 1, 'admin@hotstrading.com', 'LOGOUT', 'user', 1, NULL, '116.254.97.43', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-12 02:55:09'),
(51, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '116.254.97.43', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"116.254.97.43\"}', '2026-03-12 04:30:03'),
(52, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '116.254.97.43', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"116.254.97.43\"}', '2026-03-12 07:41:32'),
(53, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.238.157\"}', '2026-03-13 02:29:55'),
(54, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.238.157\"}', '2026-03-13 04:32:28'),
(55, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.238.157\"}', '2026-03-13 04:32:57'),
(56, 28, 'warehouse@apboots.com', 'LOGOUT', 'user', 28, NULL, '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-13 04:38:26'),
(57, NULL, 'aufahots@gmail.com', 'REGISTER', 'user', 67, 'PT BALEO BELIA JAYA', '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"role\":\"DISTRIBUTOR\"}', '2026-03-13 04:39:43'),
(58, 28, 'warehouse@apboots.com', 'LOGOUT', 'user', 28, NULL, '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-13 04:39:58'),
(59, NULL, 'aufahots@gmail.com', 'EMAIL_VERIFIED', 'user', 67, 'PT BALEO BELIA JAYA', '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', NULL, '2026-03-13 04:42:18'),
(60, NULL, 'aufahots@gmail.com', 'LOGIN', 'user', 67, 'PT BALEO BELIA JAYA', '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.238.157\"}', '2026-03-13 04:42:32'),
(61, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.238.157\"}', '2026-03-13 04:44:14'),
(62, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.238.157\"}', '2026-03-13 06:52:05'),
(63, NULL, 'aufahots@gmail.com', 'LOGIN', 'user', 67, 'PT BALEO BELIA JAYA', '202.65.238.157', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.238.157\"}', '2026-03-13 07:38:57'),
(64, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.225.123', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.225.123\"}', '2026-03-16 00:50:25'),
(65, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.225.123', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.225.123\"}', '2026-03-17 03:58:39'),
(66, 28, 'warehouse@apboots.com', 'LOGIN', 'user', 28, 'PT Waru Gunung Industry', '202.65.225.123', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '{\"ip\":\"202.65.225.123\"}', '2026-03-18 03:00:57');

-- --------------------------------------------------------

--
-- Table structure for table `admin_activity_log`
--

CREATE TABLE `admin_activity_log` (
  `id` int(10) UNSIGNED NOT NULL,
  `admin_id` int(10) UNSIGNED NOT NULL,
  `action` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admin_activity_log`
--

INSERT INTO `admin_activity_log` (`id`, `admin_id`, `action`, `description`, `ip_address`, `created_at`) VALUES
(1, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-10 15:34:48'),
(2, 1, 'APPROVE_USER', 'User ID: 64 → Status: ACTIVE', '202.65.239.154', '2026-03-10 15:35:03'),
(3, 1, 'LOGOUT', 'Admin logout', '202.65.239.154', '2026-03-10 15:53:16'),
(4, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 08:58:19'),
(5, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 11:41:28'),
(6, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 14:01:56'),
(7, 1, 'LOGOUT', 'Admin logout', '202.65.239.154', '2026-03-11 14:21:39'),
(8, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 14:21:57'),
(9, 1, 'LOGOUT', 'Admin logout', '202.65.239.154', '2026-03-11 14:22:01'),
(10, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 14:34:04'),
(11, 1, 'DEACTIVATE_PRODUCT', 'Product ID: 42 — AP Metaguard Black', '202.65.239.154', '2026-03-11 14:34:33'),
(12, 1, 'ACTIVATE_PRODUCT', 'Product ID: 42 — AP Metaguard Black', '202.65.239.154', '2026-03-11 14:34:36'),
(13, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 14:35:00'),
(14, 1, 'LOGOUT', 'Admin logout', '202.65.239.154', '2026-03-11 14:35:10'),
(15, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 14:35:11'),
(16, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 14:35:25'),
(17, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 14:35:43'),
(18, 1, 'DEACTIVATE_PRODUCT', 'Product ID: 42 — AP Metaguard Black', '202.65.239.154', '2026-03-11 14:37:28'),
(19, 1, 'ACTIVATE_PRODUCT', 'Product ID: 42 — AP Metaguard Black', '202.65.239.154', '2026-03-11 14:37:39'),
(20, 1, 'SUSPEND_USER', 'User ID: 64 → Status: SUSPENDED', '202.65.239.154', '2026-03-11 14:39:27'),
(21, 1, 'DEACTIVATE_PRODUCT', 'Product ID: 42 — AP Metaguard Black', '202.65.239.154', '2026-03-11 14:59:32'),
(22, 1, 'ACTIVATE_PRODUCT', 'Product ID: 42 — AP Metaguard Black', '202.65.239.154', '2026-03-11 14:59:41'),
(23, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 16:14:26'),
(24, 1, 'LOGOUT', 'Admin logout', '202.65.239.154', '2026-03-11 16:22:48'),
(25, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 16:22:51'),
(26, 1, 'LOGOUT', 'Admin logout', '202.65.239.154', '2026-03-11 16:22:57'),
(27, 1, 'LOGIN', 'Login dari 202.65.239.154', '202.65.239.154', '2026-03-11 16:22:59'),
(28, 1, 'LOGOUT', 'Admin logout', '202.65.239.154', '2026-03-11 16:23:01'),
(29, 1, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 09:13:08'),
(30, 1, 'CREATE_USER', 'User baru ditambahkan oleh super admin: Farhan Aditya (SUPER_ADMIN)', '116.254.97.43', '2026-03-12 09:54:13'),
(31, 1, 'LOGOUT', 'Admin logout', '116.254.97.43', '2026-03-12 09:54:22'),
(32, 65, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 09:54:23'),
(33, 65, 'LOGOUT', 'Admin logout', '116.254.97.43', '2026-03-12 09:54:41'),
(34, 48, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 09:56:18'),
(35, 48, 'LOGOUT', 'Admin logout', '116.254.97.43', '2026-03-12 10:12:13'),
(36, 65, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 11:07:21'),
(37, 65, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 11:07:22'),
(38, 48, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 11:29:37'),
(39, 48, 'LOGOUT', 'Admin logout', '116.254.97.43', '2026-03-12 11:29:49'),
(40, 48, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 11:31:06'),
(41, 48, 'LOGOUT', 'Admin logout', '116.254.97.43', '2026-03-12 11:31:14'),
(42, 48, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 11:31:37'),
(43, 48, 'LOGOUT', 'Admin logout', '116.254.97.43', '2026-03-12 11:31:39'),
(44, 65, 'LOGOUT', 'Admin logout', '116.254.97.43', '2026-03-12 11:33:28'),
(45, 1, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 11:33:36'),
(46, 1, 'LOGOUT', 'Admin logout', '116.254.97.43', '2026-03-12 11:33:42'),
(47, 1, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 11:34:00'),
(48, 1, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 11:35:24'),
(49, 1, 'CREATE_USER', 'User baru ditambahkan oleh super admin: Susi Sumarno (ADMIN)', '116.254.97.43', '2026-03-12 11:37:45'),
(50, 1, 'LOGOUT', 'Admin logout', '116.254.97.43', '2026-03-12 11:37:58'),
(51, 66, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 11:38:07'),
(52, 1, 'LOGOUT', 'Admin logout', '116.254.97.43', '2026-03-12 11:38:59'),
(53, 66, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 11:39:01'),
(54, 1, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 13:24:29'),
(55, 1, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 13:24:59'),
(56, 1, 'LOGIN', 'Login dari 116.254.97.43', '116.254.97.43', '2026-03-12 14:42:07'),
(57, 1, 'UPDATE_PRODUCT', 'Product ID: 42 diperbarui oleh admin', '116.254.97.43', '2026-03-12 14:42:20'),
(58, 1, 'SUSPEND_USER', 'User ID: 27 → Status: SUSPENDED', '116.254.97.43', '2026-03-12 14:43:41'),
(59, 1, 'REJECT_USER', 'User ID: 27 → Status: REJECTED', '116.254.97.43', '2026-03-12 14:43:47'),
(60, 1, 'APPROVE_USER', 'User ID: 27 → Status: ACTIVE', '116.254.97.43', '2026-03-12 14:43:49'),
(61, 66, 'LOGIN', 'Login dari 202.65.238.157', '202.65.238.157', '2026-03-13 10:09:51'),
(62, 66, 'LOGIN', 'Login dari 202.65.238.157', '202.65.238.157', '2026-03-13 11:29:21'),
(63, 1, 'LOGIN', 'Login dari 202.65.238.157', '202.65.238.157', '2026-03-13 11:29:52'),
(64, 1, 'ACTIVATE_PRODUCT', 'Product ID: 42 — AP Metaguard Black', '202.65.238.157', '2026-03-13 11:30:06'),
(65, 1, 'LOGIN', 'Login dari 202.65.238.157', '202.65.238.157', '2026-03-13 14:42:07'),
(66, 1, 'LOGIN', 'Login dari 202.65.225.123', '202.65.225.123', '2026-03-17 08:19:11'),
(67, 1, 'ACTIVATE_PRODUCT', 'Product ID: 43 — AP CLOGS ( WARNA)', '202.65.225.123', '2026-03-17 08:42:45'),
(68, 1, 'DEACTIVATE_PRODUCT', 'Product ID: 43 — AP CLOGS ( WARNA)', '202.65.225.123', '2026-03-17 08:43:04'),
(69, 1, 'LOGIN', 'Login dari 202.65.225.123', '202.65.225.123', '2026-03-17 13:37:17'),
(70, 1, 'LOGIN', 'Login dari 182.253.58.175', '182.253.58.175', '2026-03-19 21:14:06'),
(71, 1, 'LOGIN', 'Login dari 140.213.0.134', '140.213.0.134', '2026-03-26 16:31:53'),
(72, 1, 'LOGIN', 'Login dari 202.65.238.190', '202.65.238.190', '2026-04-01 14:36:46'),
(73, 1, 'TOGGLE_BLOG', 'Post ID: 7 → draft', '202.65.238.190', '2026-04-01 14:36:53'),
(74, 1, 'LOGIN', 'Login dari 202.65.225.197', '202.65.225.197', '2026-04-06 11:46:08');

-- --------------------------------------------------------

--
-- Table structure for table `blog_posts`
--

CREATE TABLE `blog_posts` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `excerpt` text DEFAULT NULL,
  `content` longtext NOT NULL,
  `cover_image` varchar(500) DEFAULT NULL,
  `category` varchar(100) DEFAULT 'General',
  `tags` varchar(500) DEFAULT NULL,
  `author_name` varchar(100) DEFAULT 'HOTS Trading',
  `status` enum('draft','published') NOT NULL DEFAULT 'draft',
  `meta_title` varchar(255) DEFAULT NULL,
  `meta_description` text DEFAULT NULL,
  `views` int(11) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `blog_posts`
--

INSERT INTO `blog_posts` (`id`, `title`, `slug`, `excerpt`, `content`, `cover_image`, `category`, `tags`, `author_name`, `status`, `meta_title`, `meta_description`, `views`, `created_at`, `updated_at`) VALUES
(1, 'Mengenal B2B Trading Agent: Solusi Korporasi Modern untuk Manajemen Pengadaan', 'mengenal-b2b-trading-agent-solusi-korporasi', 'Apa itu B2B Trading Agent dan bagaimana perannya dalam membantu perusahaan mengelola risiko pengadaan serta strategi pasar?', '<h2>Apa Itu B2B Trading Agent?</h2>\r\n<p>Berbeda dengan broker ritel, <strong>B2B Trading Agent</strong> adalah entitas yang ditunjuk secara resmi oleh perusahaan untuk mewakili kepentingan perdagangan mereka dalam transaksi antar korporasi. HOTS Trading (PT IndoTrading Berkah Semesta) menjalankan fungsi ini secara profesional di Indonesia.</p>\r\n<h2>Peran Strategis dalam Manajemen Pengadaan</h2>\r\n<p>Direktur Keuangan dan Procurement Manager modern menghadapi tekanan volatilitas harga yang semakin tinggi. Dalam 2024–2025, harga komoditas industri mengalami fluktuasi rata-rata <strong>12–18% per kuartal</strong>, mempersulit proyeksi COGS jangka menengah.</p>\r\n<p>HOTS Trading hadir untuk mengisi gap ini melalui:</p>\r\n<ul>\r\n<li><strong>Price Lock & Forward Pricing</strong> — mengunci harga komoditas 3–12 bulan ke depan</li>\r\n<li><strong>Supplier Diversification</strong> — membangun channel pasokan alternatif terverifikasi</li>\r\n<li><strong>Market Intelligence Reports</strong> — laporan analisis pasar bulanan untuk pengambilan keputusan strategis</li>\r\n</ul>\r\n<h2>Siapa yang Membutuhkan B2B Trading Agent?</h2>\r\n<p>Perusahaan manufaktur, konstruksi, dan distribusi dengan anggaran pengadaan tahunan di atas <strong>IDR 5 Miliar</strong> adalah kandidat utama yang dapat memperoleh manfaat signifikan dari kemitraan agen trading B2B.</p>\r\n<p>Hubungi tim kami untuk konsultasi gratis: <a href=\"mailto:info@hotstrading.com\">info@hotstrading.com</a></p>', NULL, 'B2B Strategy', NULL, 'Tim Riset HOTS Trading', 'published', 'B2B Trading Agent Indonesia | HOTS Trading', 'Kenali peran B2B Trading Agent dalam manajemen pengadaan korporasi. HOTS Trading (PT IndoTrading Berkah Semesta) hadir sebagai mitra strategis bisnis Anda.', 1, '2026-02-27 11:36:25', '2026-03-05 09:50:25'),
(2, 'HOTS Trading: Menghubungkan Industri Indonesia ke Pasar Global', 'hots-trading-menghubungkan-industri-indonesia', 'HOTS Trading hadir sebagai platform B2B yang menjembatani produsen lokal yang berkualitas dengan distributor yang membutuhkan pasokan stabil. Pelajari bagaimana visi kami mendorong pertumbuhan industri nasional.', '<h2>Siapa Kami?</h2>\r\n<p>HOTS Trading adalah platform perdagangan B2B yang lahir dari kebutuhan nyata industri Indonesia: mempertemukan produsen berkualitas dengan distributor yang tepat secara efisien dan transparan.</p>\r\n<p>Kami percaya bahwa industri manufaktur Indonesia memiliki potensi besar yang belum sepenuhnya tergali. Dengan ribuan produsen yang tersebar di seluruh kepulauan, tantangan utama bukan pada kapasitas produksi — melainkan pada akses pasar dan kepercayaan transaksi.</p>\r\n\r\n<h2>Mengapa HOTS Trading?</h2>\r\n<p>Platform kami dirancang untuk menjawab tiga permasalahan utama dalam rantai perdagangan B2B:</p>\r\n<ol>\r\n<li><strong>Visibilitas</strong> — Produsen lokal sulit ditemukan oleh distributor potensial</li>\r\n<li><strong>Efisiensi</strong> — Proses negosiasi dan penawaran masih manual dan memakan waktu</li>\r\n<li><strong>Kepercayaan</strong> — Tidak ada sistem verifikasi standar untuk menjamin kredibilitas kedua pihak</li>\r\n</ol>\r\n\r\n<h2>Fitur Unggulan Platform</h2>\r\n<p>HOTS Trading menyediakan:</p>\r\n<ul>\r\n<li><strong>Katalog Produk B2B</strong> — Ribuan produk dari produsen terverifikasi</li>\r\n<li><strong>Sistem RFQ (Request for Quotation)</strong> — Proses penawaran digital yang terstandarisasi</li>\r\n<li><strong>Verifikasi Mitra</strong> — Setiap produsen dan distributor melalui proses verifikasi</li>\r\n<li><strong>Dashboard Analytics</strong> — Data transaksi dan performa secara real-time</li>\r\n</ul>\r\n\r\n<h2>Bergabunglah dengan Komunitas HOTS Trading</h2>\r\n<p>Saat ini HOTS Trading telah melayani ratusan mitra bisnis dari berbagai sektor industri, mulai dari keselamatan kerja, alas kaki, peralatan industri, hingga produk konsumen.</p>\r\n<p>Daftarkan perusahaan Anda sekarang dan mulai perjalanan menuju perdagangan B2B yang lebih efisien.</p>', 'https://hotstrading.com/hots-assets/blog/hots-trading-platform.jpg', 'B2B Strategy', 'HOTS Trading, B2B Platform, Distributor Indonesia, Manufaktur', 'Tim HOTS Trading', 'published', 'HOTS Trading: Platform B2B Terpercaya untuk Industri Indonesia', 'HOTS Trading menghubungkan produsen lokal berkualitas dengan distributor di seluruh Indonesia melalui platform B2B modern yang efisien dan transparan.', 1, '2026-02-27 14:57:08', '2026-03-05 09:50:06'),
(3, 'AP Boots: Sepatu Safety Andalan Industri Indonesia Sejak 1960', 'ap-boots-sepatu-safety-andalan-industri-indonesia', 'AP Boots adalah merek sepatu keselamatan kerja yang telah menjadi pilihan utama industri Indonesia selama lebih dari 60 tahun. Temukan mengapa AP Boots dipercaya jutaan pekerja dan tersedia melalui HOTS Trading.', '<h2>Warisan 60 Tahun AP Boots</h2>\r\n<p>Dalam dunia keselamatan kerja di Indonesia, satu nama selalu hadir di garis terdepan: <strong>AP Boots</strong>. Merek yang telah berdiri sejak tahun 1960 ini bukan sekadar nama—melainkan simbol kepercayaan jutaan pekerja dari Sabang hingga Merauke.</p>\r\n\r\n<h2>Standar Kualitas Internasional, Harga Lokal</h2>\r\n<p>AP Boots memproduksi sepatu safety yang memenuhi standar keselamatan internasional:</p>\r\n<ul>\r\n<li><strong>SNI 7079:2016</strong> — Standar Nasional Indonesia untuk alas kaki keselamatan</li>\r\n<li><strong>ISO 20345</strong> — Standar internasional untuk sepatu keselamatan industri</li>\r\n<li><strong>Anti-slip sole</strong> — Sol anti-selip untuk berbagai permukaan kerja</li>\r\n<li><strong>Steel toe cap</strong> — Pelindung ujung baja untuk melindungi jari kaki dari benturan</li>\r\n</ul>\r\n\r\n<h2>Varian Produk AP Boots</h2>\r\n<p>HOTS Trading menyediakan berbagai varian AP Boots untuk memenuhi kebutuhan industri:</p>\r\n<ul>\r\n<li><strong>AP Boots 9518</strong> — Sepatu bot tinggi untuk area basah dan berlumpur</li>\r\n<li><strong>AP Boots Safety Low</strong> — Sepatu safety rendah untuk penggunaan sehari-hari</li>\r\n<li><strong>AP Boots Chemical Resistant</strong> — Tahan terhadap bahan kimia</li>\r\n<li><strong>AP Boots Mining Series</strong> — Dirancang khusus untuk industri pertambangan</li>\r\n</ul>\r\n\r\n<h2>Mengapa Distributor Memilih AP Boots?</h2>\r\n<p>Keunggulan bisnis AP Boots sebagai produk distribusi:</p>\r\n<ul>\r\n<li>Margin distributor yang kompetitif dengan minimum order terjangkau</li>\r\n<li>Dukungan marketing materials dari produsen</li>\r\n<li>Garansi keaslian produk melalui sistem verifikasi HOTS Trading</li>\r\n<li>Pengiriman dari gudang pusat ke seluruh Indonesia</li>\r\n</ul>\r\n\r\n<h2>Pesan AP Boots Melalui HOTS Trading</h2>\r\n<p>Sebagai distributor resmi, Anda dapat mengajukan RFQ untuk AP Boots langsung melalui platform HOTS Trading. Proses pengajuan hanya membutuhkan beberapa menit, dan tim kami akan merespons dalam 1x24 jam kerja.</p>', 'https://hotstrading.com/hots-assets/blog/ap-boots-safety.jpg', 'Industry News', 'AP Boots, Sepatu Safety, K3, Keselamatan Kerja, Alas Kaki Industrial', 'Tim HOTS Trading', 'published', 'AP Boots Sepatu Safety Industrial — Distributor Resmi HOTS Trading', 'AP Boots, sepatu keselamatan kerja andalan industri Indonesia sejak 1960. Tersedia untuk distributor melalui platform HOTS Trading dengan proses RFQ yang mudah.', 1, '2026-02-27 14:57:08', '2026-03-05 09:50:40'),
(4, 'Swallow: Dari Brand Lokal Menjadi Kekuatan Global dalam 40 Tahun', 'swallow-brand-lokal-menjadi-kekuatan-global', 'Swallow telah membuktikan bahwa brand lokal Indonesia mampu bersaing di panggung internasional. Selama hampir 40 tahun, Swallow konsisten menghadirkan produk alas kaki berkualitas untuk pasar domestik dan ekspor.', '<h2>Perjalanan Swallow Menuju Pasar Internasional</h2>\r\n<p>Ketika membicarakan brand alas kaki Indonesia yang mampu menembus pasar internasional, <strong>Swallow</strong> selalu menjadi referensi utama. Berdiri hampir empat dekade yang lalu, Swallow telah membuktikan bahwa produk lokal Indonesia dapat bersaing di kancah global.</p>\r\n\r\n<h2>Filosofi Produk Swallow</h2>\r\n<p>Kekuatan Swallow terletak pada konsistensi tiga pilar utama:</p>\r\n<ul>\r\n<li><strong>Kualitas Material</strong> — Menggunakan bahan baku pilihan yang tahan lama dan nyaman</li>\r\n<li><strong>Desain Adaptif</strong> — Mengikuti tren pasar lokal dan internasional</li>\r\n<li><strong>Harga Kompetitif</strong> — Tetap terjangkau tanpa mengorbankan kualitas</li>\r\n</ul>\r\n\r\n<h2>Portofolio Produk Swallow</h2>\r\n<p>Swallow memproduksi berbagai kategori alas kaki yang tersedia melalui jaringan distribusi HOTS Trading:</p>\r\n<ul>\r\n<li><strong>Sandal Jepit Swallow</strong> — Produk flagship dengan penjualan terbesar</li>\r\n<li><strong>Sandal Home Series</strong> — Kenyamanan untuk penggunaan dalam rumah</li>\r\n<li><strong>Sandal Outdoor</strong> — Dirancang untuk aktivitas luar ruang</li>\r\n<li><strong>Sandal Kerja</strong> — Ergonomis untuk pemakaian seharian</li>\r\n</ul>\r\n\r\n<h2>Pasar Ekspor Swallow</h2>\r\n<p>Saat ini produk Swallow telah diekspor ke lebih dari 20 negara, termasuk:</p>\r\n<ul>\r\n<li>Negara-negara Asia Tenggara: Malaysia, Filipina, Vietnam, Myanmar</li>\r\n<li>Timur Tengah: Arab Saudi, Uni Emirat Arab, Kuwait</li>\r\n<li>Afrika: Nigeria, Ghana, Kenya, Tanzania</li>\r\n</ul>\r\n\r\n<h2>Peluang Distribusi Swallow bersama HOTS Trading</h2>\r\n<p>HOTS Trading adalah mitra strategis dalam distribusi produk Swallow di Indonesia. Sebagai distributor terdaftar, Anda akan mendapatkan:</p>\r\n<ul>\r\n<li>Akses langsung ke pricelist distributor dan program promosi</li>\r\n<li>Minimum order yang fleksibel sesuai kapasitas bisnis Anda</li>\r\n<li>Dukungan logistik ke seluruh Indonesia</li>\r\n<li>Sistem RFQ digital untuk pemesanan yang lebih cepat</li>\r\n</ul>\r\n<p>Bergabunglah dengan jaringan distributor Swallow melalui HOTS Trading dan manfaatkan kekuatan brand yang telah terbukti selama hampir 40 tahun.</p>', 'https://hotstrading.com/hots-assets/blog/swallow-brand.jpg', 'Partnership', 'Swallow, Brand Lokal, Sandal Indonesia, Distribusi, Ekspor', 'Tim HOTS Trading', 'published', 'Swallow: Brand Alas Kaki Lokal Indonesia yang Go Global — HOTS Trading', 'Swallow telah membuktikan brand lokal Indonesia bisa bersaing global. Temukan peluang distribusi produk Swallow bersama HOTS Trading.', 1, '2026-02-27 14:57:08', '2026-03-05 09:50:35'),
(5, 'Panduan Lengkap: Cara Menggunakan Sistem RFQ di HOTS Trading', 'panduan-sistem-rfq-hots-trading', 'Proses Request for Quotation (RFQ) di HOTS Trading dirancang untuk memudahkan distributor mendapatkan penawaran terbaik dari produsen. Panduan ini menjelaskan setiap langkah dari katalog hingga deal.', '<h2>Apa itu RFQ di HOTS Trading?</h2>\r\n<p>RFQ (Request for Quotation) adalah fitur inti HOTS Trading yang memungkinkan distributor mengajukan permintaan harga resmi kepada produsen secara digital. Tidak perlu lagi telepon atau email — semua proses berjalan melalui platform.</p>\r\n\r\n<h2>Langkah 1: Temukan Produk di Katalog</h2>\r\n<p>Mulai dengan menjelajahi <strong>Katalog Produk</strong> HOTS Trading. Gunakan filter berdasarkan:</p>\r\n<ul>\r\n<li>Kategori produk (Safety Equipment, Footwear, Industrial Tools, dll.)</li>\r\n<li>Nama produsen</li>\r\n<li>Kisaran harga</li>\r\n<li>Minimum order quantity (MOQ)</li>\r\n</ul>\r\n\r\n<h2>Langkah 2: Ajukan RFQ</h2>\r\n<p>Klik tombol <strong>\"Request for Quotation\"</strong> pada halaman produk, lalu isi form berikut:</p>\r\n<ul>\r\n<li>Jumlah yang dibutuhkan (wajib)</li>\r\n<li>Harga target (opsional)</li>\r\n<li>Catatan khusus (spesifikasi tambahan, jadwal pengiriman, dll.)</li>\r\n</ul>\r\n\r\n<h2>Langkah 3: Produsen Merespons</h2>\r\n<p>Produsen akan menerima notifikasi dan dapat merespons dengan:</p>\r\n<ul>\r\n<li>Penawaran harga resmi</li>\r\n<li>Counter-offer dengan syarat berbeda</li>\r\n<li>Permintaan klarifikasi</li>\r\n</ul>\r\n<p>Semua komunikasi tercatat di dalam sistem untuk referensi Anda.</p>\r\n\r\n<h2>Langkah 4: Negosiasi dan Deal</h2>\r\n<p>Setelah menerima penawaran, Anda dapat:</p>\r\n<ul>\r\n<li>Menerima penawaran langsung</li>\r\n<li>Bernegosiasi lebih lanjut</li>\r\n<li>Membandingkan penawaran dari beberapa produsen</li>\r\n</ul>\r\n\r\n<h2>Tips Mendapatkan Penawaran Terbaik</h2>\r\n<ol>\r\n<li>Cantumkan volume kebutuhan yang akurat agar produsen dapat memberikan harga volume</li>\r\n<li>Sebutkan timeline pengiriman untuk membantu perencanaan produksi</li>\r\n<li>Ajukan RFQ ke beberapa produsen sekaligus untuk perbandingan harga</li>\r\n<li>Manfaatkan fitur \"Catatan Khusus\" untuk spesifikasi teknis yang spesifik</li>\r\n</ol>', 'https://hotstrading.com/hots-assets/blog/rfq-guide.jpg', 'Tutorial', 'RFQ, Request for Quotation, Panduan B2B, Katalog, HOTS Trading', 'Tim HOTS Trading', 'published', 'Panduan Sistem RFQ HOTS Trading — Cara Mudah Dapatkan Penawaran Terbaik', 'Panduan lengkap menggunakan sistem RFQ di HOTS Trading. Dari browsing katalog hingga deal distributor-produsen, semua dijelaskan langkah demi langkah.', 1, '2026-02-27 14:57:08', '2026-03-05 09:50:12'),
(7, 'HOTS Trading: Platform B2B Terpercaya untuk Industri Indonesia', 'hots-trading-platform-b2b-indonesia', 'HOTS Trading hadir sebagai platform B2B Distributor terpercaya untuk menghubungkan industri Indonesia ke pasar global.', '<h2>Siapa Kami?</h2><p>HOTS Trading adalah platform B2B Distributor yang menghubungkan manufacturer dan distributor di seluruh Indonesia. Kami menyediakan solusi pengadaan terintegrasi dengan sistem RFQ, verifikasi supplier, dan pembayaran aman.</p><h2>Kenapa HOTS Trading?</h2><ul><li>Supplier terverifikasi dengan badge resmi</li><li>Sistem RFQ transparan dan efisien</li><li>Pembayaran aman via Midtrans</li></ul>', NULL, 'B2B Strategy', NULL, 'Tim HOTS Trading', 'draft', 'HOTS Trading Platform B2B Terpercaya', 'Platform B2B Distributor terpercaya untuk industri Indonesia.', 3, '2026-03-03 15:57:43', '2026-04-01 14:36:53');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `slug`, `description`, `created_at`, `updated_at`) VALUES
(1, 'General', 'general', 'Default category', '2026-02-12 07:24:11', '2026-02-12 07:24:11'),
(2, 'Electronics', 'electronics', 'Electronic products', '2026-02-12 07:24:11', '2026-02-12 07:24:11'),
(3, 'Textiles', 'textiles', 'Textile products', '2026-02-12 07:24:11', '2026-02-12 07:24:11'),
(4, 'Machinery', 'machinery', 'Industrial machinery', '2026-02-12 07:24:11', '2026-02-12 07:24:11'),
(5, 'Food & Beverage', 'food-beverage', 'Food products', '2026-02-12 07:24:11', '2026-02-12 07:24:11');

-- --------------------------------------------------------

--
-- Table structure for table `contact_messages`
--

CREATE TABLE `contact_messages` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `message` text NOT NULL,
  `status` enum('NEW','READ','REPLIED','ARCHIVED') DEFAULT 'NEW',
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `contact_messages`
--

INSERT INTO `contact_messages` (`id`, `name`, `email`, `phone`, `company`, `message`, `status`, `ip_address`, `user_agent`, `created_at`, `updated_at`) VALUES
(1, 'Aufa', 'Aufatea1@gmail.com', '', '', 'Halo PT Waru Gunung Industry, saya ingin mengetahui lebih lanjut tentang produk Anda.', 'NEW', '116.254.97.43', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36', '2026-03-12 04:06:09', '2026-03-12 04:06:09');

-- --------------------------------------------------------

--
-- Table structure for table `email_logs`
--

CREATE TABLE `email_logs` (
  `id` int(10) UNSIGNED NOT NULL,
  `recipient_email` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `status` enum('SENT','FAILED') NOT NULL,
  `error_message` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `email_queue`
--

CREATE TABLE `email_queue` (
  `id` int(11) NOT NULL,
  `recipient_email` varchar(255) NOT NULL,
  `recipient_name` varchar(255) DEFAULT NULL,
  `subject` varchar(255) NOT NULL,
  `body` text NOT NULL,
  `status` enum('PENDING','SENT','FAILED') DEFAULT 'PENDING',
  `error_message` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `sent_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `email_tokens`
--

CREATE TABLE `email_tokens` (
  `id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `expires_at` timestamp NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `login_attempts`
--

CREATE TABLE `login_attempts` (
  `id` int(10) UNSIGNED NOT NULL,
  `ip_address` varchar(45) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `attempt_time` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `manufacturers`
--

CREATE TABLE `manufacturers` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(200) NOT NULL,
  `slug` varchar(200) NOT NULL,
  `country` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `logo_url` varchar(500) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `quotation_id` int(11) DEFAULT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `type` varchar(50) NOT NULL DEFAULT 'general',
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) NOT NULL DEFAULT 0,
  `action_url` varchar(500) DEFAULT NULL,
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`metadata`)),
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `read_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `password_resets`
--

CREATE TABLE `password_resets` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `expires_at` datetime NOT NULL,
  `used` tinyint(1) DEFAULT 0,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `password_resets`
--

INSERT INTO `password_resets` (`id`, `user_id`, `email`, `token`, `expires_at`, `used`, `created_at`) VALUES
(17, 48, 'hotstrading11@gmail.com', '9c4608ec0dc19f31d863e3bdf7f5e8549fd1ec6b72be875d60b96c2513a0387a', '2026-02-12 12:28:26', 0, '2026-02-12 11:28:26'),
(18, 48, 'hotstrading11@gmail.com', 'ecfdb217257a7df8c5cde8dd8478a71367855b598055ff4fff561d6b93a41cb4', '2026-02-12 12:33:39', 0, '2026-02-12 11:33:39');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `product_code` varchar(50) NOT NULL,
  `name` varchar(255) NOT NULL,
  `code` varchar(50) NOT NULL,
  `series` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `status` enum('PENDING','APPROVED','HIDDEN','REJECTED') NOT NULL DEFAULT 'PENDING',
  `category_id` int(10) UNSIGNED DEFAULT NULL,
  `manufacturer_id` int(11) NOT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `images` text DEFAULT NULL,
  `moq` varchar(100) DEFAULT NULL,
  `moq_new` int(10) UNSIGNED DEFAULT NULL,
  `production_capacity` varchar(100) DEFAULT NULL,
  `base_price` decimal(10,2) DEFAULT NULL,
  `currency` varchar(10) DEFAULT 'IDR',
  `is_active` tinyint(1) DEFAULT 1,
  `is_featured` tinyint(1) DEFAULT 0,
  `slug` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `custom_taxonomy` varchar(100) DEFAULT NULL COMMENT 'Custom product taxonomy/tag',
  `badges` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Array of badges' CHECK (json_valid(`badges`)),
  `is_tax_included` tinyint(1) DEFAULT 0,
  `is_transport_included` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `product_code`, `name`, `code`, `series`, `description`, `category`, `status`, `category_id`, `manufacturer_id`, `image_url`, `images`, `moq`, `moq_new`, `production_capacity`, `base_price`, `currency`, `is_active`, `is_featured`, `slug`, `created_at`, `updated_at`, `custom_taxonomy`, `badges`, `is_tax_included`, `is_transport_included`) VALUES
(25, 'AP-MX-01', 'AP Max', '', NULL, 'Size Range: 39-43 EU; Weight: Approx. 1.5 kg per pair; Packaging: Box dimensions approx. 35cm x 30cm x 15cm (estimated)\n\nMaterial: High-quality PVC/Rubber Upper\nOutsole: Nitrile Rubber (Oil and Slip Resistant)\nSafety Standard: EN 20345\nToe Protection: Protective Toe Cap (Withstands up to 200 Joules impact)\nDesign: Lace-up Ankle Boot, Hiking style\nColors: Black/Grey\nSizes: 39 - 43 (French Sizing)\nFeatures: Waterproof, Oil Resistant, Anti-Slip\nUnique Selling Points (USP)\n✓\nHybrid design combining the durability of PVC boots with the style and fit of hiking safety shoes\n✓\nCertified safety protection (200J toe cap) at a competitive price point compared to leather boots\n✓\n\'Safety to the Max\' reinforced construction for harsh industrial environments\n✓\nErgonomic footbed with wide cleated sole for superior traction on wet or uneven terrain', 'Safety Footwear', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b103b6d13604.65623585.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b103b6d13604.65623585.webp\"]', '100', 120, '', 311000.00, 'USD', 1, 0, 'ap-max', '2026-01-12 06:05:57', '2026-03-11 05:55:04', '', NULL, 0, 0),
(31, 'AP-AB-01', 'AP All Bike', '', NULL, 'Material: High-quality PVC / Polymer (One-piece injection molded)\nSize Range: EU 38-43\nColors: Black/Red, Black/Green, Black/Orange, Grey/Black\nConstruction: Seamless injection molding (no glue/stitches)\nProperties: 100% Waterproof material, Oil-resistant sole', 'Safety Footwear', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b103e26a3455.45462166.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b103e26a3455.45462166.webp\"]', '100', 100, '', 63000.00, 'USD', 1, 0, 'ap-all-bike', '2026-01-14 06:21:08', '2026-03-18 07:44:53', '', '[\"READY_STOCK\"]', 1, 1),
(32, 'AP-BW-01', 'AP Black & White Series Long', '', NULL, 'Material: High-quality PVC / Polymer (One-piece injection molded)\nSize Range: EU 38-43\nColors: Black/Red, Black/Green, Black/Orange, Grey/Black\nConstruction: Seamless injection molding (no glue/stitches)\nProperties: 100% Waterproof material, Oil-resistant sole\n\n\n✓ Integrated air ventilation system to prevent humidity buildup\n✓ Seamless construction increases durability and water resistance\n✓ Specialized oil-resistant sole prevents slipping on wet/oily surfaces\n✓ Lightweight design for commuter and rider comfort\n✓ Easy-to-clean polymer material', 'Safety Footwear', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b1045a6f2283.07679432.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b1045a6f2283.07679432.webp\"]', '100', 100, '', 78000.00, 'USD', 1, 0, 'ap-black-white-series-long', '2026-01-14 06:23:47', '2026-03-11 05:58:15', '', NULL, 0, 0),
(33, 'AP-BL-01', 'AP Bola Series', '', NULL, 'AP For Football activity and rubber PVC for comfort', 'Other', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b104465dfda8.40540564.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b104465dfda8.40540564.webp\"]', '100', 100, '', 247000.00, 'USD', 1, 0, 'ap-bola-series', '2026-01-14 06:25:07', '2026-03-11 05:57:27', '', NULL, 0, 0),
(35, 'AP-MD-01', 'AP Medic', '', NULL, 'Material: Rubbertech (proprietary rubber formulation, 100% PVC-free)\nInsole: Ortholite Footbed (removable, breathable, moisture-wicking)\nTemperature Resistance: Usable from -20°C up to 120°C (Autoclave compatible)\nSafety Standards: Anti-slip certified (Class C + D condition), Anti-static protection\nChemical Resistance: Resistant to acids, detergents, and medical fluids\nSize Range: EU 36 to 45 (Outsole lengths 23.3cm - 29.3cm)\nColors: Green, White, Blue (standard); Purple, Pink, Black (select variants)\n\n✓ Autoclavable Sterilization: Can be sterilized in autoclaves or washing machines up to 120°C, ensuring maximum hygiene.\n✓ Anti-Static Technology: Dissipates static electricity, making it safe for use around sensitive medical equipment like MRI and CT scanners.\n✓ Ergonomic Comfort: Features Ortholite footbeds and an ergonomic design to stimulate blood flow and reduce back fatigue during long shifts.\n✓ Eco-Friendly Composition: Made from Rubbertech, which is recyclable, lighter than PVC, and causes no skin irritation.\n✓ Superior Grip: Highest level anti-slip rating ensures safety on wet or slippery hospital floors.', 'Safety Footwear', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b1040d6a9f04.41646303.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b1040d6a9f04.41646303.webp\"]', '100', 99, '', 344000.00, 'USD', 1, 0, 'ap-medic', '2026-01-14 06:35:50', '2026-03-11 05:56:30', '', NULL, 0, 0),
(36, 'APB-S5-03', 'AP BOOTS SAFETY S5 YELLOW', '', NULL, 'AP Boots Safety S5 Yellow\nDimensions & Specs\nBoot Height: 38-40 cm; Outsole Length: 25.5 cm (Size 39) to 32.5 cm (Size 46); Single Box Approx: 35 cm x 30 cm x 12 cm\n\nMaterial: High-quality Rubber PVC (Polyvinyl Chloride)\nSafety Standard: EN 20345 S5 Certified (International Standard)\nToe Protection: Steel Toe Cap (Impact resistance up to 200 Joules)\nMidsole Protection: Steel Midsole (Penetration resistant)\nLining: Oeko-Tex Standard certified textile (Free from harmful chemicals)\nFeatures: Waterproof (WRU), Oil Resistant (FO), Anti-static, Energy Absorption Heel\nVisibility: Equipped with 3M Scotchlite reflective material at the heel\nSize Range: EU 39 - 46\nWeight: Approx. 2.0 kg - 2.3 kg per pair\n\n✓ First safety boot in Indonesia to achieve S5 certification, offering the highest level of waterproof protection with puncture resistance.\n✓ Integrated 3M Scotchlite reflective strip significantly enhances visibility in low-light mining and construction environments.\n✓ Oeko-Tex certified inner lining ensures hypoallergenic comfort and safety, a unique feature for industrial footwear.\n✓ Dual-protection system (Steel Toe + Steel Midsole) provides comprehensive defense against both falling heavy objects and sharp hazards on the ground.\n✓ Anti-fungal treatment and heavy-duty PVC construction ensure longevity and hygiene in harsh, wet working conditions.', 'Safety Footwear', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b103892830b6.06120358.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b103892830b6.06120358.webp\"]', '100', 100, '', 288000.00, 'USD', 1, 0, 'ap-boots-safety-s5-yellow', '2026-01-14 06:56:43', '2026-03-18 07:45:02', '', '[]', 1, 1),
(37, 'APB-S5-02', 'Ap Boots Safety S5 Black', '', NULL, 'AP Boots Safety S5 Black\nDimensions & Specs\nBoot Height: 38-40 cm; Outsole Length: 25.5 cm (Size 39) to 32.5 cm (Size 46); Single Box Approx: 35 cm x 30 cm x 12 cm\n\nMaterial: High-quality Rubber PVC (Polyvinyl Chloride)\nSafety Standard: EN 20345 S5 Certified (International Standard)\nToe Protection: Steel Toe Cap (Impact resistance up to 200 Joules)\nMidsole Protection: Steel Midsole (Penetration resistant)\nLining: Oeko-Tex Standard certified textile (Free from harmful chemicals)\nFeatures: Waterproof (WRU), Oil Resistant (FO), Anti-static, Energy Absorption Heel\nVisibility: Equipped with 3M Scotchlite reflective material at the heel\nSize Range: EU 39 - 46\nWeight: Approx. 2.0 kg - 2.3 kg per pair\n\n✓ First safety boot in Indonesia to achieve S5 certification, offering the highest level of waterproof protection with puncture resistance.\n✓ Integrated 3M Scotchlite reflective strip significantly enhances visibility in low-light mining and construction environments.\n✓ Oeko-Tex certified inner lining ensures hypoallergenic comfort and safety, a unique feature for industrial footwear.\n✓ Dual-protection system (Steel Toe + Steel Midsole) provides comprehensive defense against both falling heavy objects and sharp hazards on the ground.\n✓ Anti-fungal treatment and heavy-duty PVC construction ensure longevity and hygiene in harsh, wet working conditions.', 'Safety Footwear', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b10374f08999.31544082.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b10374f08999.31544082.webp\"]', '100', 100, '', 288000.00, 'USD', 1, 0, 'ap-boots-safety-s5-black', '2026-01-14 08:36:28', '2026-03-18 07:45:09', '', '[\"READY_STOCK\"]', 1, 1),
(38, 'APB-KD-01', 'AP Kids Safari Series', '', NULL, 'AP Kids Safari\nDimensions & Specs\nBoot Height: ~18 cm; Outsole Length: 16.5 cm - 20 cm depending on size; Packaging: Standard carton quantities (typically 12 or 24 pairs per master carton for wholesale)\n\nMaterial: High-quality PVC (Polyvinyl Chloride) / Rubber\nSize Range: EU 22 - 28\nDesigns/Themes: Safari Animals (Zebra, Giraffe, Crocodile, Elephant, Pony, Duck, Rabbit)\nHeight: Approximately 18 cm (varies slightly by size)\nOutsole Length: 16.5 cm (Size 22) to 20 cm (Size 28)\nConstruction: Injection molded, seamless waterproof body\nUnique Selling Points (USP)\n✓\n100% Waterproof and mud-proof, ideal for outdoor play and rainy seasons\n✓ Vibrant, child-friendly animal character designs (Safari theme)\n✓ Flexible and lightweight PVC material ensures comfort for active children\n✓ Anti-slip outsole designed for safety on wet and slippery surfaces\n✓ Easy to clean and quick-drying\n✓ Durable construction typical of the AP Bo', 'Safety Footwear', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b10348593061.37072518.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b10348593061.37072518.webp\"]', '100', 100, '', 43000.00, 'USD', 1, 0, 'ap-kids-safari-series', '2026-01-14 08:45:32', '2026-03-11 05:53:13', '', NULL, 0, 0),
(39, 'APB-GR-05', 'AP Go Green 2017', '', NULL, 'Ap Go Green Adalah AP Varian Terbaru dengna Fitur Keamana Baru yang lebih mutahir', 'Safety Footwear', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b10326cf1342.70142068.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b10326cf1342.70142068.webp\"]', '100', 108, '', 107000.00, 'USD', 1, 0, 'ap-go-green-2017', '2026-01-19 07:55:55', '2026-03-11 05:52:40', '', NULL, 0, 0),
(40, 'APB-MT-03', 'AP Moto 3', '', NULL, 'AP Moto 3 For Motorbike Safety', 'Safety Footwear', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b102ec94f033.39730879.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b102ec94f033.39730879.webp\"]', '100', 120, '100000', 127000.00, 'USD', 1, 0, 'ap-moto-3', '2026-01-19 10:54:20', '2026-03-11 05:51:42', '', NULL, 0, 0),
(42, 'APB-MG-02', 'AP Metaguard Black', '', NULL, 'Height: ~35 cm to 38.5 cm (varies by size); Outsole Length: 26 cm (Size 39) to 29.5 cm (Size 43); Size Range: EU 39 - 43\r\n\r\nMaterial: High-quality PVC and Rubber blend (Waterproof and Oil Resistant)\r\nToe Protection: Steel Toe Cap (Impact resistance up to 200 Joules)\r\nMetatarsal Protection: Integrated Metaguard flap for instep protection\r\nSafety Standard Compliance: EN 20345 (Safety Footwear), ASTM F2413 (implied by design class)\r\nLining: Textile lining with \'Sanitized\' anti-bacterial treatment\r\nCertification: Oeko-Tex Standard 100 (Free from harmful chemicals)\r\nOutsole: Anti-slip, abrasion-resistant, and oil-resistant PVC/Nitrile sole\r\nTemperature Resistance: Some vendor listings claim outsole resistance up to 300°C (verify specific batch/model data)\r\nColor: Available in Black and Yellow options\r\nVisibility: 3M Scotchlite reflective strip on the heel\r\n\r\nDual Safety Standards: Combines heavy-duty physical protection (Steel Toe + Metaguard) with chemical safety certifications (Oeko-Tex).\r\n✓\r\nHygiene Focus: Features \'Sanitized\' anti-microbial technology to prevent odors and fungal growth during prolonged wear.\r\n✓\r\nErgonomic Fit: Designed with a wider fit to accommodate the Asian foot shape comfortably compared to Western imports.', 'Safety Footwear', 'PENDING', 1, 28, 'https://hotstrading.com/backend/uploads/img_69b1022674cd20.10482946.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69b1022674cd20.10482946.webp\"]', '100', NULL, '', 260000.00, 'IDR', 1, 0, 'ap-metaguard-black', '2026-03-03 03:15:17', '2026-03-18 07:45:18', '', '[\"HOT_DEAL\",\"READY_STOCK\"]', 1, 1),
(43, 'APB-CL-01-37', 'AP CLOGS ( WARNA)', 'APB-CL-01-37', NULL, 'Produk AP CLOGS ( WARNA). Specs: Waterproof; Anti-Slip; Desain Clogs Slip-on. Ket: HITAM, COKLAT, BIRU, PUTIH, ABU-ABU', 'Safety Footwear', 'PENDING', 1, 28, 'https://down-id.img.susercontent.com/file/id-11134207-7r98s-ln9hyj5u3659c6', '[\"https:\\/\\/down-id.img.susercontent.com\\/file\\/id-11134207-7r98s-ln9hyj5u3659c6\"]', '250', 250, '', 52000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-18 06:24:13', '', '[]', 1, 1),
(44, 'APB-CL-02-37', 'AP CLOGS ( WHITE, PINK )', 'APB-CL-02-37', NULL, 'Produk AP CLOGS ( WHITE, PINK ). Specs: Waterproof; Anti-Slip; Desain Clogs Slip-on. Ket: PUTIH , PINK', 'Safety Footwear', 'PENDING', NULL, 28, 'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/img/VqbcmM/2022/5/21/5de165d7-b245-4b9d-87cc-e5c99de37621.jpg~tplv-aphluv4xwc-resize-jpeg:700:0.jpg', '[\"https:\\/\\/p16-oec-sg.ibyteimg.com\\/tos-alisg-i-aphluv4xwc-sg\\/img\\/VqbcmM\\/2022\\/5\\/21\\/5de165d7-b245-4b9d-87cc-e5c99de37621.jpg~tplv-aphluv4xwc-resize-jpeg:700:0.jpg\"]', '250', 250, '', 53000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-18 03:03:43', '', NULL, 0, 0),
(49, 'APB-BW-01-37', 'AP BLACK ( I )', 'APB-BW-01-37', NULL, 'Produk AP BLACK ( I ). Specs: Boot Pendek; Heavy Duty; Tahan Lumpur. Ket: HITAM PENDEK', 'Safety Footwear', 'PENDING', NULL, 28, 'https://down-id.img.susercontent.com/file/f2a69ff58a5cd9cc5f41a21c9d499957', '[\"https:\\/\\/down-id.img.susercontent.com\\/file\\/f2a69ff58a5cd9cc5f41a21c9d499957\"]', '250', 250, '', 67000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-18 07:44:04', '', '[\"READY_STOCK\"]', 0, 0),
(50, 'APB-BW-02-37', 'AP WHITE ( I )', 'APB-BW-02-37', NULL, 'Produk AP WHITE ( I ). Specs: Boot Panjang; Waterproof; Konstruksi PVC Kokoh. Ket: PUTIH PENDEK', 'Safety Footwear', 'PENDING', NULL, 28, 'https://down-id.img.susercontent.com/file/f6e56093fb9764df06a274a5efc3cdb2', '[\"https:\\/\\/down-id.img.susercontent.com\\/file\\/f6e56093fb9764df06a274a5efc3cdb2\"]', '250', 250, '', 78000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-18 07:43:54', '', '[\"HOT_DEAL\",\"READY_STOCK\"]', 0, 0),
(51, 'APB-BW-03-37', 'AP BLACK ( II )', 'APB-BW-03-37', NULL, 'Produk AP BLACK ( II ). Specs: Boot Panjang; Waterproof; Konstruksi PVC Kokoh. Ket: HITAM PANJANG', 'Safety Footwear', 'PENDING', NULL, 28, 'https://down-id.img.susercontent.com/file/id-11134207-7r98r-ln2ol679zggc1e', '[\"https:\\/\\/down-id.img.susercontent.com\\/file\\/id-11134207-7r98r-ln2ol679zggc1e\"]', '250', 250, '', 78000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-18 03:10:48', '', NULL, 0, 0),
(52, 'APB-BW-04-37', 'AP BLACK III', 'APB-BW-04-37', NULL, 'Produk AP BLACK ( III ) & (V). Specs: Boot Panjang; Waterproof; Konstruksi PVC Kokoh. Ket: HITAM PENDEK', 'Safety Footwear', 'HIDDEN', NULL, 28, 'https://down-id.img.susercontent.com/file/id-11134207-7r98w-ln2op5ayklfz82', '[\"https:\\/\\/down-id.img.susercontent.com\\/file\\/id-11134207-7r98w-ln2op5ayklfz82\"]', '250', 250, '', 70000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-18 07:43:47', '', '[]', 0, 0),
(53, 'APB-GR-01', '2005 GREEN', 'APB-GR-01', NULL, 'Produk 2005 GREEN. Specs: Shaft Tinggi; Proteksi Kaki Maksimal. Ket: HIJAU PENDEK', 'Safety Footwear', 'HIDDEN', NULL, 28, 'https://down-id.img.susercontent.com/file/sg-11134201-7rbmt-loxgw372z82t2e.webp', '[\"https:\\/\\/down-id.img.susercontent.com\\/file\\/sg-11134201-7rbmt-loxgw372z82t2e.webp\"]', '250', 250, '', 63000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-18 07:43:39', '', '[]', 0, 0),
(54, 'APB-GR-02', '2005 + MOTIF', 'APB-GR-02', NULL, 'Produk 2005 + MOTIF. Specs: Shaft Tinggi; Proteksi Kaki Maksimal. Ket: MOTIF PENDEK', 'Safety Footwear', 'HIDDEN', NULL, 28, 'https://hotstrading.com/backend/uploads/img_69ba36432daf09.66818432.webp', '[\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69ba36432daf09.66818432.webp\",\"https:\\/\\/hotstrading.com\\/backend\\/uploads\\/img_69ba36463e25a8.84331994.webp\"]', '250', 250, '', 84000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-18 07:43:31', '', '[]', 0, 0),
(55, 'APB-GR-03', '2007 GREEN', 'APB-GR-03', NULL, 'Produk 2007 GREEN. Specs: Shaft Tinggi; Proteksi Kaki Maksimal. Ket: HIJAU PENDEK', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 84000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(56, 'APB-GR-04', '2011 GREEN', 'APB-GR-04', NULL, 'Produk 2011 GREEN. Specs: Shaft Tinggi; Proteksi Kaki Maksimal. Ket: HIJAU PANJANG UNTUK WANITA', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 84000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(57, 'APB-GR-06', '2017 GREEN LIME', 'APB-GR-06', NULL, 'Produk 2017 GREEN LIME. Specs: Shaft Tinggi; Proteksi Kaki Maksimal. Ket: HIJAU LEMON PANJANG', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 108000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(58, 'APB-GR-07', '2017 GREEN TOSCA', 'APB-GR-07', NULL, 'Produk 2017 GREEN TOSCA. Specs: Shaft Tinggi; Proteksi Kaki Maksimal. Ket: HIJAU TOSCA PANJANG', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 108000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(59, 'APB-GR-08', '9905 BLACK', 'APB-GR-08', NULL, 'Produk 9905 BLACK. High-quality PVC Boots. Ket: HITAM PANJANG (SOL HITAM )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 104000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(60, 'APB-MT-01', 'AP MOTO (I) BLACK / RED', 'APB-MT-01', NULL, 'Produk AP MOTO (I) BLACK / RED. High-quality PVC Boots. Ket: HITAM - SOL MERAH', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 115000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(61, 'APB-MT-02', 'AP MOTO (II) BLACK / RED', 'APB-MT-02', NULL, 'Produk AP MOTO (II) BLACK / RED. High-quality PVC Boots. Ket: HITAM - SOL MERAH', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 121000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(62, 'APB-93-01', '9303 GREEN', 'APB-93-01', NULL, 'Produk 9303 GREEN. High-quality PVC Boots. Ket: HIJAU PANJANG', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 118000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(63, 'APB-93-02', '9303 GREEN', 'APB-93-02', NULL, 'Produk 9303 GREEN. High-quality PVC Boots. Ket: HIJAU PANJANG (EXTRA LARGE )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 120000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(64, 'APB-XT-01', 'AP XT', 'APB-XT-01', NULL, 'Produk AP XT. High-quality PVC Boots. Ket: HIJAU PANJANG (SOL PENTHEL )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 118000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(65, 'APB-95-01', '9506 GREEN', 'APB-95-01', NULL, 'Produk 9506 GREEN. High-quality PVC Boots. Ket: HIJAU PANJANG', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 132000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(66, 'APB-03-01', '2003 GREEN', 'APB-03-01', NULL, 'Produk 2003 GREEN. High-quality PVC Boots. Ket: HIJAU PANJANG (TRI-WARNA )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 138000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(67, 'APB-06-01', '2006 GREEN', 'APB-06-01', NULL, 'Produk 2006 GREEN. High-quality PVC Boots. Ket: HIJAU PANJANG (TRI-WARNA )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 140000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(68, 'APB-15-01', '2015 GREEN', 'APB-15-01', NULL, 'Produk 2015 GREEN. High-quality PVC Boots. Ket: HIJAU PANJANG (EMPAT-WARNA )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 144000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(69, 'APB-15-02', '2015 GREY', 'APB-15-02', NULL, 'Produk 2015 GREY. High-quality PVC Boots. Ket: GREY PANJANG (EMPAT-WARNA )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 144000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(70, 'APB-15-03', '2015 ORANGE', 'APB-15-03', NULL, 'Produk 2015 ORANGE. High-quality PVC Boots. Ket: ORANGE PANJANG (EMPAT-WARNA )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 144000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(71, 'APB-15-04', '2015 BLACK', 'APB-15-04', NULL, 'Produk 2015 BLACK. High-quality PVC Boots. Ket: HITAM PANJANG (EMPAT-WARNA )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 144000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(72, 'APB-18-01', '2018 ULTRAFLEX GREEN', 'APB-18-01', NULL, 'Produk 2018 ULTRAFLEX GREEN. Specs: Material Ultra Fleksibel; Empat Warna. Ket: HIJAU PANJANG (EMPAT-WARNA )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 161000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(73, 'APB-18-02', '2018 ULTRAFLEX GREY', 'APB-18-02', NULL, 'Produk 2018 ULTRAFLEX GREY. Specs: Material Ultra Fleksibel; Empat Warna. Ket: GREY PANJANG (EMPAT-WARNA )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 161000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(74, 'APB-S4-01', 'TERRA SAFETY S4 YELLOW', 'APB-S4-01', NULL, 'Produk TERRA SAFETY S4 YELLOW. Specs: Steel Toe Cap (200J); EN ISO 20345 S4. Ket: KUNING PANJANG ( SAFETY + TOE CAP )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 253000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(78, 'APB-CF-01', 'AP CHEF BLACK/WHITE', 'APB-CF-01', NULL, 'Produk AP CHEF BLACK/WHITE. Specs: Anti-Slip Superior; Insole Ortholite. Ket: HITAM PUTIH', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 229000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(79, 'APB-MD-01', 'AP MEDIC BLUE/GREEN/WHITE', 'APB-MD-01', NULL, 'Produk AP MEDIC BLUE/GREEN/WHITE. Specs: Sterilisasi Autoclave; Material Higienis. Ket: WARNA', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 344000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(80, 'APB-TC-01', 'TERRA ECO 1 BL', 'APB-TC-01', NULL, 'Produk TERRA ECO 1 BL. High-quality PVC Boots. Ket: HITAM PENDEK', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 64000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(81, 'APB-TC-02', 'TERRA ECO 2 BL', 'APB-TC-02', NULL, 'Produk TERRA ECO 2 BL. High-quality PVC Boots. Ket: HITAM PANJANG', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 75000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(82, 'APB-TC-03', 'TERRA ECO 3 BL', 'APB-TC-03', NULL, 'Produk TERRA ECO 3 BL. Specs: Sol Penthel (Mud Cleaning); Ekonomis. Ket: HITAM PANJANG SOL PENTHEL', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 97000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(83, 'APB-TC-04', 'TERRA ECO 3 GR/YL/OR', 'APB-TC-04', NULL, 'Produk TERRA ECO 3 GR/YL/OR. Specs: Sol Penthel (Mud Cleaning); Ekonomis. Ket: HIJAU/KUNIING/ORANGE PANJANG SOL PENTHEL', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 102000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(84, 'APB-TC-05', 'TERRA ECO 5 GR', 'APB-TC-05', NULL, 'Produk TERRA ECO 5 GR. High-quality PVC Boots. Ket: HIJAU PENDEK SOL PENTHEL', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 75000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(85, 'APB-TC-06', 'TERRA ECO 5 WH', 'APB-TC-06', NULL, 'Produk TERRA ECO 5 WH. High-quality PVC Boots. Ket: PUTIH PENDEK SOL PENTHEL', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 69000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(86, 'APB-TG-01', 'TERRA GP BL', 'APB-TG-01', NULL, 'Produk TERRA GP BL. High-quality PVC Boots. Ket: HITAM PANJANG', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 67000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(87, 'APB-TG-02', 'TERRA GP GR', 'APB-TG-02', NULL, 'Produk TERRA GP GR. High-quality PVC Boots. Ket: HIJAU PANJANG (SOL HITAM)', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 78000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(88, 'APB-T5-01', 'TERRA 5 GR', 'APB-T5-01', NULL, 'Produk TERRA 5 GR. High-quality PVC Boots. Ket: HIJAU PANJANG SOL PENTHEL', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 109000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(89, 'APB-T3-01', 'TERRA 3 BL/YL', 'APB-T3-01', NULL, 'Produk TERRA 3 BL/YL. High-quality PVC Boots. Ket: HITAM PANJANG (SOL KUNING )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 104000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(90, 'APB-T3-02', 'TERRA 3 GR - RED', 'APB-T3-02', NULL, 'Produk TERRA 3 GR - RED. High-quality PVC Boots. Ket: HIJAU PANJANG (SOL MERAH )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 110000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(91, 'APB-T2-01', 'TERRA 2 GR', 'APB-T2-01', NULL, 'Produk TERRA 2 GR. High-quality PVC Boots. Ket: HIJAU PANJANG (SOL PENTHEL )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 112000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(92, 'APB-TG-03', 'TERRA GR/WH/YL', 'APB-TG-03', NULL, 'Produk TERRA GR/WH/YL. High-quality PVC Boots. Ket: HIJAU, PUTIH, KUNING PANJANG', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 118000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(93, 'APB-TA-01', 'TERRA ARMY', 'APB-TA-01', NULL, 'Produk TERRA ARMY. High-quality PVC Boots. Ket: ARMY PANJANG', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 138000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(94, 'APB-TF-01', 'TERRA FOREST', 'APB-TF-01', NULL, 'Produk TERRA FOREST. High-quality PVC Boots. Ket: FOREST PANJANG', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 138000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(95, 'APB-OR-01', 'ORCA GR', 'APB-OR-01', NULL, 'Produk ORCA GR. High-quality PVC Boots. Ket: HIJAU PANJANG SOL PENTHEL', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 94000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(96, 'APB-OR-02', 'ORCA BR', 'APB-OR-02', NULL, 'Produk ORCA BR. High-quality PVC Boots. Ket: COKLAT PANJANG SOL PENTHEL', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 76000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(97, 'APB-B1-01', '961 / 967 BL', 'APB-B1-01', NULL, 'Produk 961 / 967 BL. Specs: Sepatu Capung; Sangat Ringan; Fleksibel. Ket: AP BOLA HITAM (BESAR )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 247000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(98, 'APB-B3-01', '963 BL', 'APB-B3-01', NULL, 'Produk 963 BL. High-quality PVC Boots. Ket: AP BOLA HITAM (TANGGUNG )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 236000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(99, 'APB-B3-02', '963 / 965 WH', 'APB-B3-02', NULL, 'Produk 963 / 965 WH. Specs: Sepatu Capung; Sangat Ringan; Fleksibel. Ket: AP BOLA PUTIH (BESAR )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 403000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(100, 'APB-B3-03', '963 WH', 'APB-B3-03', NULL, 'Produk 963 WH. High-quality PVC Boots. Ket: AP BOLA PUTIH (TANGGUNG )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 368000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(101, 'APB-B3-04', '963 CR', 'APB-B3-04', NULL, 'Produk 963 CR. Specs: Sepatu Capung; Sangat Ringan; Fleksibel. Ket: AP BOLA CREAM (BESAR )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 414000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(102, 'APB-B6-01', '969 WH', 'APB-B6-01', NULL, 'Produk 969 WH. Specs: Sepatu Capung; Sangat Ringan; Fleksibel. Ket: AP BOLA PUTIH 2 WARNA (BESAR )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 449000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(103, 'APB-B6-02', '969 BL', 'APB-B6-02', NULL, 'Produk 969 BL. Specs: Sepatu Capung; Sangat Ringan; Fleksibel. Ket: AP BOLA HITAM 2 WARNA (BESAR )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 357000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(104, 'APB-VT-01', '985 BL', 'APB-VT-01', NULL, 'Produk 985 BL. High-quality PVC Boots. Ket: VAN SLOP HITAM', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 247000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(105, 'APB-VT-02', '987/989 /991/995/997/1001 BL', 'APB-VT-02', NULL, 'Produk 987/989 /991/995/997/1001 BL. High-quality PVC Boots. Ket: VAN SANDAL HITAM', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 247000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(106, 'APB-VT-03', '999 BL', 'APB-VT-03', NULL, 'Produk 999 BL. High-quality PVC Boots. Ket: VAN SANDAL HITAM', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 270000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(107, 'APB-VT-04', '977 BL', 'APB-VT-04', NULL, 'Produk 977 BL. High-quality PVC Boots. Ket: VAN SEPATU KANTOR HITAM', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 305000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(108, 'APB-VT-05', '1003 BL', 'APB-VT-05', NULL, 'Produk 1003 BL. High-quality PVC Boots. Ket: VAN SEPATU KANTOR HITAM', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 305000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(109, 'APB-ST-01', 'AP STAR BLACK/WHITE 38-42', 'APB-ST-01', NULL, 'Produk AP STAR BLACK/WHITE 38-42. Specs: Desain Casual/Sekolah; Material Karet. Ket: VAN SEPATU SEKOLAH HITAM (SOLE PUTIH )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 63000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(110, 'APB-ST-02', 'AP STAR BLACK/CAMEL 38-42', 'APB-ST-02', NULL, 'Produk AP STAR BLACK/CAMEL 38-42. Specs: Desain Casual/Sekolah; Material Karet. Ket: VAN SEPATU SEKOLAH HITAM (SOLE COMEL )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 63000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(111, 'APB-ST-03', 'AP STAR NAVY/WHITE 38-42', 'APB-ST-03', NULL, 'Produk AP STAR NAVY/WHITE 38-42. Specs: Desain Casual/Sekolah; Material Karet. Ket: VAN SEPATU SEKOLAH NAVY (SOLE PUTIH )', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 63000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(112, 'APB-ST-04', 'AP STAR BLACK/BLACK 38-42', 'APB-ST-04', NULL, 'Produk AP STAR BLACK/BLACK 38-42. Specs: Desain Casual/Sekolah; Material Karet. Ket: VAN SEPATU SEKOLAH HITAM', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 61000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(113, 'APB-WK-01', 'HOBBY & WORK BLACK/RED', 'APB-WK-01', NULL, 'Produk HOBBY & WORK BLACK/RED. High-quality PVC Boots. Ket: VAN SEPATU KANTOR HITAM (SOLE MERAH)', 'Safety Footwear', 'PENDING', NULL, 28, 'https://down-id.img.susercontent.com/file/sg-11134201-7rbku-lngp05oytf0ifd', '[\"https:\\/\\/down-id.img.susercontent.com\\/file\\/sg-11134201-7rbku-lngp05oytf0ifd\",\"https:\\/\\/down-id.img.susercontent.com\\/file\\/id-11134207-7r98t-ln9ifgjacd6d21\"]', '250', 250, '', 75000.00, 'IDR', 0, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 06:09:44', '', NULL, 0, 0),
(114, 'APB-KD-02', '9307 W', 'APB-KD-02', NULL, 'Produk 9307 W. Specs: Motif Karakter/Binatang; Warna Cerah. Ket: ANAK-ANAK KECIL', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 44000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(115, 'APB-KD-03', 'GRANDPRIX', 'APB-KD-03', NULL, 'Produk GRANDPRIX. Specs: Motif Karakter/Binatang; Warna Cerah. Ket: ANAK-ANAK KECIL', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 45000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(116, 'APB-KD-04', '9309 W', 'APB-KD-04', NULL, 'Produk 9309 W. Specs: Motif Karakter/Binatang; Warna Cerah. Ket: WARNA ANAK-ANAK BESAR', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 49000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(117, 'APB-KD-05', '2001 W', 'APB-KD-05', NULL, 'Produk 2001 W. Specs: Motif Karakter/Binatang; Warna Cerah. Ket: WARNA TANGGUNG PENDEK', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 67000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(118, 'APB-KD-06', '2001 GR', 'APB-KD-06', NULL, 'Produk 2001 GR. Specs: Motif Karakter/Binatang; Warna Cerah. Ket: HIJAU TANGGUNG PENDEK', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 69000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(119, 'APB-KD-07', '2001 ROOT N LEAVES', 'APB-KD-07', NULL, 'Produk 2001 ROOT N LEAVES. Specs: Motif Karakter/Binatang; Warna Cerah. Ket: ROOT N LEAVES TANGGUNG PENDEK', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 86000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0),
(121, 'APB-KD-09', 'AP JASMINE', 'APB-KD-09', NULL, 'Produk AP JASMINE. Specs: Motif Karakter/Binatang; Warna Cerah. Ket: PATTERN BONEKA UNTUK ANAK-ANAK KECIL', NULL, 'HIDDEN', NULL, 28, NULL, NULL, '250', 250, NULL, 63000.00, 'IDR', 1, 0, NULL, '2026-03-16 02:33:29', '2026-03-17 04:43:54', NULL, NULL, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `product_certifications`
--

CREATE TABLE `product_certifications` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `certification_name` varchar(255) NOT NULL,
  `certification_number` varchar(100) DEFAULT NULL,
  `issued_date` date DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `document_url` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_regions`
--

CREATE TABLE `product_regions` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `region` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_specifications`
--

CREATE TABLE `product_specifications` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `spec_label` varchar(100) NOT NULL,
  `spec_value` varchar(255) NOT NULL,
  `display_order` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_use_cases`
--

CREATE TABLE `product_use_cases` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `use_case` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `quotations`
--

CREATE TABLE `quotations` (
  `id` int(11) NOT NULL,
  `quotation_number` varchar(50) NOT NULL,
  `distributor_id` int(11) NOT NULL,
  `manufacturer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `target_price` decimal(10,2) DEFAULT NULL,
  `total_price` decimal(15,2) DEFAULT NULL,
  `admin_fee` decimal(15,2) DEFAULT 0.00,
  `tax_amount` decimal(15,2) DEFAULT 0.00,
  `logistics_cost` decimal(15,2) DEFAULT 0.00,
  `final_price` decimal(15,2) DEFAULT NULL,
  `currency` varchar(10) DEFAULT 'USD',
  `delivery_location` varchar(255) DEFAULT NULL,
  `delivery_deadline` date DEFAULT NULL,
  `quoted_price` decimal(10,2) DEFAULT NULL,
  `quoted_moq` int(11) DEFAULT NULL,
  `validity_days` int(11) DEFAULT 7,
  `seller_notes` text DEFAULT NULL,
  `admin_notes` text DEFAULT NULL,
  `quoted_delivery_time` varchar(100) DEFAULT NULL,
  `manufacturer_notes` text DEFAULT NULL,
  `status` enum('PENDING','QUOTED','ADMIN_REVIEW','ACCEPTED','REJECTED','EXPIRED') DEFAULT 'PENDING',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `responded_at` timestamp NULL DEFAULT NULL,
  `migrated_to_items` tinyint(1) NOT NULL DEFAULT 0,
  `expired_at` datetime DEFAULT NULL COMMENT 'Waktu quotation di-expire oleh sistem',
  `notes` text DEFAULT NULL COMMENT 'Catatan khusus dari buyer',
  `delivery_timeline` varchar(100) DEFAULT NULL COMMENT 'Timeline pengiriman yang diinginkan buyer',
  `special_requirements` text DEFAULT NULL COMMENT 'Spesifikasi teknis tambahan'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `quotations`
--

INSERT INTO `quotations` (`id`, `quotation_number`, `distributor_id`, `manufacturer_id`, `product_id`, `quantity`, `target_price`, `total_price`, `admin_fee`, `tax_amount`, `logistics_cost`, `final_price`, `currency`, `delivery_location`, `delivery_deadline`, `quoted_price`, `quoted_moq`, `validity_days`, `seller_notes`, `admin_notes`, `quoted_delivery_time`, `manufacturer_notes`, `status`, `created_at`, `updated_at`, `responded_at`, `migrated_to_items`, `expired_at`, `notes`, `delivery_timeline`, `special_requirements`) VALUES
(5, 'QT-20260303-261D30', 28, 28, 25, 100, NULL, NULL, 0.00, 0.00, 0.00, NULL, 'USD', NULL, NULL, NULL, NULL, 7, NULL, NULL, NULL, NULL, 'PENDING', '2026-03-03 08:44:35', '2026-03-03 08:44:35', NULL, 0, NULL, 'Test RFQ dari halaman /rfq_test', NULL, NULL),
(6, 'QT-20260303-A16729', 28, 28, 25, 100, NULL, NULL, 0.00, 0.00, 0.00, NULL, 'USD', NULL, NULL, 500000.00, 50, 7, NULL, NULL, NULL, NULL, 'QUOTED', '2026-03-03 08:58:56', '2026-03-03 08:59:01', '2026-03-03 08:59:01', 0, NULL, 'Harga sudah termasuk ongkir Jabodetabek', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `quotation_items`
--

CREATE TABLE `quotation_items` (
  `id` int(10) UNSIGNED NOT NULL,
  `quotation_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL COMMENT 'Snapshot',
  `category` varchar(100) DEFAULT NULL COMMENT 'Snapshot',
  `quantity` int(10) UNSIGNED NOT NULL DEFAULT 1,
  `moq` int(10) UNSIGNED DEFAULT NULL COMMENT 'Snapshot',
  `price_per_unit` decimal(15,2) DEFAULT NULL,
  `total_price` decimal(15,2) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `quotation_item_sizes`
--

CREATE TABLE `quotation_item_sizes` (
  `id` int(10) UNSIGNED NOT NULL,
  `quotation_item_id` int(10) UNSIGNED NOT NULL,
  `size` varchar(50) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `rate_limits`
--

CREATE TABLE `rate_limits` (
  `id` int(11) NOT NULL,
  `rate_key` varchar(255) NOT NULL,
  `attempts` int(11) DEFAULT 1,
  `window_start` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `verification_token` varchar(255) DEFAULT NULL,
  `verification_expires_at` timestamp NULL DEFAULT NULL,
  `verification_sent_at` timestamp NULL DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('MANUFACTURER','DISTRIBUTOR','ADMIN','SUPER_ADMIN') NOT NULL DEFAULT 'DISTRIBUTOR',
  `status` enum('PENDING','ACTIVE','SUSPENDED','REJECTED') DEFAULT 'PENDING',
  `company_name` varchar(255) NOT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `industry` varchar(100) DEFAULT NULL,
  `contact_person` varchar(255) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `email_verified` tinyint(1) DEFAULT 0,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL,
  `profile_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`profile_data`)),
  `nib_file` varchar(255) DEFAULT NULL,
  `siup_file` varchar(255) DEFAULT NULL,
  `npwp_file` varchar(255) DEFAULT NULL,
  `verification_status` enum('unverified','pending','verified','rejected') DEFAULT 'unverified',
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `is_hidden` tinyint(1) NOT NULL DEFAULT 0,
  `hidden_reason` text DEFAULT NULL,
  `hidden_at` timestamp NULL DEFAULT NULL,
  `hidden_by` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `fullname`, `verification_token`, `verification_expires_at`, `verification_sent_at`, `password_hash`, `role`, `status`, `company_name`, `slug`, `logo`, `description`, `industry`, `contact_person`, `phone`, `country`, `city`, `address`, `email_verified`, `created_at`, `updated_at`, `last_login`, `profile_data`, `nib_file`, `siup_file`, `npwp_file`, `verification_status`, `email_verified_at`, `is_hidden`, `hidden_reason`, `hidden_at`, `hidden_by`) VALUES
(1, 'admin@hotstrading.com', NULL, NULL, NULL, NULL, '$2y$10$mBEtXqtZmj9CHVXf3a6mEeXEi6Yf5Gy7t/g4XDd/agNYVO5vHxvD.', 'SUPER_ADMIN', 'ACTIVE', 'HOTS Trading', 'hots-trading', NULL, NULL, NULL, 'Admin User', '+62-21-1234567', 'Indonesia', 'Jakarta', NULL, 1, '2026-01-07 04:47:07', '2026-03-12 02:54:54', '2026-03-12 02:54:54', NULL, NULL, NULL, NULL, '', '2026-03-04 02:03:27', 0, NULL, NULL, NULL),
(27, 'contact@apboots.com', NULL, 'f4fb96f1c96a520f54053e0bbe86f32f7e252eded4527c7f19342026c2ff4e80', NULL, NULL, '$2y$10$ZyHL3IG/6JQuz26sb1XJaOegvafq7CaFOj7jsifoLzv1/OOUR38Ai', 'DISTRIBUTOR', 'ACTIVE', 'AP Boots', 'pt-waru-gunung-industry', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUdLQaNmxjTR9SqSdCAcJkRLd4__6xTFvvCQ&s', 'pt-waru-gunung-industry', 'Saferty Boots', '', '081196947711', '', 'Jakarta', 'contact@apboots.com', 1, '2026-01-08 06:24:08', '2026-03-12 07:43:49', '2026-02-09 08:41:25', '{\"board_members\":[],\"website\":\"https:\\/\\/www.apboots.id\\/\",\"social\":{\"linkedin\":\"https:\\/\\/www.linkedin.com\\/\",\"instagram\":\"@krakatau.steel\"}}', NULL, NULL, NULL, 'verified', NULL, 0, NULL, NULL, NULL),
(28, 'warehouse@apboots.com', NULL, '0c85435822337eb67d85485c2d5c7d5813f862ab8ce318a72c9693981ab3b311', '2026-03-06 06:47:13', NULL, '$2y$10$O0CiDCTy3a4Pr8Iqn8Dm3u2H30W8UQfayOxXvIiGwMJWbvtG7LHIy', 'MANUFACTURER', 'ACTIVE', 'PT Waru Gunung Industry', 'pt-waru-gunung-warehouse', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUdLQaNmxjTR9SqSdCAcJkRLd4__6xTFvvCQ&s', 'PT Waru Gunung Industry adalah produsen sepatu, sandal PVC, dan khususnya terkenal dengan merek sepatu bot AP Boots. Perusahaan ini berlokasi di Surabaya, Jawa Timur. \nGambaran Umum Perusahaan\nProduk Utama: Perusahaan ini berspesialisasi dalam produksi sepatu bot hujan PVC, sandal jepit PVC, dan alas kaki lainnya di bawah merek dagang AP Boots.\nLokasi: Kantor pusat dan pabrik berlokasi di Jalan Raya Mastrip No. 858 Karang Pilang, Surabaya, Jawa Timur, Indonesia.\nKontak: Anda dapat mengunjungi situs web resmi mereka di apboots.id atau menghubungi melalui email di sales@apboots.id.\nMedia Sosial: Halaman Facebook mereka tersedia di Sepatu AP Boots - PT. Waru Gunung Industry. \nPerusahaan ini secara aktif merekrut untuk berbagai posisi, termasuk peran di bidang produksi, TI, dan pembelian. ', 'Saferty Boots', '', '08123 123 123', 'Indonesia', 'Surabaya', 'Jl. Raya Mastrip No.858, Warugunung, Kec. Karangpilang, Surabaya, Jawa Timur 60221', 1, '2026-01-08 06:25:01', '2026-03-18 03:00:57', '2026-03-18 03:00:57', '{\"board_members\":[{\"name\":\"John\",\"role\":\"CEO\",\"initials\":\"J\"}],\"website\":\"https:\\/\\/www.apboots.id\\/\",\"social\":{\"linkedin\":\"https:\\/\\/www.linkedin.com\\/in\\/ferry-yonathan-931a75a4\\/?originalSubdomain=id\",\"instagram\":\"https:\\/\\/www.instagram.com\\/apboots\"}}', '/uploads/documents/28_nib_file_1772506465.png', '/uploads/documents/28_siup_file_1772506465.png', '/uploads/documents/28_npwp_file_1772506465.png', 'verified', NULL, 0, NULL, NULL, NULL),
(33, 'admin@warugunung.com', NULL, NULL, NULL, NULL, '$2y$10$yH8.Ma2uM7fnwDayMrubX.BQBMlAgL6Gm8khcPHAA.hpMjk.kl1je', '', '', 'PT Waru Gunung', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2026-01-14 06:06:10', '2026-03-16 01:22:52', NULL, NULL, NULL, NULL, NULL, 'verified', NULL, 0, NULL, NULL, NULL),
(48, 'hotstrading11@gmail.com', NULL, NULL, NULL, NULL, '$2y$10$Q4BL2uWGWVQMb0SnN..zn.ySSwXLYNGY9IR06Hxczhzt4UmRBmF9O', 'SUPER_ADMIN', 'ACTIVE', 'HOTS Trading Super', NULL, NULL, NULL, NULL, NULL, '628111111111', NULL, NULL, NULL, 1, '2026-02-11 07:49:14', '2026-03-16 01:22:57', '2026-03-05 04:32:52', NULL, NULL, NULL, NULL, '', NULL, 0, NULL, NULL, NULL),
(57, 'admin@demo.com', NULL, NULL, NULL, NULL, '$2y$12$6T5jLuU7NaHWQbSvxObQXe7vfItMsJvCPj73s5I1KGlMNoPCHJ2Gq', 'ADMIN', 'ACTIVE', 'HOTS Trading Admin', NULL, NULL, NULL, NULL, NULL, '+62 811 000 0003', 'Indonesia', 'Jakarta', 'Jl. Admin Demo No. 1, Jakarta', 1, '2026-03-03 08:05:48', '2026-03-06 04:55:59', NULL, NULL, NULL, NULL, NULL, '', '2026-03-03 08:05:48', 0, NULL, NULL, NULL),
(64, 'aufatea@gmail.com', NULL, '02d21f5769f1cf88babd416d610cf9dccd0d120a66b903cfc12d8707788f09d5', '2026-03-07 04:00:13', NULL, '$2y$10$NFTIQUK04JpaMJdaGKGEHejUHHQqxsn.rzvqXwVuFnx3FY/NBrUfu', 'DISTRIBUTOR', 'SUSPENDED', '0ppapai', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2026-03-06 04:00:13', '2026-03-11 07:39:27', NULL, NULL, NULL, NULL, NULL, 'unverified', NULL, 0, NULL, NULL, NULL),
(65, 'farhan@hotstrading.com', 'Farhan Aditya', NULL, NULL, NULL, '$2y$10$ifptU3g9q/yXlxfOBZ.fQeB.fKFu3F0zgonvVAmUUTvmqQ6A7PL62', 'SUPER_ADMIN', 'ACTIVE', 'HOTs Trade', NULL, NULL, NULL, NULL, NULL, '081196947711', 'Indonesia', 'Jakarta Utara', NULL, 1, '2026-03-12 02:54:13', '2026-03-12 02:54:13', NULL, NULL, NULL, NULL, NULL, 'unverified', NULL, 0, NULL, NULL, NULL),
(66, 'susi@hotstrading.com', 'Susi Sumarno', NULL, NULL, NULL, '$2y$10$4CYXlF51AE3VtGGdhv9M7eZ9p3qerfX092GKUAc3gehqG89h6CWp2', 'ADMIN', 'ACTIVE', 'HOTs Trading', NULL, NULL, NULL, NULL, NULL, '081196947711', 'Indonesia', 'Jakarta Utara', NULL, 1, '2026-03-12 04:37:45', '2026-03-12 04:37:45', NULL, NULL, NULL, NULL, NULL, 'unverified', NULL, 0, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_product_summary`
-- (See below for the actual view)
--
CREATE TABLE `v_product_summary` (
`id` int(11)
,`product_code` varchar(50)
,`name` varchar(255)
,`category` varchar(100)
,`series` varchar(255)
,`manufacturer_name` varchar(255)
,`manufacturer_country` varchar(100)
,`is_active` tinyint(1)
,`is_featured` tinyint(1)
,`quotation_count` bigint(21)
,`created_at` timestamp
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_quotation_summary`
-- (See below for the actual view)
--
CREATE TABLE `v_quotation_summary` (
`id` int(11)
,`quotation_number` varchar(50)
,`status` enum('PENDING','QUOTED','ADMIN_REVIEW','ACCEPTED','REJECTED','EXPIRED')
,`product_name` varchar(255)
,`distributor_name` varchar(255)
,`manufacturer_name` varchar(255)
,`quantity` int(11)
,`quoted_price` decimal(10,2)
,`currency` varchar(10)
,`created_at` timestamp
,`responded_at` timestamp
);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user` (`user_id`),
  ADD KEY `idx_action` (`action`),
  ADD KEY `idx_entity` (`entity_type`,`entity_id`),
  ADD KEY `idx_created` (`created_at`);

--
-- Indexes for table `admin_activity_log`
--
ALTER TABLE `admin_activity_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_admin_id` (`admin_id`),
  ADD KEY `idx_action` (`action`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indexes for table `blog_posts`
--
ALTER TABLE `blog_posts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_slug` (`slug`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_category` (`category`),
  ADD KEY `idx_created_at` (`created_at`),
  ADD KEY `idx_blog_slug` (`slug`),
  ADD KEY `idx_blog_status` (`status`),
  ADD KEY `idx_blog_category` (`category`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_slug` (`slug`),
  ADD KEY `idx_name` (`name`);

--
-- Indexes for table `contact_messages`
--
ALTER TABLE `contact_messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_created` (`created_at`),
  ADD KEY `idx_status_created` (`status`,`created_at`);

--
-- Indexes for table `email_logs`
--
ALTER TABLE `email_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_email` (`recipient_email`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indexes for table `email_queue`
--
ALTER TABLE `email_queue`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_status` (`status`);

--
-- Indexes for table `email_tokens`
--
ALTER TABLE `email_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `idx_token` (`token`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `login_attempts`
--
ALTER TABLE `login_attempts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_ip` (`ip_address`),
  ADD KEY `idx_time` (`attempt_time`);

--
-- Indexes for table `manufacturers`
--
ALTER TABLE `manufacturers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_slug` (`slug`),
  ADD KEY `idx_name` (`name`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_sender` (`sender_id`),
  ADD KEY `idx_receiver` (`receiver_id`),
  ADD KEY `idx_quotation` (`quotation_id`),
  ADD KEY `idx_read` (`is_read`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_notif_user` (`user_id`),
  ADD KEY `idx_notif_read` (`is_read`),
  ADD KEY `idx_notif_type` (`type`),
  ADD KEY `idx_notif_created` (`created_at`);

--
-- Indexes for table `password_resets`
--
ALTER TABLE `password_resets`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_token` (`token`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_token` (`token`),
  ADD KEY `idx_expires_at` (`expires_at`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `product_code` (`product_code`),
  ADD KEY `idx_product_code` (`product_code`),
  ADD KEY `idx_category` (`category`),
  ADD KEY `idx_manufacturer` (`manufacturer_id`),
  ADD KEY `idx_active` (`is_active`),
  ADD KEY `idx_featured` (`is_featured`),
  ADD KEY `idx_products_manufacturer` (`manufacturer_id`),
  ADD KEY `idx_products_category` (`category`),
  ADD KEY `idx_products_active` (`is_active`),
  ADD KEY `idx_products_search` (`manufacturer_id`,`is_active`,`category`),
  ADD KEY `fk_products_category` (`category_id`);
ALTER TABLE `products` ADD FULLTEXT KEY `idx_search` (`name`,`description`,`category`);

--
-- Indexes for table `product_certifications`
--
ALTER TABLE `product_certifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_product` (`product_id`);

--
-- Indexes for table `product_regions`
--
ALTER TABLE `product_regions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_product` (`product_id`);

--
-- Indexes for table `product_specifications`
--
ALTER TABLE `product_specifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_product` (`product_id`);

--
-- Indexes for table `product_use_cases`
--
ALTER TABLE `product_use_cases`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_product` (`product_id`);

--
-- Indexes for table `quotations`
--
ALTER TABLE `quotations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `quotation_number` (`quotation_number`),
  ADD KEY `idx_quotation_number` (`quotation_number`),
  ADD KEY `idx_distributor` (`distributor_id`),
  ADD KEY `idx_manufacturer` (`manufacturer_id`),
  ADD KEY `idx_product` (`product_id`),
  ADD KEY `idx_status` (`status`);

--
-- Indexes for table `quotation_items`
--
ALTER TABLE `quotation_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_quotation` (`quotation_id`),
  ADD KEY `idx_product` (`product_id`);

--
-- Indexes for table `quotation_item_sizes`
--
ALTER TABLE `quotation_item_sizes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_item` (`quotation_item_id`);

--
-- Indexes for table `rate_limits`
--
ALTER TABLE `rate_limits`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_key` (`rate_key`),
  ADD KEY `idx_window` (`window_start`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD UNIQUE KEY `idx_slug` (`slug`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_role` (`role`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_users_role` (`role`),
  ADD KEY `idx_users_email` (`email`),
  ADD KEY `idx_users_slug` (`slug`),
  ADD KEY `idx_is_hidden` (`is_hidden`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT for table `admin_activity_log`
--
ALTER TABLE `admin_activity_log`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- AUTO_INCREMENT for table `blog_posts`
--
ALTER TABLE `blog_posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `contact_messages`
--
ALTER TABLE `contact_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `email_logs`
--
ALTER TABLE `email_logs`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `email_queue`
--
ALTER TABLE `email_queue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `email_tokens`
--
ALTER TABLE `email_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `login_attempts`
--
ALTER TABLE `login_attempts`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `manufacturers`
--
ALTER TABLE `manufacturers`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `password_resets`
--
ALTER TABLE `password_resets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=122;

--
-- AUTO_INCREMENT for table `product_certifications`
--
ALTER TABLE `product_certifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `product_regions`
--
ALTER TABLE `product_regions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `product_specifications`
--
ALTER TABLE `product_specifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `product_use_cases`
--
ALTER TABLE `product_use_cases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `quotations`
--
ALTER TABLE `quotations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `quotation_items`
--
ALTER TABLE `quotation_items`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `quotation_item_sizes`
--
ALTER TABLE `quotation_item_sizes`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `rate_limits`
--
ALTER TABLE `rate_limits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=68;

-- --------------------------------------------------------

--
-- Structure for view `v_product_summary`
--
DROP TABLE IF EXISTS `v_product_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`hotj4796`@`localhost` SQL SECURITY DEFINER VIEW `v_product_summary`  AS SELECT `p`.`id` AS `id`, `p`.`product_code` AS `product_code`, `p`.`name` AS `name`, `p`.`category` AS `category`, `p`.`series` AS `series`, `u`.`company_name` AS `manufacturer_name`, `u`.`country` AS `manufacturer_country`, `p`.`is_active` AS `is_active`, `p`.`is_featured` AS `is_featured`, count(distinct `q`.`id`) AS `quotation_count`, `p`.`created_at` AS `created_at` FROM ((`products` `p` left join `users` `u` on(`p`.`manufacturer_id` = `u`.`id`)) left join `quotations` `q` on(`p`.`id` = `q`.`product_id`)) GROUP BY `p`.`id` ;

-- --------------------------------------------------------

--
-- Structure for view `v_quotation_summary`
--
DROP TABLE IF EXISTS `v_quotation_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`hotj4796`@`localhost` SQL SECURITY DEFINER VIEW `v_quotation_summary`  AS SELECT `q`.`id` AS `id`, `q`.`quotation_number` AS `quotation_number`, `q`.`status` AS `status`, `p`.`name` AS `product_name`, `d`.`company_name` AS `distributor_name`, `m`.`company_name` AS `manufacturer_name`, `q`.`quantity` AS `quantity`, `q`.`quoted_price` AS `quoted_price`, `q`.`currency` AS `currency`, `q`.`created_at` AS `created_at`, `q`.`responded_at` AS `responded_at` FROM (((`quotations` `q` join `products` `p` on(`q`.`product_id` = `p`.`id`)) join `users` `d` on(`q`.`distributor_id` = `d`.`id`)) join `users` `m` on(`q`.`manufacturer_id` = `m`.`id`)) ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `email_tokens`
--
ALTER TABLE `email_tokens`
  ADD CONSTRAINT `email_tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `messages_ibfk_3` FOREIGN KEY (`quotation_id`) REFERENCES `quotations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `fk_notifications_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `password_resets`
--
ALTER TABLE `password_resets`
  ADD CONSTRAINT `fk_password_resets_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `fk_products_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`manufacturer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_certifications`
--
ALTER TABLE `product_certifications`
  ADD CONSTRAINT `product_certifications_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_regions`
--
ALTER TABLE `product_regions`
  ADD CONSTRAINT `product_regions_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_specifications`
--
ALTER TABLE `product_specifications`
  ADD CONSTRAINT `product_specifications_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_use_cases`
--
ALTER TABLE `product_use_cases`
  ADD CONSTRAINT `product_use_cases_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `quotations`
--
ALTER TABLE `quotations`
  ADD CONSTRAINT `quotations_ibfk_1` FOREIGN KEY (`distributor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `quotations_ibfk_2` FOREIGN KEY (`manufacturer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `quotations_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `quotation_items`
--
ALTER TABLE `quotation_items`
  ADD CONSTRAINT `fk_quotation_items_quotation` FOREIGN KEY (`quotation_id`) REFERENCES `quotations` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
