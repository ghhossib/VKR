-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Июн 22 2026 г., 23:06
-- Версия сервера: 10.4.32-MariaDB
-- Версия PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `vkr`
--

-- --------------------------------------------------------

--
-- Структура таблицы `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `auth_permission`
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
(25, 'Can add car', 7, 'add_car'),
(26, 'Can change car', 7, 'change_car'),
(27, 'Can delete car', 7, 'delete_car'),
(28, 'Can view car', 7, 'view_car'),
(29, 'Can add booking', 8, 'add_booking'),
(30, 'Can change booking', 8, 'change_booking'),
(31, 'Can delete booking', 8, 'delete_booking'),
(32, 'Can view booking', 8, 'view_booking'),
(33, 'Can add booking message', 9, 'add_bookingmessage'),
(34, 'Can change booking message', 9, 'change_bookingmessage'),
(35, 'Can delete booking message', 9, 'delete_bookingmessage'),
(36, 'Can view booking message', 9, 'view_bookingmessage'),
(37, 'Can add booking status history', 10, 'add_bookingstatushistory'),
(38, 'Can change booking status history', 10, 'change_bookingstatushistory'),
(39, 'Can delete booking status history', 10, 'delete_bookingstatushistory'),
(40, 'Can view booking status history', 10, 'view_bookingstatushistory');

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user`
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
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$x2Th9muXOztfjb8R0GEVN0$7wta96wOPN8nAJE/knWyioIpYPVRYUkV8GE0pP13jtM=', '2026-06-22 20:55:36.063651', 0, 'user', '', '', 'user@gmail.com', 0, 1, '2026-05-11 19:44:03.989700'),
(2, 'pbkdf2_sha256$600000$NhVd6vi4wEX2wR6W9KGpmV$1Y3uxqyLBsvC4LnZYYavorC1mQsjem/Eqh28wCvK1Fw=', '2026-06-22 20:55:58.647496', 0, '123', '', '', 'asd@gmail.com', 0, 1, '2026-05-11 19:45:09.313633'),
(5, 'pbkdf2_sha256$600000$0IsBckCDdVRL0F1xbZ4mU0$fvFxWSUBPsNshWOzA9WFTD47AVlz+ptH+Q064vMEXus=', '2026-06-22 20:57:21.553370', 0, 'nik16', '', '', 'nik16@gmail.com', 1, 1, '2026-05-13 11:29:40.085920'),
(8, 'pbkdf2_sha256$600000$ZaxAzPCXsZmFoUtg6yC13Z$dC/hkcEpWgbxKiQlYJBD0GE+ZHjHBuMnoyV1EZNi5fU=', '2026-06-22 20:55:46.902081', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2026-06-22 20:51:12.536329');

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `cars_booking`
--

CREATE TABLE `cars_booking` (
  `id` bigint(20) NOT NULL,
  `start_at` datetime(6) NOT NULL,
  `end_at` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `car_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `manager_comment` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `cars_booking`
--

INSERT INTO `cars_booking` (`id`, `start_at`, `end_at`, `status`, `created_at`, `car_id`, `user_id`, `manager_comment`) VALUES
(1, '2026-05-11 20:30:00.000000', '2026-05-11 23:30:00.000000', 'canceled', '2026-05-13 13:02:01.765820', 1, 2, ''),
(2, '2026-05-12 00:00:00.000000', '2026-05-12 02:00:00.000000', 'canceled', '2026-05-13 13:02:01.765820', 1, 2, ''),
(3, '2026-05-11 20:54:00.000000', '2026-05-11 21:54:00.000000', 'canceled', '2026-05-13 13:02:01.765820', 3, 2, ''),
(4, '2026-05-11 21:02:00.000000', '2026-05-12 21:02:00.000000', 'canceled', '2026-05-13 13:02:01.765820', 1, 2, ''),
(5, '2026-05-13 20:00:00.000000', '2026-05-13 22:00:00.000000', 'canceled', '2026-05-13 13:02:01.765820', 1, 2, 'отказ'),
(6, '2026-05-13 11:55:00.000000', '2026-05-13 12:55:00.000000', 'canceled', '2026-05-13 13:02:01.765820', 3, 5, ''),
(7, '2026-05-13 11:55:00.000000', '2026-05-13 17:55:00.000000', 'canceled', '2026-05-13 13:02:01.765820', 5, 2, '123'),
(8, '2026-05-13 13:25:00.000000', '2026-05-13 19:25:00.000000', 'created', '2026-05-13 13:20:38.481830', 3, 2, ''),
(9, '2026-05-14 07:50:00.000000', '2026-05-14 08:50:00.000000', 'confirmed', '2026-05-14 07:45:18.968831', 1, 2, '');

-- --------------------------------------------------------

--
-- Структура таблицы `cars_bookingmessage`
--

CREATE TABLE `cars_bookingmessage` (
  `id` bigint(20) NOT NULL,
  `text` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `author_id` int(11) NOT NULL,
  `booking_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `cars_bookingmessage`
--

INSERT INTO `cars_bookingmessage` (`id`, `text`, `created_at`, `author_id`, `booking_id`) VALUES
(1, '123', '2026-05-13 13:02:01.773116', 2, 5),
(2, 'ку', '2026-05-13 13:02:01.773116', 5, 5),
(3, '123', '2026-05-13 13:02:01.773116', 2, 5),
(4, 'аыва', '2026-05-13 13:02:01.773116', 5, 5),
(5, 'привет', '2026-05-13 13:24:05.670287', 2, 8),
(6, 'здаров', '2026-05-13 13:24:27.628822', 5, 8),
(7, 'как дела', '2026-05-13 13:24:34.444548', 2, 8),
(8, 'норм', '2026-05-13 13:24:42.296028', 5, 8),
(9, 'Добрый день! Где находится автомобиль?', '2026-06-22 20:56:52.907067', 2, 9),
(10, 'Здравствуйте, автомобиль находится на улице Республики 49, парковка в ТЦ \"Апельсин\"', '2026-06-22 20:58:21.734108', 5, 9);

-- --------------------------------------------------------

--
-- Структура таблицы `cars_bookingstatushistory`
--

CREATE TABLE `cars_bookingstatushistory` (
  `id` bigint(20) NOT NULL,
  `from_status` varchar(20) NOT NULL,
  `to_status` varchar(20) NOT NULL,
  `comment` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `booking_id` bigint(20) NOT NULL,
  `changed_by_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `cars_bookingstatushistory`
--

INSERT INTO `cars_bookingstatushistory` (`id`, `from_status`, `to_status`, `comment`, `created_at`, `booking_id`, `changed_by_id`) VALUES
(1, 'created', 'confirmed', 'Подтверждено менеджером', '2026-06-22 20:58:40.414037', 9, 5);

-- --------------------------------------------------------

--
-- Структура таблицы `cars_car`
--

CREATE TABLE `cars_car` (
  `id` bigint(20) NOT NULL,
  `model_name` varchar(120) NOT NULL,
  `car_class` varchar(20) NOT NULL,
  `year` int(10) UNSIGNED NOT NULL CHECK (`year` >= 0),
  `transmission` varchar(20) NOT NULL,
  `seats` smallint(5) UNSIGNED NOT NULL CHECK (`seats` >= 0),
  `price_per_hour` decimal(10,2) NOT NULL,
  `description` longtext NOT NULL,
  `image_url` varchar(200) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `image_file` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `cars_car`
--

INSERT INTO `cars_car` (`id`, `model_name`, `car_class`, `year`, `transmission`, `seats`, `price_per_hour`, `description`, `image_url`, `is_active`, `created_at`, `image_file`) VALUES
(1, 'Porsche Macan', 'business', 2024, 'automatic', 5, 2800.00, 'Премиальный SUV для деловых и вечерних поездок.', '', 1, '2026-01-01 10:00:00.000000', 'cars/porsche-macan.webp'),
(2, 'BMW X3', 'suv', 2023, 'automatic', 5, 2400.00, 'Баланс динамики и комфорта для города и трассы.', '', 1, '2026-01-01 10:00:00.000000', 'cars/bmw-x3.webp'),
(3, 'Mercedes-Benz E-Class', 'business', 2023, 'automatic', 5, 2600.00, 'Тихий и статусный седан для встреч и аэропорта.', '', 1, '2026-01-01 10:00:00.000000', 'cars/mercedes-benz-e-class.webp'),
(4, 'Audi A6', 'comfort', 2022, 'automatic', 5, 1900.00, 'Уверенная динамика и продуманная эргономика.', '', 1, '2026-01-01 10:00:00.000000', 'cars/audi-a6.webp'),
(5, 'Toyota Camry', 'comfort', 2022, 'automatic', 5, 1300.00, 'Комфортный городской вариант на каждый день.', '', 1, '2026-01-01 10:00:00.000000', 'cars/toyota-camry.webp'),
(6, 'Volkswagen Polo', 'economy', 2021, 'automatic', 5, 800.00, 'Экономичный вариант для коротких городских маршрутов.', '', 1, '2026-01-01 10:00:00.000000', 'cars/volkswagen-polo.webp');

-- --------------------------------------------------------

--
-- Структура таблицы `django_admin_log`
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(8, 'cars', 'booking'),
(9, 'cars', 'bookingmessage'),
(10, 'cars', 'bookingstatushistory'),
(7, 'cars', 'car'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Структура таблицы `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-05-13 13:01:44.868297'),
(2, 'auth', '0001_initial', '2026-05-13 13:01:45.180914'),
(3, 'admin', '0001_initial', '2026-05-13 13:01:45.245570'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-05-13 13:01:45.253383'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-05-13 13:01:45.263183'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-05-13 13:01:45.304280'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-05-13 13:01:45.340225'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-05-13 13:01:45.349078'),
(9, 'auth', '0004_alter_user_username_opts', '2026-05-13 13:01:45.352139'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-05-13 13:01:45.381054'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-05-13 13:01:45.382052'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-05-13 13:01:45.385097'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-05-13 13:01:45.395158'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-05-13 13:01:45.403808'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-05-13 13:01:45.414323'),
(16, 'auth', '0011_update_proxy_permissions', '2026-05-13 13:01:45.414323'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-05-13 13:01:45.428144'),
(18, 'cars', '0001_initial', '2026-05-13 13:01:45.514202'),
(19, 'cars', '0002_car_image_file', '2026-05-13 13:01:45.518351'),
(20, 'cars', '0003_booking_manager_comment', '2026-05-13 13:01:45.529866'),
(21, 'cars', '0004_bookingmessage', '2026-05-13 13:01:45.596997'),
(22, 'cars', '0005_bookingstatushistory', '2026-05-13 13:01:45.671893'),
(23, 'sessions', '0001_initial', '2026-05-13 13:01:45.694742');

-- --------------------------------------------------------

--
-- Структура таблицы `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('3r938hk8stlhfkzdlnkp0p8v36vcj3jl', '.eJxVjEEOwiAQRe_C2hBhpmVw6b5nIANDpWpoUtqV8e7apAvd_vfef6nA21rC1vISJlEXBer0u0VOj1x3IHeut1mnua7LFPWu6IM2PcySn9fD_Tso3Mq3RrBoM9jElNF4Fucd9NYBeRTsmOw5JxcNEPXcjSY5Io4-jRAFDLJ6fwC9LDdO:1wNQmj:UlKtPIvxO5Lhge1zEQIy2cPcPguCUDN4zuFSCQzpclY', '2026-05-28 07:47:09.837704'),
('amelkcbmadw56p7aeq0yjpljfjinc8z5', '.eJxVjEEOwiAQRe_C2hAQBqhL9z0DmYFBqoYmpV0Z765NutDtf-_9l4i4rTVunZc4ZXERIE6_G2F6cNtBvmO7zTLNbV0mkrsiD9rlOGd-Xg_376Bir99aDV4rrQLabMgG1JDtoIMCkx0467y1mqFAYnKBi2HyjMWUYijpM6B4fwC3Ujei:1wbjEr:WHM0rlHRzPgoFgNlKvsRHPJNB0pgRbrSHdCn_j6la-s', '2026-07-06 18:19:17.223577'),
('bwjami0w41cpyy3gndwbxq8q0yyixvbf', '.eJxVjMsOwiAQRf-FtSHl0YG6dO83EIYZpGogKe3K-O_apAvd3nPOfYkQt7WErfMSZhJnYcTpd8OYHlx3QPdYb02mVtdlRrkr8qBdXhvx83K4fwcl9vKt2WRNnmFgo0eLOTtn8qQ5DThltJAJga1TySnwEZxRQCqpMRmyyoEX7w_4Yjfk:1wN74z:UCh6MV_f1ydgArtFhSFY1EztXMg2mwUWpKW-lYAs6hE', '2026-05-27 10:44:41.463173'),
('cqlwho1kynelgkmln4kqzjuys2550w0n', '.eJxVjMEOwiAQBf-FsyFQWFg8evcbCLAgVQNJaU_Gf9cmPej1zcx7MR-2tfpt5MXPxM4M2Ol3iyE9ctsB3UO7dZ56W5c58l3hBx382ik_L4f7d1DDqN86J1GMjWizwslIpOIMSqcBAoGakosuSwKhsCS0YKPQVibQWhlLJCV7fwDSrDcD:1wN9ZW:J31-QNsGo3Ld7WPG2WNYr7EWryH_jNVmRHoMyTlFJLI', '2026-05-27 13:24:22.633289'),
('d7qsg6pszawa1dcs4zpt2kvcztxsl44t', '.eJxVjDsOwjAQBe_iGln-fyjpOYO19m5wANlSnFSIu0OkFNC-mXkvlmBba9oGLWlGdmaKnX63DOVBbQd4h3brvPS2LnPmu8IPOvi1Iz0vh_t3UGHUby2VDsYZMjZkKSMWiwoogI04FR2EKUILclaLqIWXxRA4mgJC1Oi98uz9AcZaN0c:1wN7vR:lMKv3NBxEq1IVRFaiKhrvh4R39rCP2xYnmK-fuoVAiY', '2026-05-27 11:38:53.349331');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Индексы таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Индексы таблицы `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Индексы таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Индексы таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Индексы таблицы `cars_booking`
--
ALTER TABLE `cars_booking`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cars_booking_car_id_01baf191_fk_cars_car_id` (`car_id`),
  ADD KEY `cars_booking_user_id_cc451371_fk_auth_user_id` (`user_id`);

--
-- Индексы таблицы `cars_bookingmessage`
--
ALTER TABLE `cars_bookingmessage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cars_bookingmessage_author_id_bc1f5be5_fk_auth_user_id` (`author_id`),
  ADD KEY `cars_bookingmessage_booking_id_583d88e8_fk_cars_booking_id` (`booking_id`);

--
-- Индексы таблицы `cars_bookingstatushistory`
--
ALTER TABLE `cars_bookingstatushistory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cars_bookingstatushistory_booking_id_f97eec17_fk_cars_booking_id` (`booking_id`),
  ADD KEY `cars_bookingstatushistory_changed_by_id_8c861854_fk_auth_user_id` (`changed_by_id`);

--
-- Индексы таблицы `cars_car`
--
ALTER TABLE `cars_car`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Индексы таблицы `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Индексы таблицы `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT для таблицы `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `cars_booking`
--
ALTER TABLE `cars_booking`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `cars_bookingmessage`
--
ALTER TABLE `cars_bookingmessage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `cars_bookingstatushistory`
--
ALTER TABLE `cars_bookingstatushistory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `cars_car`
--
ALTER TABLE `cars_car`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `cars_booking`
--
ALTER TABLE `cars_booking`
  ADD CONSTRAINT `cars_booking_car_id_01baf191_fk_cars_car_id` FOREIGN KEY (`car_id`) REFERENCES `cars_car` (`id`),
  ADD CONSTRAINT `cars_booking_user_id_cc451371_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `cars_bookingmessage`
--
ALTER TABLE `cars_bookingmessage`
  ADD CONSTRAINT `cars_bookingmessage_author_id_bc1f5be5_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `cars_bookingmessage_booking_id_583d88e8_fk_cars_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `cars_booking` (`id`);

--
-- Ограничения внешнего ключа таблицы `cars_bookingstatushistory`
--
ALTER TABLE `cars_bookingstatushistory`
  ADD CONSTRAINT `cars_bookingstatushistory_booking_id_f97eec17_fk_cars_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `cars_booking` (`id`),
  ADD CONSTRAINT `cars_bookingstatushistory_changed_by_id_8c861854_fk_auth_user_id` FOREIGN KEY (`changed_by_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
