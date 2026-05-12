-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Máy chủ: localhost:3306
-- Thời gian đã tạo: Th5 11, 2026 lúc 04:56 PM
-- Phiên bản máy phục vụ: 8.4.3
-- Phiên bản PHP: 8.3.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `petshop_db`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `bookings`
--

CREATE TABLE `bookings` (
  `id` int NOT NULL,
  `customer_id` int NOT NULL,
  `pet_id` int NOT NULL,
  `service_id` int NOT NULL,
  `employee_id` int DEFAULT NULL,
  `booking_time` datetime NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `is_paid` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `bookings`
--

INSERT INTO `bookings` (`id`, `customer_id`, `pet_id`, `service_id`, `employee_id`, `booking_time`, `status`, `notes`, `created_at`, `is_paid`) VALUES
(2, 1, 2, 4, 1, '2026-04-21 17:20:00', 'Pending', 'dfd', '2026-04-20 17:19:03', 1),
(5, 1, 1, 1, 2, '2026-05-07 16:09:00', 'Confirmed', '', '2026-05-06 16:09:29', 1),
(6, 1, 2, 2, 2, '2026-05-07 16:19:00', 'Confirmed', 'Có thể đến muộn hơn', '2026-05-06 16:19:49', 0),
(7, 6, 21, 1, 2, '2026-05-15 10:20:00', 'Confirmed', '', '2026-05-09 10:20:54', 1),
(8, 6, 21, 1, 2, '2026-05-02 10:28:00', 'Confirmed', '', '2026-05-09 10:28:45', 1),
(9, 10, 11, 3, 2, '2026-05-15 10:29:00', 'Confirmed', '', '2026-05-09 10:29:13', 1),
(10, 10, 12, 2, 1, '2026-05-02 10:52:00', 'Confirmed', '', '2026-05-09 10:52:50', 0),
(11, 1, 1, 1, 2, '2026-04-17 10:57:00', 'Confirmed', 'mm', '2026-05-09 10:57:26', 0),
(12, 2, 3, 1, 2, '2026-05-09 11:09:00', 'Confirmed', '', '2026-05-09 11:10:14', 1),
(13, 1, 5, 1, 2, '2026-05-10 01:30:00', 'Confirmed', 'hhh', '2026-05-09 11:29:08', 0);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `categories`
--

CREATE TABLE `categories` (
  `id` int NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `categories`
--

INSERT INTO `categories` (`id`, `name`, `description`) VALUES
(1, 'Thức ăn', 'Thức ăn khô và ướt cho thú cưng'),
(2, 'Phụ kiện', 'Vòng cổ, dây dắt, lồng vận chuyển'),
(3, 'Đồ chơi', 'Xương gặm, cần câu mèo, bóng');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `customers`
--

CREATE TABLE `customers` (
  `id` int NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tier` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `points` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `total_spent` float DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `customers`
--

INSERT INTO `customers` (`id`, `name`, `phone`, `address`, `tier`, `points`, `created_at`, `total_spent`) VALUES
(1, 'Nguyễn Văn A', '0988123456', 'None', 'Platinum', 150, '2026-04-17 17:31:01', 69164400),
(2, 'Trần Thị B', '0912345678', 'None', 'Standard', 300, '2026-04-17 17:31:01', 650100),
(4, 'Cần câu mèo lông vũ', '0338484668', 'None', 'Standard', 0, '2026-04-23 21:59:43', 0),
(6, 'Dang Bao Hung', '098812345631', '', 'Standard', 0, '2026-04-23 22:45:55', 150000),
(8, 'Tiêm ngừa dại (Rabies)', '09123456781', 'None', NULL, 0, '2026-05-08 15:53:13', 0),
(10, 'Đào Ngọc Đức', '132131232132', NULL, NULL, 0, '2026-05-08 16:48:41', 30695000),
(11, 'Long', '0912121212', NULL, NULL, 0, '2026-05-08 17:09:36', 2075000),
(12, 'THanh', '091313131', NULL, NULL, 0, '2026-05-08 17:31:15', 3465000);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `orders`
--

CREATE TABLE `orders` (
  `id` int NOT NULL,
  `customer_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `total_amount` float NOT NULL,
  `payment_method` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `orders`
--

INSERT INTO `orders` (`id`, `customer_id`, `user_id`, `total_amount`, `payment_method`, `status`, `created_at`) VALUES
(1, 1, 1, 15000, 'Cash', 'Completed', '2026-04-20 16:51:43'),
(2, NULL, 1, 120000, 'Banking', 'Completed', '2026-04-20 16:51:48'),
(3, NULL, 1, 240000, 'Banking', 'Completed', '2026-04-23 22:26:58'),
(4, NULL, 1, 730000, 'Cash', 'Completed', '2026-04-23 22:31:57'),
(5, NULL, 1, 95000, 'Cash', 'Completed', '2026-04-23 22:33:41'),
(6, NULL, 1, 95000, 'Cash', 'Completed', '2026-04-23 22:33:48'),
(7, NULL, 1, 650000, 'Cash', 'Completed', '2026-04-23 22:36:36'),
(8, NULL, 1, 95000, 'Cash', 'Completed', '2026-04-23 22:36:45'),
(9, NULL, 1, 240000, 'Cash', 'Completed', '2026-04-23 22:36:46'),
(10, NULL, 1, 240000, 'Cash', 'Completed', '2026-04-23 22:36:48'),
(11, NULL, 1, 225000, 'Cash', 'Completed', '2026-04-23 22:36:53'),
(12, NULL, 1, 95000, 'Cash', 'Completed', '2026-04-23 22:42:04'),
(13, NULL, 1, 95000, 'Cash', 'Completed', '2026-04-23 22:42:30'),
(14, NULL, 1, 315000, 'Cash', 'Completed', '2026-04-23 22:54:18'),
(15, NULL, 1, 760000, 'Cash', 'Completed', '2026-04-23 22:54:26'),
(16, NULL, 1, 215000, 'Cash', 'Completed', '2026-04-23 23:05:08'),
(17, NULL, 1, 95000, 'Banking', 'Completed', '2026-04-23 23:10:50'),
(18, NULL, 1, 1760000, 'Banking', 'Completed', '2026-04-23 23:19:27'),
(19, 1, 1, 3620000, 'Cash', 'Completed', '2026-04-23 23:20:55'),
(20, 1, 1, 1720000, 'Cash', 'Completed', '2026-04-23 23:21:06'),
(21, 1, 1, 2260000, 'Cash', 'Completed', '2026-04-23 23:21:13'),
(22, 1, 1, 422750, 'Banking', 'Completed', '2026-04-23 23:21:56'),
(23, 1, 1, 1871500, 'Cash', 'Completed', '2026-04-23 23:25:07'),
(24, 1, 1, 2840500, 'Cash', 'Completed', '2026-04-23 23:25:42'),
(25, 1, 1, 350000, 'Banking', 'Completed', '2026-04-23 23:39:14'),
(26, 1, 1, 108000, 'Cash', 'Completed', '2026-04-23 23:42:57'),
(27, 1, 1, 85500, 'Cash', 'Completed', '2026-04-23 23:45:09'),
(28, 1, 1, 85500, 'Banking', 'Completed', '2026-04-23 23:45:19'),
(29, 1, 1, 670500, 'Cash', 'Completed', '2026-04-23 23:48:01'),
(30, NULL, 1, 645000, 'Banking', 'Completed', '2026-05-06 13:20:29'),
(31, 1, 1, 350000, 'Cash', 'Completed', '2026-05-06 16:01:29'),
(32, 1, 1, 50000, 'Cash', 'Completed', '2026-05-06 16:06:21'),
(33, NULL, 1, 615000, 'Banking', 'Completed', '2026-05-07 00:12:22'),
(34, 1, 1, 1075000, 'Banking', 'Completed', '2026-05-07 11:11:17'),
(35, NULL, 1, 10000000, 'Banking', 'Completed', '2026-05-08 16:02:13'),
(36, NULL, 1, 4000000, 'Cash', 'Completed', '2026-05-08 16:10:29'),
(37, 10, 1, 20045000, 'Cash', 'Completed', '2026-05-08 16:48:41'),
(38, 1, 1, 10000000, 'Cash', 'Completed', '2026-05-08 17:03:27'),
(39, 11, 1, 2075000, 'Cash', 'Completed', '2026-05-08 17:09:36'),
(40, 12, 1, 3465000, 'Cash', 'Completed', '2026-05-08 17:31:15'),
(41, 1, 1, 2450000, 'Cash', 'Completed', '2026-05-08 17:31:43'),
(42, NULL, 1, 150000, 'Cash', 'Completed', '2026-05-09 10:21:20'),
(43, 6, 1, 150000, 'Cash', 'Completed', '2026-05-09 10:31:22'),
(44, 1, 1, 40495000, 'Cash', 'Completed', '2026-05-09 10:45:47'),
(45, 1, 1, 695100, 'Cash', 'Completed', '2026-05-09 10:48:07'),
(46, 2, 1, 650100, 'Banking', 'Completed', '2026-05-09 11:11:22'),
(47, 10, 1, 10650000, 'Banking', 'Completed', '2026-05-09 11:30:35');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `order_items`
--

CREATE TABLE `order_items` (
  `id` int NOT NULL,
  `order_id` int NOT NULL,
  `product_id` int DEFAULT NULL,
  `service_id` int DEFAULT NULL,
  `quantity` int NOT NULL,
  `price` float NOT NULL,
  `pet_for_sale_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `service_id`, `quantity`, `price`, `pet_for_sale_id`) VALUES
(1, 1, 2, NULL, 1, 15000, NULL),
(2, 2, 4, NULL, 1, 120000, NULL),
(3, 3, 4, NULL, 1, 120000, NULL),
(4, 3, NULL, 4, 1, 120000, NULL),
(5, 4, NULL, 2, 2, 350000, NULL),
(6, 4, 2, NULL, 2, 15000, NULL),
(7, 5, 3, NULL, 1, 45000, NULL),
(8, 5, NULL, 3, 1, 50000, NULL),
(9, 6, 3, NULL, 1, 45000, NULL),
(10, 6, NULL, 3, 1, 50000, NULL),
(11, 7, 2, NULL, 1, 15000, NULL),
(12, 7, NULL, 2, 1, 350000, NULL),
(13, 7, 3, NULL, 1, 45000, NULL),
(14, 7, 4, NULL, 1, 120000, NULL),
(15, 7, NULL, 4, 1, 120000, NULL),
(16, 8, NULL, 3, 1, 50000, NULL),
(17, 8, 3, NULL, 1, 45000, NULL),
(18, 9, 4, NULL, 1, 120000, NULL),
(19, 9, NULL, 4, 1, 120000, NULL),
(20, 10, 4, NULL, 1, 120000, NULL),
(21, 10, NULL, 4, 1, 120000, NULL),
(22, 11, 5, NULL, 3, 35000, NULL),
(23, 11, NULL, 4, 1, 120000, NULL),
(24, 12, 3, NULL, 1, 45000, NULL),
(25, 12, NULL, 3, 1, 50000, NULL),
(26, 13, 3, NULL, 1, 45000, NULL),
(27, 13, NULL, 3, 1, 50000, NULL),
(28, 14, 3, NULL, 1, 45000, NULL),
(29, 14, NULL, 3, 3, 50000, NULL),
(30, 14, 4, NULL, 1, 120000, NULL),
(31, 15, 3, NULL, 1, 45000, NULL),
(32, 15, 4, NULL, 1, 120000, NULL),
(33, 15, 5, NULL, 7, 35000, NULL),
(34, 15, NULL, 2, 1, 350000, NULL),
(35, 16, 3, NULL, 1, 45000, NULL),
(36, 16, NULL, 3, 1, 50000, NULL),
(37, 16, NULL, 4, 1, 120000, NULL),
(38, 17, 3, NULL, 1, 45000, NULL),
(39, 17, NULL, 3, 1, 50000, NULL),
(40, 18, 5, NULL, 1, 35000, NULL),
(41, 18, NULL, 4, 13, 120000, NULL),
(42, 18, 2, NULL, 11, 15000, NULL),
(43, 19, 4, NULL, 3, 120000, NULL),
(44, 19, 3, NULL, 8, 45000, NULL),
(45, 19, NULL, 4, 5, 120000, NULL),
(46, 19, NULL, 2, 6, 350000, NULL),
(47, 19, NULL, 1, 1, 150000, NULL),
(48, 19, NULL, 3, 1, 50000, NULL),
(49, 20, NULL, 3, 9, 50000, NULL),
(50, 20, 2, NULL, 4, 15000, NULL),
(51, 20, NULL, 2, 2, 350000, NULL),
(52, 20, NULL, 1, 1, 150000, NULL),
(53, 20, NULL, 4, 3, 120000, NULL),
(54, 21, NULL, 4, 3, 120000, NULL),
(55, 21, NULL, 3, 3, 50000, NULL),
(56, 21, NULL, 2, 5, 350000, NULL),
(57, 22, 3, NULL, 1, 45000, NULL),
(58, 22, NULL, 3, 1, 50000, NULL),
(59, 22, NULL, 2, 1, 350000, NULL),
(60, 23, 5, NULL, 2, 35000, NULL),
(61, 23, NULL, 4, 5, 120000, NULL),
(62, 23, NULL, 3, 5, 50000, NULL),
(63, 23, NULL, 2, 3, 350000, NULL),
(64, 24, NULL, 3, 11, 50000, NULL),
(65, 24, NULL, 4, 5, 120000, NULL),
(66, 24, 3, NULL, 2, 45000, NULL),
(67, 24, NULL, 2, 5, 350000, NULL),
(68, 25, NULL, 2, 1, 350000, NULL),
(69, 26, NULL, 4, 1, 120000, NULL),
(70, 27, 3, NULL, 1, 45000, NULL),
(71, 27, NULL, 3, 1, 50000, NULL),
(72, 28, 3, NULL, 1, 45000, NULL),
(73, 28, NULL, 3, 1, 50000, NULL),
(74, 29, 3, NULL, 1, 45000, NULL),
(75, 29, NULL, 3, 4, 50000, NULL),
(76, 29, 4, NULL, 1, 120000, NULL),
(77, 29, NULL, 4, 2, 120000, NULL),
(78, 29, 5, NULL, 4, 35000, NULL),
(79, 30, NULL, 3, 2, 50000, NULL),
(80, 30, 3, NULL, 1, 45000, NULL),
(81, 30, NULL, 2, 1, 350000, NULL),
(82, 30, NULL, 1, 1, 150000, NULL),
(83, 31, NULL, 2, 1, 350000, NULL),
(84, 32, NULL, 3, 1, 50000, NULL),
(85, 33, 3, NULL, 1, 45000, NULL),
(86, 33, 4, NULL, 1, 120000, NULL),
(87, 33, 5, NULL, 1, 35000, NULL),
(88, 33, 2, NULL, 1, 15000, NULL),
(89, 33, NULL, 2, 1, 350000, NULL),
(90, 33, NULL, 3, 1, 50000, NULL),
(91, 34, 2, NULL, 1, 15000, NULL),
(92, 34, NULL, 2, 2, 350000, NULL),
(93, 34, NULL, 4, 3, 120000, NULL),
(94, 35, NULL, NULL, 1, 10000000, 3),
(95, 36, NULL, NULL, 4, 1000000, 2),
(96, 37, NULL, NULL, 2, 10000000, 3),
(97, 37, 2, NULL, 3, 15000, NULL),
(98, 38, NULL, NULL, 1, 10000000, 3),
(99, 39, NULL, NULL, 2, 1000000, 2),
(100, 39, 2, NULL, 2, 15000, NULL),
(101, 39, 3, NULL, 1, 45000, NULL),
(102, 40, NULL, NULL, 3, 1000000, 2),
(103, 40, 1, NULL, 1, 450000, NULL),
(104, 40, 2, NULL, 1, 15000, NULL),
(105, 41, NULL, NULL, 2, 1000000, 2),
(106, 41, 1, NULL, 1, 450000, NULL),
(107, 42, NULL, 1, 1, 150000, NULL),
(108, 43, NULL, 1, 1, 150000, NULL),
(109, 44, NULL, NULL, 4, 10000000, 3),
(110, 44, 1, NULL, 1, 450000, NULL),
(111, 44, 3, NULL, 1, 45000, NULL),
(112, 45, NULL, 1, 1, 150000, NULL),
(113, 45, 1, NULL, 1, 450000, NULL),
(114, 45, 3, NULL, 1, 45000, NULL),
(115, 45, NULL, 3, 1, 50000, NULL),
(116, 45, NULL, NULL, 1, 100, 5),
(117, 46, NULL, 1, 1, 150000, NULL),
(118, 46, 1, NULL, 1, 450000, NULL),
(119, 46, NULL, 3, 1, 50000, NULL),
(120, 46, NULL, NULL, 1, 100, 5),
(121, 47, NULL, 3, 1, 50000, NULL),
(122, 47, 1, NULL, 1, 450000, NULL),
(123, 47, NULL, 1, 1, 150000, NULL),
(124, 47, NULL, NULL, 1, 10000000, 3);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `pets`
--

CREATE TABLE `pets` (
  `id` int NOT NULL,
  `customer_id` int NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `species` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `breed` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `image` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `health_notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `source` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'customer_owned',
  `purchase_order_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `pets`
--

INSERT INTO `pets` (`id`, `customer_id`, `name`, `species`, `breed`, `dob`, `weight`, `image`, `health_notes`, `created_at`, `source`, `purchase_order_id`) VALUES
(1, 1, 'Milo', 'Chó', 'Corgi', NULL, 12.5, NULL, NULL, '2026-04-17 17:31:01', 'customer_owned', NULL),
(2, 1, 'Bông', 'Mèo', 'Ba Tư', NULL, 36, NULL, 'None', '2026-04-17 17:31:01', 'customer_owned', NULL),
(3, 2, 'Mực', 'Chó', 'Poodle', NULL, 5, NULL, NULL, '2026-04-17 17:31:01', 'customer_owned', NULL),
(4, 1, 'Cún', 'Chó', 'Phú Quốc', NULL, 45, NULL, '', '2026-05-06 15:49:34', 'customer_owned', NULL),
(5, 1, 'Mun', 'Chó', 'Phú Quốc', NULL, 5, NULL, 'Khỏe mạnh', '2026-05-06 16:17:35', 'customer_owned', NULL),
(11, 10, 'mèo lông vũ #1', 'Mèo', 'Phú Quốc', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #37). ', '2026-05-08 16:48:41', 'store_purchase', NULL),
(12, 10, 'mèo lông vũ #2', 'Mèo', 'Phú Quốc', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #37). ', '2026-05-08 16:48:41', 'store_purchase', NULL),
(13, 1, 'mèo lông vũ', 'Mèo', 'Phú Quốc', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #38). ', '2026-05-08 17:03:27', 'store_purchase', 38),
(14, 11, 'Mun #1', 'Mèo', 'Ba Tư', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #39). ', '2026-05-08 17:09:36', 'store_purchase', 39),
(15, 11, 'Mun #2', 'Mèo', 'Ba Tư', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #39). ', '2026-05-08 17:09:36', 'store_purchase', 39),
(16, 12, 'Mun #1', 'Mèo', 'Ba Tư', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #40). ', '2026-05-08 17:31:15', 'store_purchase', 40),
(17, 12, 'Mun #2', 'Mèo', 'Ba Tư', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #40). ', '2026-05-08 17:31:15', 'store_purchase', 40),
(18, 12, 'Mun #3', 'Mèo', 'Ba Tư', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #40). ', '2026-05-08 17:31:15', 'store_purchase', 40),
(19, 1, 'Mun #1', 'Mèo', 'Ba Tư', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #41). ', '2026-05-08 17:31:43', 'store_purchase', 41),
(20, 1, 'Mun #2', 'Mèo', 'Ba Tư', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #41). ', '2026-05-08 17:31:43', 'store_purchase', 41),
(21, 6, 'Cún', 'Chó', 'Phú Quốc', NULL, 12, NULL, '', '2026-05-09 10:20:35', 'customer_owned', NULL),
(22, 1, 'mèo lông vũ #1', 'Mèo', 'Phú Quốc', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #44). ', '2026-05-09 10:45:47', 'store_purchase', 44),
(23, 1, 'mèo lông vũ #2', 'Mèo', 'Phú Quốc', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #44). ', '2026-05-09 10:45:47', 'store_purchase', 44),
(24, 1, 'mèo lông vũ #3', 'Mèo', 'Phú Quốc', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #44). ', '2026-05-09 10:45:47', 'store_purchase', 44),
(25, 1, 'mèo lông vũ #4', 'Mèo', 'Phú Quốc', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #44). ', '2026-05-09 10:45:47', 'store_purchase', 44),
(26, 1, 'Têmo', 'Mèo', 'tam the', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #45). qqq', '2026-05-09 10:48:07', 'store_purchase', 45),
(27, 2, 'Têmo', 'Mèo', 'tam the', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #46). qqq', '2026-05-09 11:11:22', 'store_purchase', 46),
(28, 10, 'mèo lông vũ', 'Mèo', 'Phú Quốc', NULL, NULL, NULL, 'Mua từ cửa hàng (Mã ĐH: #47). ', '2026-05-09 11:30:35', 'store_purchase', 47);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `pets_for_sale`
--

CREATE TABLE `pets_for_sale` (
  `id` int NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `species` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `breed` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `age` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `price` float NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `health_notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `quantity` int DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `pets_for_sale`
--

INSERT INTO `pets_for_sale` (`id`, `name`, `species`, `breed`, `age`, `price`, `status`, `image`, `health_notes`, `created_at`, `quantity`) VALUES
(2, 'Mun', 'Mèo', 'Ba Tư', '2 tháng', 1000000, 'Available', NULL, '', '2026-05-07 11:34:02', 29),
(3, 'mèo lông vũ', 'Mèo', 'Phú Quốc', '2 tháng', 10000000, 'Available', NULL, '', '2026-05-07 11:41:56', 4),
(4, 'Cún', 'Mèo', 'Phú Quốc', '2 tháng', 5000000, 'Available', NULL, '', '2026-05-08 15:46:31', 10),
(5, 'Têmo', 'Mèo', 'tam the', '2 tháng', 100, 'Available', NULL, 'qqq', '2026-05-08 16:08:52', 34),
(6, 'Cún mili', 'Thỏ', 'tam the', '3 tháng', 1000000, 'Available', NULL, '', '2026-05-09 10:25:31', 15);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `products`
--

CREATE TABLE `products` (
  `id` int NOT NULL,
  `category_id` int NOT NULL,
  `sku` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` float NOT NULL,
  `cost` float DEFAULT NULL,
  `stock_quantity` int DEFAULT NULL,
  `image` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `products`
--

INSERT INTO `products` (`id`, `category_id`, `sku`, `name`, `price`, `cost`, `stock_quantity`, `image`, `created_at`) VALUES
(1, 1, 'RC-P-2000', 'Hạt Royal Canin Puppy 2kg', 450000, 350000, 549, NULL, '2026-04-20 16:49:50'),
(2, 1, 'WK-M-085', 'Pate Whiskas Vị Cá Thu 85g', 15000, 10000, 547, NULL, '2026-04-20 16:49:50'),
(3, 2, 'ACC-CO-01', 'Vòng cổ phản quang', 45000, 20000, 1505, NULL, '2026-04-20 16:49:50'),
(4, 2, 'ACC-SH-01', 'Sữa tắm SOS 500ml', 120000, 80000, 355351, NULL, '2026-04-20 16:49:50'),
(5, 3, 'TOY-C-01', 'Cần câu mèo lông vũ', 35000, 15000, 85, NULL, '2026-04-20 16:49:50'),
(6, 2, 'WK-M-0852', 'Lồng cho mèo', 500000, 0, 15, NULL, '2026-05-08 15:51:40');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `services`
--

CREATE TABLE `services` (
  `id` int NOT NULL,
  `category_id` int NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` float NOT NULL,
  `duration_minutes` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `services`
--

INSERT INTO `services` (`id`, `category_id`, `name`, `price`, `duration_minutes`, `is_active`) VALUES
(1, 1, 'Tắm sấy cơ bản (Chó nhỏ)', 150000, 45, 1),
(2, 1, 'Cắt tỉa tạo kiểu (Chó nhỏ)', 350000, 90, 1),
(3, 1, 'Cắt móng & vệ sinh tai', 50000, 15, 1),
(4, 2, 'Tiêm ngừa dại (Rabies)', 120000, 10, 1);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `service_categories`
--

CREATE TABLE `service_categories` (
  `id` int NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `service_categories`
--

INSERT INTO `service_categories` (`id`, `name`) VALUES
(1, 'Làm đẹp (Grooming)'),
(2, 'Sức khỏe');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `full_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `plain_password` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `role`, `is_active`, `full_name`, `email`, `customer_id`, `phone`, `plain_password`) VALUES
(1, 'admin', 'scrypt:32768:8:1$yrBa0M7KLgzUHeyC$3238040343f2454b43c66be8a75db7e1c14c5b66de5d08291e381381a3e709c87ad8739beaa351c36d4828960d14c0621c2e1578311a510bc4b8e57f85d790cf', 'admin', 1, '', NULL, NULL, '', '123456'),
(2, 'groomer1', 'scrypt:32768:8:1$8lRirvpRPXgiF021$81c8b8584d94a9925e84785853525373bf5b56a70de490cf760d94c06982a98702fe9ac7ac967c1b1cba4c7e25cb690503644e8f0a5c63f81aa2beb1c782fa86', 'staff', 1, 'Bác sĩ Hùng', NULL, NULL, '', '123456'),
(3, 'hung', 'scrypt:32768:8:1$NHoBVtDhQpGV8MUa$c550c29ef2dfec943a110a1a98b65843f638029a22f8826ecc0f760be9dac2551ffc9fa0ca9198b3c189ef110560726442e88235d8eb9f8d29ab7d01403b82bd', 'customer', 1, 'Dang Bao Hung', 'baohungqp04@gmail.com', 6, '098812345631', '123456'),
(4, '0988123456', 'scrypt:32768:8:1$niDUNS1pFCZ7KGW4$f6a4c5d78f10d1ffb1592c63b5da58f7850b25ccea68f2bdefb1b7a304872cb8c46f7a7b07e9b07e02219004a9646864a1cda9e7bccc2544cd2f60fdf4c67c93', 'customer', 1, 'Nguyễn Văn A', NULL, 1, '0988123456', '123456'),
(5, '0912345678', 'scrypt:32768:8:1$bkYyk4XOTdRygFrk$49c501d84d3b13dff7b7224d1adc3619b374050965811c7314b191bcf984acadef24cf18ab9e592cc85b9226252765ba32bd48026494c48e692e0586e09c4573', 'customer', 1, 'Trần Thị B', '', 2, '0912345678', '1234562'),
(6, '0338484668', 'scrypt:32768:8:1$olE1nERAUxuYD1Dp$86020546200be2ea3158489caa9006c7f27c47e80b0ab5f45ba8862232a7b83945755f6a5683a184b0985e5a6d73b61f3332c58b7d7f2e18476e3bb096d0767e', 'customer', 1, 'Cần câu mèo lông vũ', NULL, 4, '0338484668', '123456'),
(7, 'letan', 'scrypt:32768:8:1$A2R3BV0nhlt2IwCz$cd6b72d0cca59031743001eda29fe5718584970acf16621017055848e64137768c9553179c2eb858740daaa59c2752d6e73107b8570daa698c3420c77775b5cc', 'receptionist', 1, 'Dao Ngoc Duc', 'duc@gmail.com', NULL, '012345678', '123456'),
(8, '09123456781', 'scrypt:32768:8:1$32JPKMI6njqcyPv8$559cece2250a5b0fb9040a0353b724b3fd5e3dd3e16c4198d7e45f895f2af5bc601f5b53b59c8d9aea9f3e27fd613f21231e4ba23e4cea8ee7dbc208c90a3a7c', 'customer', 1, 'Tiêm ngừa dại (Rabies)', NULL, 8, '09123456781', '123456');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `pet_id` (`pet_id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `employee_id` (`employee_id`);

--
-- Chỉ mục cho bảng `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_customers_phone` (`phone`);

--
-- Chỉ mục cho bảng `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Chỉ mục cho bảng `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `pet_for_sale_id` (`pet_for_sale_id`);

--
-- Chỉ mục cho bảng `pets`
--
ALTER TABLE `pets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `fk_pets_purchase_order` (`purchase_order_id`);

--
-- Chỉ mục cho bảng `pets_for_sale`
--
ALTER TABLE `pets_for_sale`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_products_sku` (`sku`),
  ADD KEY `category_id` (`category_id`);

--
-- Chỉ mục cho bảng `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Chỉ mục cho bảng `service_categories`
--
ALTER TABLE `service_categories`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_username` (`username`),
  ADD UNIQUE KEY `ix_users_email` (`email`),
  ADD KEY `fk_user_customer` (`customer_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT cho bảng `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT cho bảng `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT cho bảng `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT cho bảng `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=125;

--
-- AUTO_INCREMENT cho bảng `pets`
--
ALTER TABLE `pets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT cho bảng `pets_for_sale`
--
ALTER TABLE `pets_for_sale`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT cho bảng `products`
--
ALTER TABLE `products`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT cho bảng `services`
--
ALTER TABLE `services`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT cho bảng `service_categories`
--
ALTER TABLE `service_categories`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT cho bảng `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Ràng buộc đối với các bảng kết xuất
--

--
-- Ràng buộc cho bảng `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`id`),
  ADD CONSTRAINT `bookings_ibfk_3` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`),
  ADD CONSTRAINT `bookings_ibfk_4` FOREIGN KEY (`employee_id`) REFERENCES `users` (`id`);

--
-- Ràng buộc cho bảng `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ràng buộc cho bảng `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  ADD CONSTRAINT `order_items_ibfk_3` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`),
  ADD CONSTRAINT `order_items_ibfk_4` FOREIGN KEY (`pet_for_sale_id`) REFERENCES `pets_for_sale` (`id`);

--
-- Ràng buộc cho bảng `pets`
--
ALTER TABLE `pets`
  ADD CONSTRAINT `fk_pets_purchase_order` FOREIGN KEY (`purchase_order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `pets_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

--
-- Ràng buộc cho bảng `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);

--
-- Ràng buộc cho bảng `services`
--
ALTER TABLE `services`
  ADD CONSTRAINT `services_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `service_categories` (`id`);

--
-- Ràng buộc cho bảng `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_user_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
