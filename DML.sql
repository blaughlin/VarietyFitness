-- Query to select all Members and display name as one column ---
SELECT memberID, Concat(firstName ," ", lastName) as name, email, phone, membershipStartDate, monthlyDues, creditCardNumber, expirationMonth, expirationYear, paymentCurrent
FROM Members;

-- Query to select member by ID---
SELECT memberID, firstName, lastName, email, phone, membershipStartDate, monthlyDues, creditCardNumber, expirationMonth, expirationYear, paymentCurrent
FROM Members WHERE memberID = :memberID;

 
-- Query to select all Classes with employeeID replaced with name of employee --
SELECT Classes.classID, Concat(Employees.firstName, " ", Employees.lastName) as instructor, Classes.classDescription, Classes.classDate, Classes.startTime, Classes.endTime, Classes.roomNumber
from Classes
inner join Employees on Classes.employeeID = Employees.employeeID;

-- Query to select class by ID---
SELECT classID, employeeID, classDescription, classDate, startTime, endTime, roomNumber
FROM Classes WHERE classID = :classID;

-- Query to select all Invoices with memberID replaced with full name of member --
SELECT Invoices.invoiceID, Concat(Members.firstName, " ", Members.lastName) as member, Invoices.date, Invoices.amountDue
FROM Invoices 
INNER JOIN Members on Invoices.memberID = Members.memberID;

-- Query to select invoice by ID---
SELECT invoiceID, memberID, date, amountDue
FROM Invoices WHERE invoiceID = :invoiceID;

-- Query to select all Employees and display name as one column--
SELECT employeeID, Concat(firstName ," ", lastName) as name, hireDate, hourlyRate, jobTitle
FROM Employees;

-- Query to select employee by ID---
SELECT employeeID, firstName, lastName  hireDate, hourlyRate, jobTitle
From Employees WHERE employeeID = :employeeID;

-- Query to select all MemberVisits and replace memberID with member's full name --
SELECT MemberVisits.visitID, Concat(Members.firstName, " ", Members.lastName) as member, MemberVisits.date
FROM MemberVisits
INNER JOIN Members On MemberVisits.memberID = Members.memberID;

-- Query to select MemberVisits by ID---
SELECT visitID, memberID, date 
FROM MemberVisits WHERE visitID = :visitID;

-- Query to select all Classes_Members with memberID replaced with member's full name and classID replaced with description, date and start time--
SELECT Classes_Members.classMemberID, Concat(Members.firstName, " ", Members.lastName) as member, Concat(Classes.classDescription, " " ,Classes.classDate, " ", Classes.startTime) as class
from Classes_Members
inner join Members on Classes_Members.memberID = Members.memberID
inner join Classes on Classes_Members.classID = Classes.classID;

-- Query to select Classes_Members by ID---
SELECT classMemberID, memberID, classID
FROM Classes_Members WHERE classMemberID = :classMemberID;

-- Query to add to Members ---
INSERT INTO Members (firstName, lastName, email, phone, membershipStartDate, monthlyDues, creditCardNumber, expirationMonth, expirationYear, paymentCurrent) 
   VALUES (:firstName, :lastName, :email, :phone, :membershipStartDate, :monthlyDues, :creditCardNumber, :expirationMonth, :expirationYear, :paymentCurrent_from_dropdown_Input);

-- Query to add to Classes --
INSERT INTO Classes (employeeID, classDescription, classDate, startTime, endTime, roomNumber)
    VALUES(:employeeID_from_dropdown_Input, :classDescription, :classDate, :startTime, :endTime, :roomNumber);

-- Query to add to Invoices --
INSERT INTO Invoices(memberID, date, amountDue)
    VALUES(:memberID_from_dropdown_input, :date, :amountDue);

-- Query to add to Employees --
INSERT INTO Employees(firstName, lastName, hireDate, hourlyRate, jobTitle)
    VALUES(:firstName, :lastName, :hireDate, :hourlyRate, :jobTitle);

-- Query to add to MemberVisits --
INSERT INTO MemberVisits(memberID, date)
    VALUES(:memberID_from_dropdown_input, :date)

-- Query to add to Classes_Members --
INSERT INTO Classes_Members(memberID, classID)
VALUES(:memberID_from_dropdown_input, :classID_from_dropdown_input,);

-- Query to delete  Classes_Members  --
DELETE FROM Classes_Members WHERE classMemberID = :classMemberID_selected_from_browse_classes_page;

-- Query to delete Classes --
DELETE FROM Classes WHERE id = :classID_selected_from_browse_classes_page;

-- Query to update Classes ---
SELECT classID, employeeID, classDescription, startTime, endTime, roomNumber 
   FROM Classes 
   WHERE classID = :classID_selected_from_browse_classes_page

UPDATE Classes 
   SET employeeID = :employeeID_from_dropdown_Input, classDescription= :classDescription, 
       startTime = :startTime, endTime= :endTime roomNumber = :roomNumber
   WHERE id= :classID_from_the_update_form;

-- Query to update Classes_Members ---
SELECT classMemberID, memberID, classID
    FROM Classes_Members
    WHERE classMemberID = :classMemberID_selected_from_browse_classes_page

UPDATE Classes_Members
    SET memberID = :memberID_from_dropdown_input, classID = :classID_from_dropdown_input
WHERE classMemberID = : classMemberID_selected_from_browse_classes_page

-- get all Member IDs and Names to populate the Member dropdown
SELECT memberID, firstName, lastName FROM Members;

-- get all Employee IDs and Names to populate the Employee dropdown
SELECT employeeID, firstName, lastName FROM Employees;

-- get all class IDs, description, date, and start time to populate the class dropdown
SELECT classID, classDescription, classDate, startTime FROM Classes;