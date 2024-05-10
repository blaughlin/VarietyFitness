-- Query to select Members ---
SELECT *
FROM Members;
 
-- Query to select Classes --
SELECT *
FROM Classes;

-- Query to select Invoices --
SELECT *
FROM Invoices;

-- Query to select Employees --
SELECT *
FROM Employees;

-- Query to select MemberVisits --
SELECT *
FROM MemberVisits;

-- Query to select Class_Members --
SELECT *
FROM Class_Members;

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

-- Query to add to Class_Members --
INSERT INTO Classes_Members(memberID, classID)
VALUES(:memberID_from_dropdown_input, :classID_from_dropdown_input,);

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


-- get all Member IDs and Names to populate the Member dropdown
SELECT memberID, firstName, lastName FROM Members;

-- get all Employee IDs and Names to populate the Employee dropdown
SELECT employeeID, firstName, lastName FROM Employees;

-- get all class IDs, description, date, and start time to populate the class dropdown
SELECT classID, classDescription, classDate, startTime FROM Classes;