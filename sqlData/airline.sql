-- phpMyAdmin SQL Dump
-- version 4.8.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 05, 2018 at 04:27 AM
-- Server version: 10.1.31-MariaDB
-- PHP Version: 7.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airline`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `airline_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('China Eastern'),
('Delta'),
('Spirit');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

CREATE TABLE `airline_staff` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `airline_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline_name`) VALUES
('dinghaha@nyu.edu', '5ca5108e182122488415608048267557', 'Zhengyuan', 'Ding', '1990-12-31', 'Delta'),
('yz2113@nyu.edu', 'c48680bd1f8ac559802e25a963bd3fbc', 'Sharon', 'Zhang', '1996-01-27', 'China Eastern'),
('zd415@nyu.edu', '5ca5108e182122488415608048267557', 'Carol', 'Ding', '1995-09-09', 'Spirit');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `airline_name` varchar(50) NOT NULL,
  `airplane_id` int(11) NOT NULL,
  `seats` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_id`, `seats`) VALUES
('China Eastern', 198, 10),
('Delta', 222, 20),
('Delta', 339, 50),
('Delta', 666, 5),
('Spirit', 440, 3);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `airport_name` varchar(50) NOT NULL,
  `airport_city` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_name`, `airport_city`) VALUES
('BCIA', 'Beijing'),
('JFK', 'NYC'),
('ORD', 'Chicago'),
('PVG', 'Shanghai');

-- --------------------------------------------------------

--
-- Table structure for table `booking_agent`
--

CREATE TABLE `booking_agent` (
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `booking_agent_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `booking_agent`
--

INSERT INTO `booking_agent` (`email`, `password`, `booking_agent_id`) VALUES
('chunqiu@gmail.com', '2c3980303aaecf9a8fb6c1679cb1dd74', 12345),
('cmu@gmail.com', '9132d3085c324b19c082f6b5c7f07a08', 9960),
('cu@gmail.com', '7adbce45955e6019c920abb1059f451a', 8222),
('dongfang@gmail.com', 'd5572a057b2038b8783f9b93214e96f9', 1350),
('gatech@gmail.com', '04df808d3d8bda154e9b27f238e2b916', 29),
('nw@gmail.com', 'ef11389eca69fd28de4057f6ff5d55ef', 33608),
('nyu@gmail.com', '687f3afe1be9338f278363ea8a62f488', 19);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `building_number` varchar(30) NOT NULL,
  `street` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `state` varchar(30) NOT NULL,
  `phone_number` int(11) NOT NULL,
  `passport_number` varchar(30) NOT NULL,
  `passport_expiration` date NOT NULL,
  `passport_country` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('fanny@nyu.edu', 'Fanny', '54f63ec45458661b963d1dd2a52925e8', '14B', 'Lafayette Street', 'New York', 'NY', 917496, 'EABC400', '2023-01-23', 'U.S.', '1993-01-07'),
('jane@nyu.edu', 'Jane', 'bde56bd67225e2a3e190dc834d969a6b', '3b', 'Caoyang Road', 'Beijing', 'Beijing', 99637, 'Q19967', '2022-02-02', 'China', '1990-09-08'),
('nancy@nyu.edu', 'Nancy', 'c71b649b6347f09782c3406c9592b776', '20', 'Yangzi Road', 'Shanghai', 'Shanghai', 1234509, 'C198', '2030-01-20', ' China', '1988-12-30'),
('sallyzhang@gmail.com', 'Sally', '9e65c8f79ace26f75ea119695b2d1449', '2', 'Century Avenue', 'Shanghai', 'Shanghai', 1387402, 'E139704', '2020-12-17', 'China', '1996-06-08');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `airline_name` varchar(50) NOT NULL,
  `flight_num` int(11) NOT NULL,
  `departure_airport` varchar(50) NOT NULL,
  `departure_time` datetime NOT NULL,
  `arrival_airport` varchar(50) NOT NULL,
  `arrival_time` datetime NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `status` varchar(50) NOT NULL,
  `airplane_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES
('China Eastern', 9098, 'JFK', '2018-05-20 11:45:00', 'PVG', '2018-05-21 12:00:00', '5000', 'upcoming', 198),
('Delta', 188, 'ORD', '2017-03-02 12:00:00', 'JFK', '2017-03-02 15:30:00', '3200', 'in progress', 222),
('Delta', 320, 'ORD', '2018-01-01 03:40:04', 'PVG', '2018-01-02 09:00:00', '4500', 'in progress', 339),
('Delta', 380, 'BCIA', '2018-03-10 03:00:00', 'ORD', '2018-03-10 19:00:00', '8000', 'in progress', 666),
('Delta', 999, 'BCIA', '2018-03-29 04:00:00', 'PVG', '2018-03-29 06:00:00', '2000', 'in progress', 339),
('Spirit', 119, 'PVG', '2018-05-05 19:40:00', 'JFK', '2018-05-05 03:25:00', '1800', 'upcoming', 440);

-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

CREATE TABLE `purchases` (
  `ticket_id` int(11) NOT NULL,
  `customer_email` varchar(50) NOT NULL,
  `booking_agent_id` int(11) DEFAULT NULL,
  `purchase_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES
(1, 'jane@nyu.edu', NULL, '2017-12-30'),
(2, 'fanny@nyu.edu', 1350, '2017-04-29'),
(3, 'sallyzhang@gmail.com', 19, '2017-11-19'),
(502, 'fanny@nyu.edu', 9960, '2018-01-01'),
(22222, 'fanny@nyu.edu', 1350, '2018-04-30'),
(111111, 'sallyzhang@gmail.com', NULL, '2018-03-07'),
(111112, 'sallyzhang@gmail.com', 12345, '2018-03-09'),
(222223, 'jane@nyu.edu', 1350, '2018-04-20'),
(300001, 'fanny@nyu.edu', 8222, '2018-02-20'),
(300001, 'sallyzhang@gmail.com', 33608, '2018-03-01'),
(300002, 'jane@nyu.edu', 8222, '2018-02-10'),
(400003, 'nancy@nyu.edu', 29, '2018-02-10');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticket_id` int(11) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `flight_num` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES
(111111, 'China Eastern', 9098),
(111112, 'China Eastern', 9098),
(40001, 'Delta', 188),
(1, 'Delta', 320),
(2, 'Delta', 320),
(3, 'Delta', 320),
(502, 'Delta', 380),
(400003, 'Delta', 380),
(30000, 'Delta', 999),
(300001, 'Delta', 999),
(300002, 'Delta', 999),
(22222, 'Spirit', 119),
(222223, 'Spirit', 119),
(45002279, 'Spirit', 119);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- Indexes for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airline_name`,`airplane_id`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`airport_name`);

--
-- Indexes for table `booking_agent`
--
ALTER TABLE `booking_agent`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`airline_name`,`flight_num`),
  ADD KEY `airline_name` (`airline_name`,`airplane_id`),
  ADD KEY `departure_airport` (`departure_airport`),
  ADD KEY `arrival_airport` (`arrival_airport`);

--
-- Indexes for table `purchases`
--
ALTER TABLE `purchases`
  ADD PRIMARY KEY (`ticket_id`,`customer_email`),
  ADD KEY `customer_email` (`customer_email`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_id`),
  ADD KEY `airline_name` (`airline_name`,`flight_num`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline_name`,`airplane_id`) REFERENCES `airplane` (`airline_name`, `airplane_id`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`departure_airport`) REFERENCES `airport` (`airport_name`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`arrival_airport`) REFERENCES `airport` (`airport_name`);

--
-- Constraints for table `purchases`
--
ALTER TABLE `purchases`
  ADD CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`),
  ADD CONSTRAINT `purchases_ibfk_2` FOREIGN KEY (`customer_email`) REFERENCES `customer` (`email`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`airline_name`,`flight_num`) REFERENCES `flight` (`airline_name`, `flight_num`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
