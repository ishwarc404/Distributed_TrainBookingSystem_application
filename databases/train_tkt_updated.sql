-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 07, 2019 at 03:21 PM
-- Server version: 10.1.35-MariaDB
-- PHP Version: 7.2.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `train_tkt`
--

-- --------------------------------------------------------

--
-- Table structure for table `passenger`
--

CREATE TABLE `passenger` (
  `Passenger_id` int(11) NOT NULL,
  `Name` text,
  `Age` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `trains`
--

CREATE TABLE `trains` (
  `Train_id` int(11) NOT NULL,
  `From_city` text NOT NULL,
  `To_city` text NOT NULL,
  `Trains` text NOT NULL,
  `Train_Time` time DEFAULT NULL,
  `No_of_available_seat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `trains`
--

INSERT INTO `trains` (`Train_id`, `From_city`, `To_city`, `Trains`, `Train_Time`, `No_of_available_seat`) VALUES
(1, 'Bangalore', 'Shimogga', 'Shatabdi ', '08:00:00', 100),
(2, 'Bangalore', 'Chennai', 'Lalbagh', '00:00:08', 100),
(3, 'Bangalore', 'Hubli', 'double decker', '00:00:10', 100),
(4, 'Hubli', 'Shimogga', 'Lalbagh', '00:00:11', 100),
(5, 'Chennai', 'Bangalore', 'Mail', '00:00:07', 100),
(6, 'Chennai', 'Shimogga', 'Chennai Express', '00:00:13', 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `passenger`
--
ALTER TABLE `passenger`
  ADD PRIMARY KEY (`Passenger_id`);

--
-- Indexes for table `trains`
--
ALTER TABLE `trains`
  ADD PRIMARY KEY (`Train_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
