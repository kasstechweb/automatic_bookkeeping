-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 15, 2023 at 08:25 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `automatic_bookkeeping`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add dictionary categories', 7, 'add_dictionarycategories'),
(26, 'Can change dictionary categories', 7, 'change_dictionarycategories'),
(27, 'Can delete dictionary categories', 7, 'delete_dictionarycategories'),
(28, 'Can view dictionary categories', 7, 'view_dictionarycategories'),
(29, 'Can add dictionary subcategories', 8, 'add_dictionarysubcategories'),
(30, 'Can change dictionary subcategories', 8, 'change_dictionarysubcategories'),
(31, 'Can delete dictionary subcategories', 8, 'delete_dictionarysubcategories'),
(32, 'Can view dictionary subcategories', 8, 'view_dictionarysubcategories'),
(33, 'Can add document', 9, 'add_document'),
(34, 'Can change document', 9, 'change_document'),
(35, 'Can delete document', 9, 'delete_document'),
(36, 'Can view document', 9, 'view_document');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `comp_name` varchar(255) DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `comp_name`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$260000$cR7DEuEVHwJ541XLKSqYzC$3/xR/c221JxsGrnJYSFCFec5tQ4mJiVam9v9Rsu+DNI=', '2023-01-14 22:03:22.266119', 0, 'kasstechweb', '', '', 'kasstechweb@gmail.com', NULL, 0, 1, '2023-01-06 22:21:50.209805'),
(2, 'pbkdf2_sha256$260000$vKRTprsXTVVazHaGB0zGMe$dIyqYVhFlbdVdV0EHiJw5vu77zRzMGGiaLJpZW2DPIo=', '2023-01-14 21:03:28.703260', 1, 'kasstechwebadmin@gmail.com', '', '', 'kasstechwebadmin@gmail.com', NULL, 1, 1, '2023-01-14 21:03:00.244387');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `company`
--

CREATE TABLE `company` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `province` varchar(255) DEFAULT NULL,
  `zip` varchar(255) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `company`
--

INSERT INTO `company` (`id`, `name`, `phone`, `street`, `city`, `province`, `zip`, `user_id`) VALUES
(4, 'test comp', 123456789, '1515 street ', 'Edmonton', 'QC', 't5e 5rw', 1);

-- --------------------------------------------------------

--
-- Table structure for table `dictionary_categories`
--

CREATE TABLE `dictionary_categories` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `code` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dictionary_categories`
--

INSERT INTO `dictionary_categories` (`id`, `name`, `code`) VALUES
(1, 'Accounting fees', 8862),
(2, 'Advertising', 8521),
(3, 'Advertising and promotion', 8520),
(4, 'Amortization of intangible assets', 8570),
(5, 'Amortization of natural resource assets', 8650),
(6, 'Amortization of tangible assets', 8670),
(7, 'Appraisal fees', 8865),
(8, 'Architect Fees', 8864),
(9, 'Bad debt expense', 8590),
(10, 'Bank charges', 8715),
(11, 'Bonuses', 9063),
(12, 'Brokerage fees', 8869),
(13, 'Business taxes', 8762),
(14, 'Business taxes, licences and memberships', 8760),
(15, 'Camp supplies', 9139),
(16, 'Cash over / short', 9271),
(17, 'Collection and credit costs', 8717),
(18, 'Commissions', 9061),
(19, 'Computer-related expenses', 9150),
(20, 'Condominium fees', 8913),
(21, 'Consulting fees', 8863),
(22, 'Contributions to deferred income plans', 8623),
(23, 'Credit card charges', 8716),
(24, 'Crew share', 9062),
(25, 'Data processing', 8813),
(26, 'Delivery, freight and express', 9275),
(27, 'Directors fees', 9064),
(28, 'Donations', 8522),
(29, 'Dumping charges', 9279),
(30, 'Electricity', 9221),
(31, 'Employee benefits', 8620),
(32, 'Employee salaries', 9066),
(33, 'Employer\'s portion of employee benefits', 8622),
(34, 'Equipment rental', 8914),
(35, 'Fishing gear', 9136),
(36, 'Food and catering', 9135),
(37, 'Franchise fees', 8763),
(38, 'Fuel costs', 9224),
(39, 'Garbage removal', 9014),
(40, 'General and administrative expenses', 9284),
(41, 'Goodwill impairment loss', 8571),
(42, 'Government fees', 8764),
(43, 'Group insurance benefits', 8621),
(44, 'Heat', 9223),
(45, 'Insurance', 8690),
(46, 'Interest and bank charges', 8710),
(47, 'Interest on bonds and debentures', 8712),
(48, 'Interest on long term debt', 8714),
(49, 'Interest on mortgages', 8713),
(50, 'Interest on short term debt', 8711),
(51, 'Interest paid (financial institutions)', 8740),
(52, 'Interest paid on bonds and debentures', 8742),
(53, 'Interest paid on deposits', 8741),
(54, 'Interfund transfer', 9286),
(55, 'Internet', 9152),
(56, 'Laboratory fees', 8866),
(57, 'Land fill fees', 9280),
(58, 'Laundry', 9134),
(59, 'Legal fees', 8861),
(60, 'Life insurance on executives', 8691),
(61, 'Loan losses', 8610),
(62, 'Machine shop expense', 9011),
(63, 'Management and administration fees', 8871),
(64, 'Management salaries', 9065),
(65, 'Meals and entertainment', 8523),
(66, 'Medical fees', 8867),
(67, 'Meetings and conventions', 9201),
(68, 'Memberships', 8761),
(69, 'Moorage (boat)', 8916),
(70, 'Motor vehicle rentals', 8915),
(71, 'Nets and traps', 9137),
(72, 'Nova Scotia tax on large corporations', 8790),
(73, 'Occupancy costs', 8912),
(74, 'Office stationery and supplies', 8811),
(75, 'Office utilities', 8812),
(76, 'Other expenses', 9270),
(77, 'Other repairs and maintenance', 9010),
(78, 'Professional fees', 8860),
(79, 'Promotion', 8524),
(80, 'Property taxes', 9180),
(81, 'Provision for loan losses', 8611),
(82, 'Quota rental', 8918),
(83, 'Real estate rental', 8911),
(84, 'Refining and assay', 8872),
(85, 'Registrar and transfer agent fees', 8873),
(86, 'Reimbursement of parent company expense', 9272),
(87, 'Rental', 8910),
(88, 'Repairs and maintenance', 8960),
(89, 'Repairs and maintenance - boats', 8963),
(90, 'Repairs and maintenance - buildings', 8961),
(91, 'Repairs and maintenance - machinery and equipment', 8964),
(92, 'Repairs and maintenance - vehicles', 8962),
(93, 'Research and development', 9282),
(94, 'Restructuring costs', 8874),
(95, 'Road costs', 9012),
(96, 'Royalty expenses - non-resident', 9278),
(97, 'Royalty expenses - resident', 9277),
(98, 'Salaries and wages', 9060),
(99, 'Salt, bait, and ice', 9138),
(100, 'Securities and commission fees', 8875),
(101, 'Security', 9013),
(102, 'Selling expenses', 9273),
(103, 'Shipping and warehouse expense', 9274),
(104, 'Shop expense', 9132),
(105, 'Small tools', 9131),
(106, 'Storage', 8917),
(107, 'Studio and recording', 8877),
(108, 'Sub-contracts', 9110),
(109, 'Supplies', 9130),
(110, 'Telephone and telecommunications', 9225),
(111, 'Training expense', 8876),
(112, 'Transfer fees', 8870),
(113, 'Travel expenses', 9200),
(114, 'Uniforms', 9133),
(115, 'Upgrade', 9151),
(116, 'Utilities', 9220),
(117, 'Vehicle expenses', 9281),
(118, 'Veterinary fees', 8868),
(119, 'Water', 9276),
(120, 'Warranty expenses', 9222),
(121, 'Withholding taxes', 9283),
(122, 'Cost of Good Sold', 8518),
(123, 'Office expenses', 8810),
(124, 'Motor Vehicles', 1742),
(125, 'payment', 0),
(126, 'Interdivisional', 9285);

-- --------------------------------------------------------

--
-- Table structure for table `dictionary_subcategories`
--

CREATE TABLE `dictionary_subcategories` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `dictionary_category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dictionary_subcategories`
--

INSERT INTO `dictionary_subcategories` (`id`, `name`, `dictionary_category_id`) VALUES
(1, 'intuit', 1),
(2, 'global tax', 1),
(3, 'equifax', 1),
(4, 'marota', 2),
(5, 'canva', 2),
(6, 'clickasnap', 2),
(7, 'upwork', 2),
(8, 'miniso', 3),
(9, 'orbit', 3),
(10, 'lego', 3),
(11, 'long & mcquade', 3),
(12, 'icon experience', 3),
(13, 'toysrus', 3),
(14, 'toy land', 3),
(15, 'smilemakers', 3),
(16, 'E children', 3),
(17, 'alca', 3),
(18, 'urban measure', 3),
(19, 'flower', 3),
(20, 'bath and body', 3),
(21, 'bloomex', 3),
(22, 'oomomo', 3),
(23, 'toys', 3),
(24, 'carters', 3),
(25, 'serkel', 3),
(26, 'kidstrong', 3),
(27, 'nintendo', 3),
(28, 'sony', 3),
(29, 'merch', 3),
(30, 'disney', 3),
(31, 'lindt', 3),
(32, 'gift', 3),
(33, 'marketing', 3),
(34, 'bark', 3),
(35, 'mastermind', 3),
(36, 'petals', 3),
(37, 'hot plates', 3),
(38, 'yellow pages', 3),
(39, 'news', 3),
(40, 'ENVIRO-WORKS', 8),
(41, 'overlimit fee', 10),
(42, 'card fees', 10),
(43, 'bill', 10),
(44, 'fee', 10),
(45, 'telescotia', 10),
(46, 'td', 10),
(47, 'city of st. albert', 14),
(48, 'hailson', 14),
(49, 'epermit', 14),
(50, 'MTO', 14),
(51, 'OMA', 14),
(52, 'corporate', 14),
(53, 'bluehost', 14),
(54, 'cpss', 14),
(55, 'gsuite', 19),
(56, 'quickbooks', 19),
(57, 'godaddy', 19),
(58, 'nchsoftware', 19),
(59, 'anixter', 19),
(60, 'best buy', 19),
(61, 'monoprice', 19),
(62, 'microsoftoffice', 19),
(63, 'teamsnap', 19),
(64, 'adobe acropro', 19),
(65, 'microsoft', 19),
(66, 'partsource', 19),
(67, 'anycubic', 19),
(68, 'bestbuy', 19),
(69, 'siteground', 19),
(70, 'zoho', 19),
(71, 'dell', 19),
(72, 'DYE & DURHAM', 19),
(73, 'adobe', 19),
(74, 'applied information sys', 19),
(75, 'msft', 19),
(76, 'essex', 19),
(77, 'bby', 19),
(78, 'one stop', 19),
(79, 'foreflight', 19),
(80, 'maxigreen', 20),
(81, 'investing', 21),
(82, 'csi', 21),
(83, 'hb usa', 21),
(84, 'endonet', 21),
(85, 'annual fee', 23),
(86, 'dragon', 25),
(87, 'dhl', 26),
(88, 'uline', 26),
(89, 'alaigra', 26),
(90, 'courier', 26),
(91, 'fedex', 26),
(92, 'jetbox', 26),
(93, 'ups', 26),
(94, 'totaline', 26),
(95, 'islamic relief', 28),
(96, 'al-rashid', 28),
(97, 'mosque', 28),
(98, 'islamic', 28),
(99, 'muslim', 28),
(100, 'plan canada', 28),
(101, 'dar sunnah', 28),
(102, 'human concern', 28),
(103, 'yemen food pack', 28),
(104, 'islamique', 28),
(105, 'red cross', 28),
(106, 'bayyinah', 28),
(107, 'canadahelps', 28),
(108, 'operation smile', 28),
(109, 'fundraiser', 28),
(110, 'kizilay', 28),
(111, 'united canadian', 28),
(112, 'humanity', 28),
(113, 'more than a fad', 28),
(114, 'foundation', 28),
(115, 'darul uloom', 28),
(116, 'christ', 28),
(117, 'catholic', 28),
(118, 'world vision', 28),
(119, 'muscular dystrophy can', 28),
(120, 'life for relief', 28),
(121, 'islam', 28),
(122, 'gofndme', 28),
(123, 'school', 28),
(124, 'cnib', 28),
(125, 'launchgood', 28),
(126, 'fatwa', 28),
(127, 'masjid', 28),
(128, 'its you', 28),
(129, 'funding innovation', 28),
(130, 'CITY BINS', 29),
(131, 'SAVE ON BINS', 29),
(132, 'direct energy', 30),
(133, 'atco', 30),
(134, 'ambit', 30),
(135, 'epcor', 30),
(136, 'fitness', 31),
(137, 'beauty', 31),
(138, 'injanation', 31),
(139, 'ymca', 31),
(140, 'ben moss', 31),
(141, 'paris j', 31),
(142, 'party city', 31),
(143, 'iredale', 31),
(144, 'peoples jewellers', 31),
(145, 'lucere', 31),
(146, 'well', 31),
(147, 'amphora', 31),
(148, 'yoga', 31),
(149, 'merle norman', 31),
(150, 'cosmetic', 31),
(151, 'stylists', 31),
(152, 'hellosunnyshop', 31),
(153, 'sung lee', 31),
(154, 'salon', 31),
(155, 'spa', 31),
(156, 'brow artist', 31),
(157, 'brush', 31),
(158, 'nails', 31),
(159, 'love', 31),
(160, 'alallure', 31),
(161, 'fossil', 31),
(162, 'sport', 31),
(163, 'rec', 31),
(164, 'saje', 31),
(165, 'morphe', 31),
(166, 'swiss arabian', 31),
(167, 'NAILBASICS', 31),
(168, 'fansfirst', 31),
(169, 'colasanti', 31),
(170, 'body works', 31),
(171, 'skating', 31),
(172, 'gymnastics', 31),
(173, 'volcom', 31),
(174, 'perfume', 31),
(175, 'envy', 31),
(176, 'sirius', 31),
(177, 'hockey', 31),
(178, 'tickets', 31),
(179, 'movati', 31),
(180, 'basketb', 31),
(181, 'studio', 33),
(182, 'cabelas', 35),
(183, 'petrocan', 38),
(184, '7-eleven', 38),
(185, 'petroleum', 38),
(186, 'esso', 38),
(187, 'shell', 38),
(188, '7 eleven', 38),
(189, 'husky', 38),
(190, 'gas', 38),
(191, 'mobil', 38),
(192, 'centex', 38),
(193, 'petro-canada', 38),
(194, 'coop', 38),
(195, 'hughes', 38),
(196, 'inov tin', 38),
(197, 'station', 38),
(198, 'tags', 38),
(199, 'PIONEER', 38),
(200, 'UPI', 38),
(201, 'fuel', 38),
(202, 'waste', 39),
(203, 'waste mgmt', 39),
(204, 'ppe', 40),
(205, 'dens N dente', 40),
(206, 'carrefour', 40),
(207, 'pride trading', 40),
(208, 'buck valu', 40),
(209, 'showcase', 40),
(210, 'civil', 42),
(211, 'city of', 42),
(212, 'triton', 42),
(213, 'GST', 42),
(214, 'CANADA', 42),
(215, 'ALBERTA', 42),
(216, 'wcb', 45),
(217, 'primmum', 45),
(218, 'cdspi', 45),
(219, 'aviva', 45),
(220, 'security national', 45),
(221, 'intact', 45),
(222, 'mortgage protection plan', 45),
(223, 'wfg', 45),
(224, 'insurance', 45),
(225, 'peace hills', 45),
(226, 'WAWANESA', 45),
(227, 'cash interest', 46),
(228, 'purchase interest', 46),
(229, 'interest', 46),
(230, 'MORTGAGE', 49),
(231, 'LOAN', 50),
(232, 'INVESTMENT', 53),
(233, 'shaw', 55),
(234, 'gogoinflight', 55),
(235, 'youtubepremium', 55),
(236, 'fubo tv', 55),
(237, 'tsn', 55),
(238, 'google', 55),
(239, 'crashplan', 55),
(240, 'fubotv', 55),
(241, 'myfax', 55),
(242, 'tech', 55),
(243, 'COGECO', 55),
(244, 'city soil', 57),
(245, 'dry cleaner', 58),
(246, 'FEDERAL', 59),
(247, 'FEDERAL', 59),
(248, 'planet organic', 65),
(249, 'burger king', 65),
(250, 'apna punjab foods', 65),
(251, 'shoppersdrugmart', 65),
(252, 'liquor', 65),
(253, 'mcdonald', 65),
(254, 'shoppers drug mart', 65),
(255, 'kfc', 65),
(256, 'shawarma', 65),
(257, 'restaurant', 65),
(258, 'basha international foods', 65),
(259, 'sports tab', 65),
(260, 'century casino', 65),
(261, 'sephora', 65),
(262, 'seafood', 65),
(263, 'pita pit', 65),
(264, 'italian centre shop', 65),
(265, 'cactus club', 65),
(266, 'pizza', 65),
(267, 'foodmart', 65),
(268, 'booster juice', 65),
(269, 'subway', 65),
(270, 'mr paintball', 65),
(271, 'ihop', 65),
(272, 'tays food store', 65),
(273, 'jugo juice', 65),
(274, 'guess', 65),
(275, 'paradiso', 65),
(276, 'viphalay laos and thai', 65),
(277, 'oriental noodle house', 65),
(278, 'afghan chopan kebab', 65),
(279, 'mary browns', 65),
(280, 'mt. fuji teppan-yaki', 65),
(281, 'donair', 65),
(282, 'moxies', 65),
(283, 'cafe', 65),
(284, 'ticketmaster', 65),
(285, 'boosterjuice', 65),
(286, 'edo japan', 65),
(287, 'harts table & bar', 65),
(288, 'mcdonalds', 65),
(289, 'lounge', 65),
(290, 'skipthedishes', 65),
(291, 'kernels popcorn', 65),
(292, 'fatburger', 65),
(293, 'crepe delicious', 65),
(294, 'starbucks', 65),
(295, 'zoo', 65),
(296, 'bakery', 65),
(297, 'red lobster', 65),
(298, 'macarons', 65),
(299, 'diwan', 65),
(300, 'baklawa', 65),
(301, 'khan kebabs', 65),
(302, 'turquaz', 65),
(303, 'fine foods', 65),
(304, 'tim hortons', 65),
(305, 'no frills', 65),
(306, 'popeyes', 65),
(307, 'montanas', 65),
(308, 'hyatt place', 65),
(309, 'marshalls', 65),
(310, 'frickn chickn', 65),
(311, 'laziza', 65),
(312, 'pitabake', 65),
(313, 'phoenix range & gun', 65),
(314, 'five guys', 65),
(315, 'macs conv.', 65),
(316, 'root of beirut', 65),
(317, 'abes salon hair', 65),
(318, 'hills mart', 65),
(319, 'minimart', 65),
(320, 'co-op', 65),
(321, 'dickinsfield market', 65),
(322, 'browns shoes', 65),
(323, 'real cdn superstore', 65),
(324, 'almadina halal meat', 65),
(325, 'ibrahim S halal meat', 65),
(326, 'dq grill & chill', 65),
(327, 'ruth S chris steak house', 65),
(328, 'scoop and roll', 65),
(329, 'fayads halla meat deli', 65),
(330, 'sajj factory', 65),
(331, 'rcss', 65),
(332, 'churchs texas chicken', 65),
(333, 'panago', 65),
(334, 'halong bay noodle hous', 65),
(335, 'A & W', 65),
(336, 'h&m', 65),
(337, 'purdys chocolatier', 65),
(338, 'a&w', 65),
(339, 'glengarry food store', 65),
(340, 'cedar sweets', 65),
(341, 'jomaas veggies&fruits', 65),
(342, 'macs convenience', 65),
(343, 'wendys', 65),
(344, 'cinnzeo', 65),
(345, 'dollar tree', 65),
(346, 'mr. pretzels', 65),
(347, 'bath & body works', 65),
(348, 'H & W produce', 65),
(349, 'lavish salon & massage', 65),
(350, 'real canadian sprst', 65),
(351, 'real canadian superstore', 65),
(352, 'food master M & M', 65),
(353, 'alqitta nuts', 65),
(354, 'cappadocia', 65),
(355, 'castlebake', 65),
(356, 'castelbake', 65),
(357, 'relayred', 65),
(358, 'hudson', 65),
(359, 'yellow submarine', 65),
(360, 'montfort', 65),
(361, 'crown pastries', 65),
(362, 'longos', 65),
(363, 'avondale store', 65),
(364, 'sunset grill', 65),
(365, 'antica pizzeria', 65),
(366, 'bubble tea', 65),
(367, 'pitas & burritos', 65),
(368, 'villa madina', 65),
(369, 'hero certified burgers', 65),
(370, 'buka maranga', 65),
(371, 'churchs chicken', 65),
(372, 'supermarket', 65),
(373, 'food ', 65),
(374, 'chatime', 65),
(375, 'yeg burger', 65),
(376, 'cedars deli', 65),
(377, 'krispy kreme', 65),
(378, 'middle eastern cui', 65),
(379, 'mall', 65),
(380, 'sweets', 65),
(381, 'cuisin', 65),
(382, 'beijing house', 65),
(383, 'couche-tard', 65),
(384, 'trattoria', 65),
(385, 'timeout', 65),
(386, 'depanneur', 65),
(387, 'kebab', 65),
(388, 'allo mon coco', 65),
(389, 'ryu', 65),
(390, 'paramount', 65),
(391, 'buffalo bill wings', 65),
(392, 'babylon qithara', 65),
(393, 'pizzeria', 65),
(394, 'dennys', 65),
(395, 'cora', 65),
(396, 'aladdins casbah', 65),
(397, 'castle bake', 65),
(398, 'dutch pannekoek ', 65),
(399, 'joey', 65),
(400, 'anatolia', 65),
(401, 'barcelos', 65),
(402, 'sporting goods', 65),
(403, 'wmt', 65),
(404, 'dazn', 65),
(405, 'loblaws', 65),
(406, 'saxonwell', 65),
(407, 'jay bees', 65),
(408, 'bk', 65),
(409, 'swiss chalet', 65),
(410, 'sedra', 65),
(411, 'sahara', 65),
(412, 'fayads', 65),
(413, 'real canadian super', 65),
(414, 'save on foods', 65),
(415, 'instacart', 65),
(416, 'raceway', 65),
(417, 'neojuicery', 65),
(418, 'whalers village', 65),
(419, 'wem', 65),
(420, 'tutti frutti', 65),
(421, 'nellos', 65),
(422, 'capture the moment', 65),
(423, 'goldhunt', 65),
(424, 'cineplex', 65),
(425, 'glow juicery', 65),
(426, 'snowy village', 65),
(427, 'pasta', 65),
(428, 'landmark', 65),
(429, 'braidies tavern', 65),
(430, 'state & main', 65),
(431, 'rcls', 65),
(432, 'taco', 65),
(433, 'deli', 65),
(434, 'ice cream', 65),
(435, 'fries', 65),
(436, 'veggie', 65),
(437, 'asian village', 65),
(438, 'meadows', 65),
(439, 'wok', 65),
(440, 'lotte', 65),
(441, 'currie', 65),
(442, 'spices', 65),
(443, 'restaura', 65),
(444, 'pub', 65),
(445, 'convenienc', 65),
(446, 'all india', 65),
(447, 'mcdonal', 65),
(448, 'trampoline', 65),
(449, 'grocery', 65),
(450, 'meat shop', 65),
(451, 'village', 65),
(452, 'samosa', 65),
(453, 'play', 65),
(454, 'smittys', 65),
(455, 'grill', 65),
(456, 'h&w', 65),
(457, 'royal treats', 65),
(458, 'white spot', 65),
(459, 'ace west', 65),
(460, 'massage', 65),
(461, 'weed', 65),
(462, 'treats', 65),
(463, 'tropical', 65),
(464, 'cobs', 65),
(465, 'italian', 65),
(466, 'meat', 65),
(467, 'african', 65),
(468, 'lazio', 65),
(469, 'brewster', 65),
(470, 'beach', 65),
(471, 'amore mio', 65),
(472, 'sushi', 65),
(473, 'freshly squeezed', 65),
(474, 'browns', 65),
(475, 'donnas', 65),
(476, 'circle K', 65),
(477, 'sultan', 65),
(478, 'mado dondurma', 65),
(479, 'minibar', 65),
(480, 'bulk barn', 65),
(481, 'doordash', 65),
(482, 'kernels', 65),
(483, 'vending', 65),
(484, 'cookies', 65),
(485, 'pearsons', 65),
(486, 'crepe', 65),
(487, 'boutique', 65),
(488, 'caffe', 65),
(489, 'juice', 65),
(490, 'violino', 65),
(491, 'granary', 65),
(492, 'wholesale', 65),
(493, 'marjane', 65),
(494, 'le petit', 65),
(495, 'finefish', 65),
(496, 'rest', 65),
(497, 'capadocia', 65),
(498, 'best bite', 65),
(499, 'snack', 65),
(500, 'freshco', 65),
(501, 'boba palace', 65),
(502, 'spice', 65),
(503, 'roastery', 65),
(504, 'desi', 65),
(505, 'fruiticana', 65),
(506, 'games', 65),
(507, 'R W E', 65),
(508, 'chicken', 65),
(509, 'hunt', 65),
(510, 'grandiose', 65),
(511, 'burger', 65),
(512, 'karahi', 65),
(513, 'fetta', 65),
(514, 'heirloom', 65),
(515, 'savoys', 65),
(516, 'mudpot', 65),
(517, 'india', 65),
(518, 'h-mart', 65),
(519, 'tummy full', 65),
(520, 'nuts', 65),
(521, 'groceries', 65),
(522, 'foods', 65),
(523, 'allo', 65),
(524, 'music', 65),
(525, 'rockin robyns', 65),
(526, 'buco', 65),
(527, 'beer', 65),
(528, 'dorinku', 65),
(529, 'fruit', 65),
(530, 'dream tea', 65),
(531, 'chinese', 65),
(532, 'momenthouse', 65),
(533, 'tock mission', 65),
(534, 'jacks bernard', 65),
(535, 'carmelis', 65),
(536, 'meal', 65),
(537, 'kabab', 65),
(538, 'reddimart', 65),
(539, 'second cup', 65),
(540, 'clyde corner', 65),
(541, 'mikes famous', 65),
(542, 'smoke', 65),
(543, 'lunch', 65),
(544, 'panda express', 65),
(545, 'carls jr', 65),
(546, 'tokyo express', 65),
(547, 'CANNABIS', 65),
(548, 'SPIRITLEAF', 65),
(549, 'PLANTLIFE', 65),
(550, 'MARBLE SLAB', 65),
(551, 'opa', 65),
(552, 'nandos', 65),
(553, 'eggspectation', 65),
(554, 'chuck E', 65),
(555, 'bake', 65),
(556, 'boil', 65),
(557, 'orange julius', 65),
(558, 'shisha', 65),
(559, 'tea', 65),
(560, 'daikoku', 65),
(561, 'no frill', 65),
(562, 'bar', 65),
(563, 'BETTYS', 65),
(564, 'SUPERS', 65),
(565, 'pur', 65),
(566, 'bianco', 65),
(567, 'mart', 65),
(568, 'y&t', 65),
(569, 'market', 65),
(570, 'plaza', 65),
(571, 'keg', 65),
(572, 'earl', 65),
(573, 'gangnam', 65),
(574, 'teriyaki', 65),
(575, 'cakes', 65),
(576, 'blowers', 65),
(577, 'bowling', 65),
(578, 'sharper edge', 65),
(579, 'famoso', 65),
(580, 'shed', 65),
(581, 'diner', 65),
(582, 'changs', 65),
(583, 'golf', 65),
(584, 'sub', 65),
(585, 'taste', 65),
(586, 'popcorn', 65),
(587, 'dickeys', 65),
(588, 'beavertails', 65),
(589, 'ahs accounts', 66),
(590, 'rexall pharmacy', 66),
(591, 'evansdale pharmacy', 66),
(592, 'eco medical equipment', 66),
(593, 'health centre', 66),
(594, 'pharmacy', 66),
(595, 'dynalife', 66),
(596, 'lifelabs', 66),
(597, 'braces', 66),
(598, 'edds', 66),
(599, 'health', 66),
(600, 'biocare', 66),
(601, 'implant', 66),
(602, 'med', 66),
(603, 'wellness', 66),
(604, 'eastern current', 66),
(605, 'invisalign', 66),
(606, 'kucey', 66),
(607, 'align', 66),
(608, 'endontics', 66),
(609, 'total focus', 66),
(610, 'conmetior', 66),
(611, 'sports plus', 66),
(612, 'ther', 66),
(613, 'uc baby', 66),
(614, 'smile', 66),
(615, 'eye', 66),
(616, 'spinedeck', 66),
(617, 'pharmacie', 66),
(618, 'phcie', 66),
(619, 'acupuncture', 66),
(620, 'falah', 66),
(621, 'MEMOR', 66),
(622, 'pharma', 66),
(623, 'doctor', 66),
(624, 'epilepsy', 66),
(625, 'pediatric', 66),
(626, 'optometrist', 66),
(627, 'examination', 66),
(628, 'blue cross', 66),
(629, 'clinic', 66),
(630, 'lasik', 66),
(631, 'cpaacp', 68),
(632, 'the grange', 68),
(633, 'hoa', 68),
(634, 'patreon', 68),
(635, 'orchards resident', 68),
(636, 'fkmc', 68),
(637, 'vip cars', 70),
(638, 'thrifty car', 70),
(639, 'carhire', 70),
(640, 'avis', 70),
(641, 'budget', 70),
(642, 'ink', 74),
(643, 'SHRED', 74),
(644, 'etsy', 74),
(645, 'wesclean', 75),
(646, 'greenhouse', 76),
(647, 'canvas', 76),
(648, 'hayes', 77),
(649, 'simplekleen', 77),
(650, 'pest control', 77),
(651, 'pest', 77),
(652, 'PLUMBING', 77),
(653, 'dental', 78),
(654, 'barbershop', 78),
(655, 'sport and spine', 78),
(656, 'homeserve', 78),
(657, 'massage experts', 78),
(658, 'orthodontic', 78),
(659, 'inc inc', 78),
(660, 'spasation', 78),
(661, 'hospital', 78),
(662, 'fireplace guy', 78),
(663, 'chiropractic', 78),
(664, 'paragon testing', 78),
(665, 'becan immigration', 78),
(666, 'tfwp', 78),
(667, 'dba', 78),
(668, 'rtdrs', 78),
(669, 'wu', 78),
(670, 'westernunion', 78),
(671, 'leb411', 78),
(672, 'kickstarter', 78),
(673, 'city of edmonton', 78),
(674, 'smart dubai', 78),
(675, 'citizenship', 78),
(676, 'indeed', 78),
(677, 'gsu', 78),
(678, 'ab birth', 78),
(679, 'corp canada', 78),
(680, 'lawdepot', 78),
(681, 'moneythumb', 78),
(682, 'tax', 78),
(683, 'law', 78),
(684, 'estimate', 78),
(685, 'wix', 78),
(686, 'PAYMENTEVOLUTION', 78),
(687, 'eventbrite', 79),
(688, 'enterprise', 87),
(689, 'select equipment', 87),
(690, 'ocean trailer', 87),
(691, 'furnace', 88),
(692, 'royal lock', 88),
(693, 'taskrabbit', 88),
(694, 'parts', 88),
(695, 'reliance home', 88),
(696, 'construction', 88),
(697, 'goodman', 88),
(698, 'master', 90),
(699, 'pro detail supply', 92),
(700, 'millwoods auto centre', 92),
(701, 'sams solution auto', 92),
(702, 'jiffy lube', 92),
(703, 'mr. lube', 92),
(704, 'napa', 92),
(705, 'auto repair', 92),
(706, 'princess auto', 92),
(707, 'amp auto body', 92),
(708, 'century motors', 92),
(709, 'tk truck body', 92),
(710, 'volkswagen', 92),
(711, 'U wash car', 92),
(712, 'lube city', 92),
(713, 'kal tire', 92),
(714, 'ecotire tire shop', 92),
(715, 'oil & tires', 92),
(716, 'windshield', 92),
(717, 'dodge', 92),
(718, 'spyhill', 92),
(719, 'mercedes benz', 92),
(720, 'meineke', 92),
(721, 'toyota', 92),
(722, 'body shop', 92),
(723, 'auto', 92),
(724, 'truck', 92),
(725, 'car wash', 92),
(726, 'retrofit', 92),
(727, 'fort garry', 92),
(728, 'tire', 92),
(729, 'wash', 92),
(730, 'hyundai', 92),
(731, 'allspec', 92),
(732, 'lexus', 92),
(733, 'LUBE KING', 92),
(734, 'PETES PAINT', 92),
(735, 'midas', 92),
(736, 'mazda', 92),
(737, 'muffler', 92),
(738, 'kia', 92),
(739, 'jeep', 92),
(740, 'lincoln', 92),
(741, 'lube', 97),
(742, 'alarmforce', 101),
(743, 'securtek', 101),
(744, 'united security', 101),
(745, 'adt', 101),
(746, 'fraud', 101),
(747, 'alltron', 101),
(748, 'armstrongs', 101),
(749, 'lock', 101),
(750, 'fire', 101),
(751, 'safe', 101),
(752, 'SECURITY', 101),
(753, 'u-haul', 106),
(754, 'storage', 106),
(755, 'vortek construction', 108),
(756, 'rh services', 108),
(757, 'naiad irrigation', 108),
(758, 'cleaners warehouse', 109),
(759, 'carpet superstore', 109),
(760, 'glenora lumber', 109),
(761, 'home depot', 109),
(762, 'dulux paints', 109),
(763, 'lowes', 109),
(764, 'staples', 109),
(765, 'fancy windows', 109),
(766, 'cdn tire', 109),
(767, 'supplies', 109),
(768, 'consolidated gupsum', 109),
(769, 'vistaprint', 109),
(770, 'plywood', 109),
(771, 'rona', 109),
(772, 'fancy doors & mouldings', 109),
(773, 'lumber', 109),
(774, 'wal-mart', 109),
(775, 'cdn tire', 109),
(776, 'dollarama', 109),
(777, 'costco', 109),
(778, 'aliexpress', 109),
(779, 'harry rosen', 109),
(780, 'staples', 109),
(781, 'amazon', 109),
(782, 'toys R us', 109),
(783, 'hudsons bay', 109),
(784, 'holt renfrew', 109),
(785, 'nofrills', 109),
(786, 'groupon', 109),
(787, 'thyme maternity', 109),
(788, 'army navy dept store', 109),
(789, 'london drugs', 109),
(790, 'texonic av mounting', 109),
(791, 'elsafadi', 109),
(792, 'healthcare supply', 109),
(793, 'memory express', 109),
(794, 'aldo', 109),
(795, 'safeway', 109),
(796, 'cellularoutfitter', 109),
(797, 'urban behaviour', 109),
(798, 'toner laser centre', 109),
(799, 'sherwin-williams', 109),
(800, 'albaraka meat shop', 109),
(801, 'sobeys', 109),
(802, 'mildly chinese herbal', 109),
(803, 'senza', 109),
(804, 'appliance outlet', 109),
(805, 'dynamite', 109),
(806, 'sportschek', 109),
(807, 'sport chek', 109),
(808, 'kijiji', 109),
(809, 'amzn', 109),
(810, 'save foods', 109),
(811, 'henry schein', 109),
(812, 'recall system solutions', 109),
(813, 'medicine shoppe', 109),
(814, 'drug', 109),
(815, 'polymershapes', 109),
(816, 'ardene', 109),
(817, 'fabricland', 109),
(818, 'hugo boss', 109),
(819, 'walmart', 109),
(820, 'healthcare solutions', 109),
(821, 'calvin klein', 109),
(822, 'hajars halal meats', 109),
(823, 'gap', 109),
(824, 'show warehouse', 109),
(825, 'thebay', 109),
(826, 'puma', 109),
(827, 'old navy', 109),
(828, 'softmoc', 109),
(829, 'ikea', 109),
(830, 'visions electronics', 109),
(831, 'wayfair', 109),
(832, 'nike', 109),
(833, 'shoe warehouse', 109),
(834, 'lululemon', 109),
(835, 'michaels', 109),
(836, 'education station', 109),
(837, 'mosquito', 109),
(838, 'TOOLS', 109),
(839, 'RICHELIEU', 109),
(840, 'supply', 109),
(841, 'product', 109),
(842, 'refrigeration', 109),
(843, 'diamond ice', 109),
(844, 'mckinley', 109),
(845, 'universal rewind', 109),
(846, 'bell mobility', 110),
(847, 'koodo mobile', 110),
(848, 'fido mobile', 110),
(849, 'telus', 110),
(850, 'cellxpress', 110),
(851, 'freedom mobile', 110),
(852, 'rogers', 110),
(853, 'apple', 110),
(854, 'mightycall', 110),
(855, 'cellular toy shop', 110),
(856, 'crc', 110),
(857, 'apl', 110),
(858, 'spotify', 110),
(859, 'fido', 110),
(860, 'lg', 110),
(861, 'otterbox', 110),
(862, 'cell xpress', 110),
(863, 'wesbell', 110),
(864, 'virgin', 110),
(865, 'wirelesswave', 110),
(866, 'netflix', 110),
(867, 'tv', 110),
(868, 'corpcentre', 110),
(869, 'logmein', 110),
(870, 'phone', 110),
(871, 'UNITE COMMUNICATIONS', 110),
(872, 'OOMA', 110),
(873, 'plan', 110),
(874, 'gotoconnect', 110),
(875, 'scholarships', 111),
(876, 'indigo', 111),
(877, 'prepdoctors', 111),
(878, 'uofa', 111),
(879, 'spectrum', 111),
(880, 'firstaid', 111),
(881, 'wpy', 111),
(882, 'ada&c', 111),
(883, 'crdha', 111),
(884, 'bookjewl', 111),
(885, 'springer', 111),
(886, 'librar', 111),
(887, 'olivers learning', 111),
(888, 'safety coordination', 111),
(889, 'rcdso', 111),
(890, 'college', 111),
(891, 'cultural connections', 111),
(892, 'acusport', 111),
(893, 'udemy', 111),
(894, 'ab transportation', 111),
(895, 'noorart', 111),
(896, 'ielts', 111),
(897, 'pikos', 111),
(898, 'education', 111),
(899, 'duolingo', 111),
(900, 'scholastic', 111),
(901, 'goodwill', 111),
(902, 'stockscores', 111),
(903, 'homeschl', 111),
(904, 'centennial', 111),
(905, 'threshold aviation', 111),
(906, 'achieve', 111),
(907, 'cpr', 111),
(908, 'cmu', 111),
(909, 'learn', 111),
(910, 'risio', 111),
(911, 'airbnb', 112),
(912, 'airportrentals', 112),
(913, 'hostelling', 112),
(914, 'expedia', 112),
(915, 'air can', 112),
(916, 'flighthub', 112),
(917, 'hotel', 112),
(918, 'westjet', 112),
(919, 'uber', 113),
(920, 'royal jordan', 113),
(921, 'covid19 test', 113),
(922, 'doubletree', 113),
(923, 'atpstaxi&limo', 113),
(924, 'comfort inn', 113),
(925, 'americana conference reso', 113),
(926, 'travelers canada', 113),
(927, 'cheaptix', 113),
(928, 'hilton falls', 113),
(929, 'hilton', 113),
(930, 'yyz otg', 113),
(931, 'bird ', 113),
(932, 'limride', 113),
(933, 'banff', 113),
(934, 'guide', 113),
(935, 'lake louise', 113),
(936, 'border', 113),
(937, 'holiday inn', 113),
(938, 'bentley', 113),
(939, 'resort', 113),
(940, 'uhaul', 113),
(941, 'emirates', 113),
(942, 'delta ', 113),
(943, 'passport', 113),
(944, 'days inn', 113),
(945, 'park', 113),
(946, 'alsa', 113),
(947, 'relay', 113),
(948, 'sunwing', 113),
(949, 'bookmyvacay', 113),
(950, 'book my vacay', 113),
(951, 'american ai', 113),
(952, 'cayman villas', 113),
(953, 'greyhound', 113),
(954, 'sheraton', 113),
(955, 'photo stop', 113),
(956, 'transat', 113),
(957, 'hostel', 113),
(958, 'river cree', 113),
(959, 'yellow cab', 113),
(960, 'taxi', 113),
(961, 'trail', 113),
(962, 'cab', 113),
(963, 'suites', 113),
(964, 'burrard', 113),
(965, 'duty free', 113),
(966, 'herschel', 113),
(967, 'water slide', 113),
(968, 'drumheller', 113),
(969, 'lodge', 113),
(970, 'jasper', 113),
(971, 'iga', 113),
(972, 'lodging', 113),
(973, 'fly', 113),
(974, 'atlantis', 113),
(975, 'sawridge', 113),
(976, 'sylvan lake', 113),
(977, 'elk island', 113),
(978, 'revelstoke', 113),
(979, 'cruise', 113),
(980, 'hicv', 113),
(981, 'canalta', 113),
(982, 'best western', 113),
(983, 'baymont', 113),
(984, 'pay stn', 113),
(985, 'ferry', 113),
(986, 'dubai', 113),
(987, 'madina', 113),
(988, 'makkah', 113),
(989, 'travel', 113),
(990, 'camping', 113),
(991, 'saudi', 113),
(992, 'niagara', 113),
(993, 'mississauga', 113),
(994, 'nissan', 114),
(995, 'honda', 114),
(996, 'double ace auto', 114),
(997, 'winners', 114),
(998, 'shoe company', 114),
(999, 'urban planet', 114),
(1000, 'jack and jones', 114),
(1001, 'zara', 114),
(1002, 'simons', 114),
(1003, 'designer brands shoes', 114),
(1004, 'champs', 114),
(1005, 'giant tiger', 114),
(1006, 'bootlegger', 114),
(1007, 'ae', 114),
(1008, 'barber shop', 114),
(1009, 'penningtons', 114),
(1010, 'sportchek', 114),
(1011, 'brownsshoes', 114),
(1012, 'seymos barber', 114),
(1013, 'pull & bear', 114),
(1014, 'ecco', 114),
(1015, 'lacoste', 114),
(1016, 'van heusen', 114),
(1017, 'tailor', 114),
(1018, 'marks', 114),
(1019, 'vans', 114),
(1020, 'childrens place', 114),
(1021, 'adidas', 114),
(1022, 'le chateau', 114),
(1023, 'crossiron mills', 114),
(1024, 'rw', 114),
(1025, 'bananarepublic', 114),
(1026, 'saksoff5th', 114),
(1027, 'gcds', 114),
(1028, 'maternity', 114),
(1029, 'mountain warehouse', 114),
(1030, 'monyberry', 114),
(1031, 'ivrose', 114),
(1032, 'wish', 114),
(1033, 'shopsmarter', 114),
(1034, 'burberry', 114),
(1035, 'jaanuu', 114),
(1036, 'londonderry', 114),
(1037, 'value village', 114),
(1038, 'ua', 114),
(1039, 'needen', 114),
(1040, 'mega savers', 114),
(1041, 'barber', 114),
(1042, 'urban behavior', 114),
(1043, 'peavey', 114),
(1044, 'dsw', 114),
(1045, 'waikiki', 114),
(1046, 'center point', 114),
(1047, 'fashion', 114),
(1048, 'shein', 114),
(1049, 'cleo', 114),
(1050, 'br', 114),
(1051, 'monsoon', 114),
(1052, 'reitman', 114),
(1053, 'designer depot', 114),
(1054, 'uniform', 114),
(1055, 'outlet', 114),
(1056, 'laura', 114),
(1057, 'victorias secret', 114),
(1058, 'tsawwassen', 114),
(1059, 'tsewwassen', 114),
(1060, 'tory burch', 114),
(1061, 'arden', 114),
(1062, 'suzy shier', 114),
(1063, 'tommy hilfiger', 114),
(1064, 'melanie lyne', 114),
(1065, 'gucci', 114),
(1066, 'reebok', 114),
(1067, 'oldnavy', 114),
(1068, 'joefresh', 114),
(1069, 'defacto', 114),
(1070, 'decathlon', 114),
(1071, 'sara folard', 114),
(1072, 'opulence', 114),
(1073, 'eddie bauer', 114),
(1074, 'boots', 114),
(1075, 'kashkha', 114),
(1076, 'abaya', 114),
(1077, 'g-star', 114),
(1078, 'spring', 114),
(1079, 'canada goose', 114),
(1080, 'foot locker', 114),
(1081, 'west 49', 114),
(1082, 'boathouse', 114),
(1083, 'steve madden', 114),
(1084, 'skechers', 114),
(1085, 'armour', 114),
(1086, 'nordstrom', 114),
(1087, 'wear', 114),
(1088, 'clothing', 114),
(1089, 'hijab', 114),
(1090, 'ilahui', 114),
(1091, 'impark', 117),
(1092, 'air', 117),
(1093, 'carfax', 117),
(1094, 'vincheckup', 117),
(1095, 'in & out registry', 117),
(1096, 'alberta one stop registry', 117),
(1097, 'your spot', 117),
(1098, 'parking ppl', 117),
(1099, 'stationnement centre', 117),
(1100, 'ua u-park', 117),
(1101, 'myalberta', 117),
(1102, 'traffic', 117),
(1103, 'aara', 117),
(1104, 'akco', 117),
(1105, 'ama', 117),
(1106, 'regis', 117),
(1107, 'regi', 117),
(1108, 'impound', 117),
(1109, 'rv', 117),
(1110, 'rcmp', 117),
(1111, 'road test', 117),
(1112, 'towing', 117),
(1113, 'stahl', 117),
(1114, 'nortrux', 117),
(1115, 'ford', 117),
(1116, 'pet valu', 118),
(1117, 'petsmart', 118),
(1118, 'trupanion', 118),
(1119, 'rocky', 118),
(1120, 'culligan', 119),
(1121, 'unicon concrete', 122),
(1122, 'milltrade building', 122),
(1123, 'shan construction service', 122),
(1124, 'c.o.d. concrete', 122),
(1125, 'capital concrete', 122),
(1126, 'hilti', 122),
(1127, 'refinery serv', 122),
(1128, 'cloverdale paint', 122),
(1129, 'brick', 122),
(1130, 'finning', 122),
(1131, 'haden pumping', 122),
(1132, 'homesense', 122),
(1133, 'entwistle concrete', 122),
(1134, 'conuvo construction', 122),
(1135, 'kenroc', 122),
(1136, 'landscape', 122),
(1137, 'lafarge', 122),
(1138, 'citagenix', 122),
(1139, 'dentsply', 122),
(1140, 'den mat', 122),
(1141, 'denmat', 122),
(1142, 'laminati', 122),
(1143, 'texonic', 122),
(1144, 'synca', 122),
(1145, 'univet', 122),
(1146, 'drywall', 122),
(1147, 'northland moulding', 122),
(1148, 'brotherhood', 122),
(1149, 'riverside motorsports', 122),
(1150, 'canadian wheel', 122),
(1151, 'marina', 122),
(1152, 'orascoptic', 122),
(1153, 'landscaping', 122),
(1154, 'manderley', 122),
(1155, 'cascade', 122),
(1156, 'equipment', 122),
(1157, 'distributors', 122),
(1158, 'ruyan', 122),
(1159, 'queen ', 122),
(1160, 'akberi', 122),
(1161, 'ramez', 122),
(1162, 'planmeca', 122),
(1163, 'anatomage', 122),
(1164, 'osteoid', 122),
(1165, 'dentbear', 122),
(1166, 'x-nav', 122),
(1167, 'prodent', 122),
(1168, 'practicon', 122),
(1169, 'ultrasonic', 122),
(1170, 'dbw', 122),
(1171, 'amre', 122),
(1172, 'tile & stone', 122),
(1173, 'TILE', 122),
(1174, 'FASTENERS', 122),
(1175, 'GLASS', 122),
(1176, 'auction', 122),
(1177, 'trovadent', 122),
(1178, 'CUMMINS', 122),
(1179, 'ufa', 122),
(1180, 'leon', 123),
(1181, 'coca cola', 123),
(1182, 'nut and bolt', 123),
(1183, 'showhome', 123),
(1184, 'florist', 123),
(1185, 'jysk', 123),
(1186, 'bed bath & beyond', 123),
(1187, 'wholesale liquidators', 123),
(1188, 'liquidation', 123),
(1189, 'woowlish', 123),
(1190, 'inspire uplift', 123),
(1191, 'zanhome', 123),
(1192, 'Z A N home', 123),
(1193, 'garden scents', 123),
(1194, 'stokes', 123),
(1195, 'giftsstore', 123),
(1196, 'hypermarket', 123),
(1197, 'ansar', 123),
(1198, 'discount', 123),
(1199, 'sleep country', 123),
(1200, 'thrift', 123),
(1201, 'quilts', 123),
(1202, 'oud', 123),
(1203, 'buckvalu', 123),
(1204, 'Lighting', 123),
(1205, 'velvet rose', 123),
(1206, 'dollar store', 123),
(1207, 'printer', 123),
(1208, 'buck', 123),
(1209, 'ritchie bros', 124),
(1210, 'pick-n-pull', 124),
(1211, 'stewart belland', 124),
(1212, 'stark auto', 124),
(1213, 'i pull U pull', 124),
(1214, 'payment', 125);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2023-01-14 21:21:38.389605', '125', 'DictionaryCategories object (125)', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 7, 2),
(2, '2023-01-14 21:21:58.135853', '125', 'DictionaryCategories object (125)', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 7, 2),
(3, '2023-01-14 21:48:04.658937', '1282', 'DictionarySubcategories object (1282)', 1, '[{\"added\": {}}]', 8, 2);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'home', 'dictionarycategories'),
(8, 'home', 'dictionarysubcategories'),
(9, 'home', 'document'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-01-06 22:02:09.656624'),
(2, 'auth', '0001_initial', '2023-01-06 22:02:09.920118'),
(3, 'admin', '0001_initial', '2023-01-06 22:02:09.973964'),
(4, 'admin', '0002_logentry_remove_auto_add', '2023-01-06 22:02:09.983938'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-01-06 22:02:09.992913'),
(6, 'contenttypes', '0002_remove_content_type_name', '2023-01-06 22:02:10.028079'),
(7, 'auth', '0002_alter_permission_name_max_length', '2023-01-06 22:02:10.064535'),
(8, 'auth', '0003_alter_user_email_max_length', '2023-01-06 22:02:10.077501'),
(9, 'auth', '0004_alter_user_username_opts', '2023-01-06 22:02:10.086478'),
(10, 'auth', '0005_alter_user_last_login_null', '2023-01-06 22:02:10.105916'),
(11, 'auth', '0006_require_contenttypes_0002', '2023-01-06 22:02:10.108910'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2023-01-06 22:02:10.118246'),
(13, 'auth', '0008_alter_user_username_max_length', '2023-01-06 22:02:10.131197'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2023-01-06 22:02:10.144157'),
(15, 'auth', '0010_alter_group_name_max_length', '2023-01-06 22:02:10.168333'),
(16, 'auth', '0011_update_proxy_permissions', '2023-01-06 22:02:10.178339'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2023-01-06 22:02:10.191285'),
(18, 'home', '0001_initial', '2023-01-06 22:02:10.228000'),
(19, 'sessions', '0001_initial', '2023-01-06 22:02:10.243530');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('t2x7cgslncy4hq8e840v2olwqxw7uslq', '.eJxVizsOwjAQBe_iGlm2N05iSiTOYe0vigWYCCcV4u4QiQKaV7yZeZqM2zrnrekjFzFH483h9yPki9Yd4LI0uwOta2Fcy71avWG52vO-p6_4V8_Y5k_qCFSiEjMqDg5VHCfuknBI0YMXogFEgkuhB-pRwDONI6Sp6-I4OfN6A3jlN8Q:1pDv64:t-pfjUvwDkARdYypUR248I-OC5tzv67C_FypABIe5cs', '2023-01-20 22:21:56.993125');

-- --------------------------------------------------------

--
-- Table structure for table `home_document`
--

CREATE TABLE `home_document` (
  `id` int(11) NOT NULL,
  `docfile` varchar(100) NOT NULL,
  `date` datetime(6) NOT NULL,
  `submitter_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- Indexes for table `dictionary_categories`
--
ALTER TABLE `dictionary_categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dictionary_subcategories`
--
ALTER TABLE `dictionary_subcategories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_dictionary_categorie_id` (`dictionary_category_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `home_document`
--
ALTER TABLE `home_document`
  ADD PRIMARY KEY (`id`),
  ADD KEY `home_document_submitter_id_89ebe35c_fk_auth_user_id` (`submitter_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `company`
--
ALTER TABLE `company`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `dictionary_categories`
--
ALTER TABLE `dictionary_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=127;

--
-- AUTO_INCREMENT for table `dictionary_subcategories`
--
ALTER TABLE `dictionary_subcategories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1283;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `home_document`
--
ALTER TABLE `home_document`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `company`
--
ALTER TABLE `company`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `dictionary_subcategories`
--
ALTER TABLE `dictionary_subcategories`
  ADD CONSTRAINT `fk_dictionary_categorie_id` FOREIGN KEY (`dictionary_category_id`) REFERENCES `dictionary_categories` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `home_document`
--
ALTER TABLE `home_document`
  ADD CONSTRAINT `home_document_submitter_id_89ebe35c_fk_auth_user_id` FOREIGN KEY (`submitter_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
