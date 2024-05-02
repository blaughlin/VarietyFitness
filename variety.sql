SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

--
-- Table structure for table `Members`
--

DROP TABLE IF EXISTS `Members`;

CREATE TABLE `Members`
(
    `memberID` int(11) NOT NULL AUTO_INCREMENT,
    `firstName` varchar(50) NOT NULL,
    `lastName` varchar(50) NOT NULL,
    `email` varchar(50) NOT NULL,
    `phone` varchar(10) NOT NULL,
    `membershipStartDate` DATE NOT NULL,
    `monthlyDues` decimal(5,2) NOT NULL,
    `creditCardNumber` bigint NOT NULL,
    `expirationMonth` int(2) NOT NULL,
    `expirationYear` int(4) NOT NULL,
    `paymentCurrent` BOOLEAN,
    PRIMARY KEY(`memberID`) 
);

--
-- Inserting data for table `Members`
--

INSERT INTO `Members` 
(
    `firstName`,
    `lastName`,
    `email`,
    `phone` ,
    `membershipStartDate`,
    `monthlyDues`,
    `creditCardNumber`,
    `expirationMonth`,
    `expirationYear`,
    `paymentCurrent`
)
VALUES 
('John', 'Doe', 'jon@gmail.com', 5551234567, '20240501', 70.00, 1234567891234567, 11, 2029, 1),
('Sarah', 'Mills', 'sarah@gmail.com', 5551234455, '20230501', 65.00, 1234567891234562, 8, 2030, 1),
('Ben', 'Smith', 'ben@gmail.com', 5551233214, '20220811', 63.00, 1234567891234561, 2, 2025, 1);

-- --
-- -- Table structure for table `Invoices`
-- --

DROP TABLE IF EXISTS `Invoices`;

CREATE TABLE `Invoices`
(
    `invoiceID` int(11) NOT NULL AUTO_INCREMENT,
    `memberID` int(11) NOT NULL,
    `date` DATE NOT NULL,
    `amountDue` decimal(5,2) NOT NULL,
    PRIMARY KEY(`invoiceID`),
    FOREIGN KEY (`memberID`) REFERENCES Members(`memberID`) ON DELETE CASCADE

);

-- --
-- --  Inserting data for table `Invoices`
-- --
INSERT INTO `Invoices` 
(
    `memberID`,
    `date`,
    `amountDue`
)
VALUES 
((SELECT `memberID` FROM `Members` WHERE `firstName` = 'John' AND `lastName` = 'Doe'),
 '20240501',
 (SELECT `monthlyDues` FROM `Members` WHERE `firstName` = 'John' AND `lastName` = 'Doe') ),
((SELECT `memberID` FROM `Members` WHERE `firstName` = 'Sarah' AND `lastName` = 'Mills'),
 '20240501',
 (SELECT `monthlyDues` FROM `Members` WHERE `firstName` = 'Sarah' AND `lastName` = 'Mills') ),
 ((SELECT `memberID` FROM `Members` WHERE `firstName` = 'Ben' AND `lastName` = 'Smith'),
 '20240501',
 (SELECT `monthlyDues` FROM `Members` WHERE `firstName` = 'Ben' AND `lastName` = 'Smith') );

-- --
-- -- Table structure for table `Visits`
-- --

DROP TABLE IF EXISTS `Visits`;

CREATE TABLE `Visits`
(
    `visitID` int(11) NOT NULL AUTO_INCREMENT,
    `memberID` int(11) NOT NULL,
    `date` date NOT NULL,
    PRIMARY KEY(`visitID`),
    FOREIGN KEY(`memberID`) references Members(`memberID`) ON DELETE CASCADE
);


-- --
-- -- Inserting data for table `Visits`
-- --
INSERT INTO `Visits` 
(
    `memberID`,
    `date`
)
VALUES 
((SELECT `memberID` FROM `Members` WHERE `firstName` = 'John' AND `lastName` = 'Doe'),
 '20240501'),
((SELECT `memberID` FROM `Members` WHERE `firstName` = 'Sarah' AND `lastName` = 'Mills'),
 '20240501'),
((SELECT `memberID` FROM `Members` WHERE `firstName` = 'Sarah' AND `lastName` = 'Mills'),
 '20240502'),
((SELECT `memberID` FROM `Members` WHERE `firstName` = 'John' AND `lastName` = 'Doe'),
 '20240503');


-- --
-- -- Table structure for table `Employees`
-- --

DROP TABLE IF EXISTS `Employees`;

CREATE TABLE `Employees`
(
    `employeeID` int(11) NOT NULL AUTO_INCREMENT,
    `firstName` varchar(50) NOT NULL,
    `lastName` varchar(50) NOT NULL,
    `hireDate` date NOT NULL,
    `hourlyRate` decimal(4,2) NOT NULL,
    `jobTitle` varchar(50) NOT NULL,
    PRIMARY KEY(`employeeID`)
);

-- --
-- -- Inserting data for table `Employees`
-- --

INSERT INTO `Employees` 
(
    `firstName`,
    `lastName`,
    `hireDate`,
    `hourlyRate`,
    `jobTitle`
)
VALUES 
('Steve', 'Smith', '20230101', 23.56, "Personal Trainer"),
('Julie', 'Moore', '20220101', 22.56, "Receptionist"),
('Paul', 'Green', '20210222', 24.56, "Fitness Instructor"),
('Mary', 'Star', '20221103', 28.00, "Fitness Instructor");


-- --
-- -- Table structure for table `Classes`
-- --
DROP TABLE IF EXISTS `Classes`;

CREATE TABLE `Classes`
(
    `classID` int(11) NOT NULL AUTO_INCREMENT,
    `employeeID` int(11) NOT NULL,
    `classDescription` varchar(500) NOT NULL,
    `classDate` DATE NOT NULL,
    `startTime` TIME NOT NULL,
    `endTime` TIME NOT NULL,
    `roomNumber` int NOT NULL,
    PRIMARY KEY(`classID`),
    FOREIGN KEY(`employeeID`) references Employees(`employeeID`) ON DELETE CASCADE
);

-- --
-- -- Inserting data for table `Classes`
-- --
INSERT INTO `Classes` 
(
    `employeeID`,
    `classDescription`,
    `classDate`,
    `startTime`,
    `endTime`,
    `roomNumber`
)
VALUES 
((SELECT `employeeID` FROM `Employees` WHERE `firstName` = 'Paul' AND `lastName` = 'Green'),
'Zumba', '20240501', '11:00:00', '11:50:00', 1),
((SELECT `employeeID` FROM `Employees` WHERE `firstName` = 'Paul' AND `lastName` = 'Green'),
'Zumba', '20240505', '11:00:00', '11:50:00', 1),
((SELECT `employeeID` FROM `Employees` WHERE `firstName` = 'Mary' AND `lastName` = 'Star'),
'Yoga Flow', '20240501', '10:00:00', '10:50:00', 2);

-- --
-- -- Table structure for table `Classes_Members`
-- --
DROP TABLE IF EXISTS `Classes_Members`;

CREATE TABLE `Classes_Members`
(
    `classMemberID` int(11) NOT NULL AUTO_INCREMENT,
    `memberID` int(11),
    `classID` int(11),
    PRIMARY KEY(`classMemberID`),
    FOREIGN KEY(`memberID`) references Members(`memberID`) ON DELETE SET NULL,
    FOREIGN KEY(`classID`) references Classes(`classID`) ON DELETE CASCADE
);

-- --
-- -- Inserting data for table `Classes_Members`
-- --
INSERT INTO `Classes_Members`
(
    `memberID`,
    `classID`
) 
VALUES
((SELECT `memberID` FROM `Members` WHERE `firstName` = 'John' AND `lastName` = 'Doe'),
(SELECT `classID` FROM `Classes` WHERE `classDate` = '20240501' AND  `startTime` = '11:00:00' AND `roomNumber`= 1 )),

((SELECT `memberID` FROM `Members` WHERE `firstName` = 'Ben' AND `lastName` = 'Smith'),
(SELECT `classID` FROM `Classes` WHERE `classDate` = '20240501' AND  `startTime` = '11:00:00' AND `roomNumber` = 1 )),

((SELECT `memberID` FROM `Members` WHERE `firstName` = 'John' AND `lastName` = 'Doe'),
(SELECT `classID` FROM `Classes` WHERE `classDate` = '20240501' AND  `startTime` = '10:00:00' AND `roomNumber` = 2 ));

SET FOREIGN_KEY_CHECKS=1;
COMMIT;