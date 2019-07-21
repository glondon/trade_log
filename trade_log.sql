-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jul 22, 2019 at 01:01 AM
-- Server version: 10.1.19-MariaDB
-- PHP Version: 5.6.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `trade_log`
--

-- --------------------------------------------------------

--
-- Table structure for table `actions`
--

CREATE TABLE `actions` (
  `id` int(11) NOT NULL,
  `viewed_rules` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `id` int(11) NOT NULL,
  `item` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `trades`
--

CREATE TABLE `trades` (
  `id` int(11) NOT NULL,
  `symbol` varchar(8) NOT NULL,
  `entry` decimal(10,4) NOT NULL,
  `exit` decimal(10,4) NOT NULL DEFAULT '0.0000',
  `position` enum('long','short') NOT NULL,
  `stop` decimal(10,4) NOT NULL DEFAULT '0.0000',
  `target` decimal(10,4) NOT NULL DEFAULT '0.0000',
  `entry_date` date NOT NULL,
  `exit_date` date NOT NULL DEFAULT '0000-00-00',
  `size` varchar(25) DEFAULT NULL,
  `account` enum('tos','ibg','ibc') NOT NULL,
  `entry_comm` decimal(10,2) NOT NULL DEFAULT '0.00',
  `exit_comm` decimal(10,2) NOT NULL DEFAULT '0.00',
  `result` decimal(10,2) NOT NULL DEFAULT '0.00',
  `early_exit` tinyint(1) NOT NULL DEFAULT '0',
  `trade_reasons` varchar(255) DEFAULT NULL,
  `notes` varchar(500) DEFAULT NULL,
  `status` enum('open','closed') NOT NULL DEFAULT 'open',
  `exp_date` date NOT NULL DEFAULT '0000-00-00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `trade_ideas`
--

CREATE TABLE `trade_ideas` (
  `id` int(11) NOT NULL,
  `ticker` varchar(8) NOT NULL,
  `notes` varchar(255) NOT NULL,
  `idea_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `trade_lessons`
--

CREATE TABLE `trade_lessons` (
  `id` int(11) NOT NULL,
  `lesson` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `trade_plan`
--

CREATE TABLE `trade_plan` (
  `id` int(11) NOT NULL,
  `plan` text NOT NULL,
  `plan_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `trade_rules`
--

CREATE TABLE `trade_rules` (
  `id` int(11) NOT NULL,
  `rule` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `watchlist`
--

CREATE TABLE `watchlist` (
  `id` int(11) NOT NULL,
  `ticker` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `actions`
--
ALTER TABLE `actions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trades`
--
ALTER TABLE `trades`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trade_ideas`
--
ALTER TABLE `trade_ideas`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trade_lessons`
--
ALTER TABLE `trade_lessons`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trade_plan`
--
ALTER TABLE `trade_plan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trade_rules`
--
ALTER TABLE `trade_rules`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ticker` (`ticker`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `actions`
--
ALTER TABLE `actions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;
--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT for table `trades`
--
ALTER TABLE `trades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1148;
--
-- AUTO_INCREMENT for table `trade_ideas`
--
ALTER TABLE `trade_ideas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `trade_lessons`
--
ALTER TABLE `trade_lessons`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;
--
-- AUTO_INCREMENT for table `trade_plan`
--
ALTER TABLE `trade_plan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `trade_rules`
--
ALTER TABLE `trade_rules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=105;
--
-- AUTO_INCREMENT for table `watchlist`
--
ALTER TABLE `watchlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
