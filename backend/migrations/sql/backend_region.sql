-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 02, 2019 at 09:08 AM
-- Server version: 5.7.17-0ubuntu0.16.04.2
-- PHP Version: 7.0.32-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cruises`
--

--
-- Dumping data for table `backend_region`
--

INSERT INTO `backend_region` (`id`, `name`, `description`, `url`, `slug`) VALUES
(1, 'Alaska', 'The Last Frontier, the Great Land, North to the Future, Land of the Midnight Sun… The nicknames vary, but what remains unchanged is Alaska’s status as a premier, rugged, and fascinating travel destination. The largest, least densely populated, northernmost and westernmost U.S. state Alaska is practically its own country.With thousands of miles of scenic coastline, experiencing the 49 state on an Alaskan cruise is a. The massive glaciers, misty fjords, tranquil waterways, immense mountains, thriving rainforests, and rugged tundra landscapes are home to scores of wildlife… all viewable from the comfort of your cruise ship or via exciting onshore excursions.Due to its massive size and diverse landscapes, Alaska can be broken down into several regions. The Inside Passage, also known as the Panhandle, stretches across the southeastern end of state and is the most accessible destination within Alaska. Its majestic forests, wealth of fjords and islands, and abundant wildlife add to the appeal of this region. Southern and Southwestern Alaska includes the city of Anchorage and the volcanic Aleutian Islands. Farther north, Arctic Alaska is home to impressive tundra landscapes, the aurora borealis, and the midnight sun.', '/regions/view/Alaska', 'alaska'),
(2, 'Asia', NULL, '/regions/view/Asia', 'asia'),
(3, 'Australia/New Zealand', ' ', '/regions/view/Australia%7E%7ENew+Zealand', 'australianew-zealand'),
(4, 'Bermuda', NULL, '/regions/view/Bermuda', 'bermuda'),
(5, 'Caribbean', ' ', '/regions/view/Caribbean', 'caribbean'),
(6, 'Europe', NULL, '/regions/view/Europe', 'europe'),
(7, 'Hawaii and South Pacific', ' . ', '/regions/view/Hawaii+and+South+Pacific', 'hawaii-and-south-pacific'),
(8, 'Mediterranean', ' ', '/regions/view/Mediterranean', 'mediterranean'),
(9, 'Mexico', ' .', '/regions/view/Mexico', 'mexico'),
(10, 'Panama Canal', NULL, '/regions/view/Panama+Canal', 'panama-canal'),
(11, 'River Cruises', NULL, '/regions/view/River+Cruises', 'river-cruises'),
(12, 'Trans-Ocean', NULL, '/regions/view/Trans-Ocean', 'trans-ocean'),
(13, 'Atlantic Seaboard', NULL, NULL, 'atlantic-seaboard'),
(14, 'South America', NULL, NULL, 'south-america'),
(15, 'Pacific Seaboard', NULL, NULL, 'pacific-seaboard'),
(16, 'Cruise To Nowhere', NULL, NULL, 'cruise-to-nowhere'),
(17, 'Repositioning', NULL, NULL, 'repositioning'),
(18, 'Antarctica', NULL, '/regions/view/Antarctica', 'antarctica');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
