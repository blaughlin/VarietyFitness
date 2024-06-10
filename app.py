## CS340 Spring 2024 Project: Variety Fitness
## Bernard Laughlin, Raul Preciado
## 5/23/2024
## Code based off of "https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file"

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Configuration
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_laughlbe'
app.config['MYSQL_PASSWORD'] = '0077' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_laughlbe'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Routes 
@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/members', methods = ['POST', 'GET'])
def members():
    if request.method == "GET":
        query = "SELECT memberID, CONCAT(firstName ,' ', lastName) as name, email, phone, membershipStartDate, monthlyDues, creditCardNumber, expirationMonth, expirationYear, paymentCurrent FROM Members"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("members.html", data = data)
    if request.method == "POST":
        if request.form.get("addMember"):
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            email = request.form["email"]
            phone = request.form["phone"]
            membershipStartDate = request.form["membershipStartDate"]
            monthlyDues = request.form["monthlyDues"]
            creditCardNumber = request.form["creditCardNumber"]
            expirationMonth = request.form["expirationMonth"]
            expirationYear = request.form["expirationYear"]
            current = request.form["current"]

            query = "INSERT INTO Members (firstName, lastName, email, phone, membershipStartDate, monthlyDues, creditCardNumber, expirationMonth, expirationYear, paymentCurrent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, email, phone, membershipStartDate, monthlyDues, creditCardNumber, expirationMonth, expirationYear, current))
            mysql.connection.commit()

            return redirect("/members")
        

@app.route('/edit-member/<int:id>', methods = ['POST', 'GET'])
def editMembers(id):
    if request.method == "GET":
        query = "SELECT * FROM Members WHERE memberID = %s" %(id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit-member.html", data = data)
    
    if request.method == "POST":
        if request.form.get("editMember"):
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            email = request.form["email"]
            phone = request.form["phone"]
            membershipStartDate = request.form["membershipStartDate"]
            monthlyDues = request.form["monthlyDues"]
            creditCardNumber = request.form["creditCardNumber"]
            expirationMonth = request.form["expirationMonth"]
            expirationYear = request.form["expirationYear"]
            paymentCurrent = request.form["current"]

            attributes = [firstName, lastName, email, phone, membershipStartDate, monthlyDues, creditCardNumber,\
                          expirationMonth, expirationYear, paymentCurrent]
            
            for value in attributes:
                if value == "":
                    return redirect("/error")

            query = "UPDATE Members set firstName = %s, lastName = %s, email = %s, phone = %s, membershipStartDate = %s, monthlyDues = %s, creditCardNumber = %s, expirationMonth = %s, expirationYear = %s, paymentCurrent = %s WHERE memberID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, email, phone, membershipStartDate, monthlyDues, creditCardNumber, expirationMonth, expirationYear, paymentCurrent, id))
            mysql.connection.commit()
            return redirect("/members")
        
@app.route('/delete-member/<int:id>', methods = ['POST', 'GET'])       
def deleteMember(id):
    if request.method == "GET":
        query = "Select * FROM Members WHERE memberID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template('/delete-member.html', data = data)

    elif request.method == "POST":
        query = "DELETE FROM Members WHERE memberID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        return redirect("/members")


@app.route('/classes', methods = ['POST', 'GET'])
def classes():
    if request.method == "GET":
        query = "SELECT Classes.classID, Concat(Employees.firstName, ' ', Employees.lastName) as instructor, Classes.classDescription, Classes.classDate, Classes.startTime, Classes.endTime, Classes.roomNumber FROM Classes left join Employees on Classes.employeeID = Employees.employeeID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        query = "SELECT employeeID, Concat(firstName, ' ', lastName) as instructor FROM Employees"
        cur = mysql.connection.cursor()
        cur.execute(query)
        instructors = cur.fetchall()
        return render_template("classes.html", data = data, instructors = instructors)
    if request.method == "POST":
        if request.form.get("addClass"):
            employeeID = request.form["employeeID"]
            classDescription = request.form["classDescription"]
            classDate = request.form["classDate"]
            startTime = request.form["startTime"]
            endTime = request.form["endTime"]
            roomNumber = request.form["roomNumber"]
            if employeeID == "":
                query = "INSERT INTO Classes (employeeID, classDescription, classDate, startTime, endTime, roomNumber) VALUES (NULL, %s, %s, %s, %s, %s)" 
                cur = mysql.connection.cursor()
                cur.execute(query, (classDescription, classDate, startTime, endTime, roomNumber))
                mysql.connection.commit()
                return redirect("/classes")
            else:
                query = "INSERT INTO Classes (employeeID, classDescription, classDate, startTime, endTime, roomNumber) VALUES (%s, %s, %s, %s, %s, %s)" 
                cur = mysql.connection.cursor()
                cur.execute(query, (employeeID, classDescription, classDate, startTime, endTime, roomNumber))
                mysql.connection.commit()
                return redirect("/classes")

@app.route('/delete_class/<int:id>', methods = ['POST', 'GET'])
def deleteClass(id):
    if request.method == "GET":
        query = "SELECT Classes.classID, Concat(Employees.firstName, ' ', Employees.lastName) as instructor, Classes.classDescription, Classes.classDate, Classes.startTime, Classes.endTime, Classes.roomNumber FROM Classes left join Employees on Classes.employeeID = Employees.employeeID WHERE classID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template('/delete_class.html', data = data)
    elif request.method == "POST":
        query = "DELETE FROM Classes WHERE classID = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()
        return redirect("/classes")

@app.route('/edit_class/<int:id>', methods = ['POST', 'GET'])
def editClasses(id):
    if request.method == "GET":
        query = "SELECT Classes.classID, Concat(Employees.firstName, ' ', Employees.lastName) as instructor, Classes.classDescription, Classes.classDate, Classes.startTime, Classes.endTime, Classes.roomNumber FROM Classes left join Employees on Classes.employeeID = Employees.employeeID WHERE classID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        query = "SELECT employeeID, Concat(firstName, ' ', lastName) as instructor FROM Employees"
        cur = mysql.connection.cursor()
        cur.execute(query)
        instructors = cur.fetchall()
        print(instructors)
        print(data)
        return render_template("edit_class.html", data = data, instructors = instructors)
    if request.method == "POST":
        if request.form.get("editClass"):
            instructor = request.form['employeeID']
            classDescription = request.form['classDescription']
            classDate = request.form['classDate']
            startTime = request.form['startTime']
            endTime = request.form['endTime']
            roomNumber = request.form['roomNumber']
        if instructor == "":
            # account for NULL instructor
            query = "UPDATE Classes SET employeeID = NULL, classDescription = %s, classDate = %s, startTime = %s, endTime = %s, roomNumber = %s WHERE classID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (classDescription, classDate, startTime, endTime, roomNumber, id))
            mysql.connection.commit()
            return redirect("/classes")
        else: 
            # account for instructor
            query = "UPDATE Classes SET employeeID = %s, classDescription = %s, classDate = %s, startTime = %s, endTime = %s, roomNumber = %s WHERE classID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (instructor, classDescription, classDate, startTime, endTime, roomNumber, id))
            mysql.connection.commit()
            return redirect("/classes")


@app.route('/class-members',  methods = ['POST', 'GET'])
def classMembeers():
        if request.method == "GET":
            query = "SELECT Classes_Members.classMemberID, Concat(Members.firstName, ' ', Members.lastName) as member, Concat(Classes.classDescription, ' ' ,Classes.classDate, ' ', Classes.startTime) as class from Classes_Members inner join Members on Classes_Members.memberID = Members.memberID inner join Classes on Classes_Members.classID = Classes.classID"
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()
            query = "SELECT memberID, Concat(firstName, ' ', lastName) as member FROM Members"
            cur = mysql.connection.cursor()
            cur.execute(query)
            members = cur.fetchall()
            query = "SELECT classID, Concat(classDescription, ' ', classDate, ' ', startTime) as class FROM Classes"
            cur = mysql.connection.cursor()
            cur.execute(query)
            classes = cur.fetchall()
            return render_template("class-members.html", data = data, members = members, classes = classes)
        if request.method == "POST":
            if request.form.get("addClassMember"):
                memberID = request.form["memberID"]
                classID = request.form["classID"]
                query = "INSERT INTO Classes_Members (memberID, ClassID) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (memberID, classID))
                mysql.connection.commit()
                return redirect("/class-members")     
                      
@app.route('/edit_classMembers/<int:id>',  methods = ['POST', 'GET'])
def editClassMembers(id):
    if request.method == "GET":
        query = "SELECT Classes_Members.classMemberID, Concat(Members.firstName, ' ', Members.lastName) as member, Concat(Classes.classDescription, ' ' ,Classes.classDate, ' ', Classes.startTime) as class from Classes_Members inner join Members on Classes_Members.memberID = Members.memberID inner join Classes on Classes_Members.classID = Classes.classID WHERE classMemberID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        query = "SELECT memberID, Concat(firstName, ' ', lastName) as member FROM Members"
        cur = mysql.connection.cursor()
        cur.execute(query)
        members = cur.fetchall()
        query = "SELECT classID, Concat(classDescription, ' ', classDate, ' ', startTime) as class FROM Classes"
        cur = mysql.connection.cursor()
        cur.execute(query)
        classes = cur.fetchall()
        return render_template("edit-class-member.html", data = data, members = members, classes= classes)
    if request.method == "POST":
        if request.form.get("editClassMember"):
            memberID = request.form["memberID"]
            classID = request.form["classID"]
            query = "UPDATE Classes_Members SET memberID = %s, classID = %s WHERE classMemberID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (memberID, classID, id))
            mysql.connection.commit()
            return redirect("/class-members")


@app.route('/delete_classMembers/<int:id>', methods = ['POST', 'GET'])
def deleteClassMembers(id):
    if request.method == "GET":
        query = "SELECT Classes_Members.classMemberID, Concat(Members.firstName, ' ', Members.lastName) as member, Concat(Classes.classDescription, ' ' ,Classes.classDate, ' ', Classes.startTime) as class from Classes_Members inner join Members on Classes_Members.memberID = Members.memberID inner join Classes on Classes_Members.classID = Classes.classID WHERE classMemberID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template('/delete_classMembers.html', data = data)
    elif request.method == "POST":
        query = "DELETE FROM Classes_Members WHERE classMemberID = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()
        return redirect("/class-members")
          
@app.route('/member-visits', methods = ['POST', 'GET'])
def memberVisits():
     if request.method == "GET":
         query = "SELECT MemberVisits.visitID, Concat(Members.firstName, ' ', Members.lastName) as member, MemberVisits.date from MemberVisits inner join Members on MemberVisits.memberID = Members.memberID"
         cur = mysql.connection.cursor()
         cur.execute(query)
         visits = cur.fetchall()
         query = "SELECT memberID, Concat(firstName, ' ', lastName) as member FROM Members"
         cur = mysql.connection.cursor()
         cur.execute(query)
         members = cur.fetchall()
         return render_template("member-visits.html", data = visits, members = members)
     if request.method == "POST":
         if request.form.get("addMemberVisit"):
             memberID = request.form["memberID"]
             date = request.form["date"]
             query = "INSERT INTO MemberVisits (memberID, date) VALUES (%s, %s)"
             cur = mysql.connection.cursor()
             cur.execute(query, (memberID, date))
             mysql.connection.commit()
             return redirect("/member-visits")
         
         
@app.route('/delete-member-visit/<int:id>', methods = ['POST', 'GET'])
def deleteVisit(id):
    if request.method == "GET":
        query = "SELECT MemberVisits.visitID, Concat(Members.firstName, ' ', Members.lastName) as member, MemberVisits.date from MemberVisits inner join Members on MemberVisits.memberID = Members.memberID WHERE MemberVisits.visitID = %s" %(id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        visits = cur.fetchall()
        # query = "SELECT memberID, Concat(firstName, ' ', lastName) as member FROM Members"
        # cur = mysql.connection.cursor()
        # cur.execute(query)
        # members = cur.fetchall()
        return render_template("delete-member-visit.html", data = visits)
    
    if request.method == "POST":
        query = "DELETE FROM MemberVisits WHERE visitID = %s" %(id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        return redirect("/member-visits")
    

@app.route('/edit-member-visit/<int:id>', methods = ['POST', 'GET'])
def editVisit(id):
    if request.method == "GET":
        query = "SELECT MemberVisits.visitID, Concat(Members.firstName, ' ', Members.lastName) as member, MemberVisits.memberID, MemberVisits.date from MemberVisits inner join Members on MemberVisits.memberID = Members.memberID WHERE MemberVisits.visitID = %s" %(id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        visits = cur.fetchall()
        query = "SELECT memberID, Concat(firstName, ' ', lastName) as member FROM Members"
        cur = mysql.connection.cursor()
        cur.execute(query)
        members = cur.fetchall()
        return render_template("edit-member-visit.html", data = visits, members = members)
    
    if request.method == "POST":
        memberID = request.form['memberID']
        date = request.form['date']
        query = "UPDATE MemberVisits SET memberID = %s, date = %s WHERE visitID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (memberID, date, id))
        mysql.connection.commit()
        return redirect("/member-visits")



@app.route('/employees', methods = ['POST', 'GET'])
def employees():
    if request.method == "GET":
         query = "SELECT employeeID, CONCAT(firstName ,' ', lastName) as name, hireDate, hourlyRate, jobTitle FROM Employees"
         cur = mysql.connection.cursor()
         cur.execute(query)
         employees = cur.fetchall()
         print(employees)
         return render_template("employees.html", data = employees)
    if request.method == "POST":
        if request.form.get("addEmployee"):
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            hireDate = request.form["hireDate"]
            hourlyRate = request.form["hourlyRate"]
            jobTitle = request.form["jobTitle"]
            query = "INSERT INTO Employees (firstName, lastName, hireDate, hourlyRate, jobTitle) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, hireDate, hourlyRate, jobTitle))
            mysql.connection.commit()
            return redirect("/employees")
        
@app.route('/edit-employee/<int:id>', methods = ['POST', 'GET'])
def editEmployees(id):
    
    if request.method == "GET":
        query = "SELECT * FROM Employees WHERE employeeID = %s" %(id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit-employee.html", data = data)
    
    if request.method == "POST":
        if request.form.get("editEmployee"):
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            hireDate = request.form['hireDate']
            hourlyRate = request.form['hourlyRate']
            jobTitle = request.form['jobTitle']

            query = "UPDATE Employees SET firstName = %s, lastName = %s, hireDate = %s, hourlyRate = %s, jobTitle = %s WHERE employeeID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, hireDate, hourlyRate, jobTitle, id))
            mysql.connection.commit()
            return redirect("/employees")
        
@app.route('/delete-employee/<int:id>', methods = ['POST', 'GET'])       
def deleteEmployee(id):
    if request.method == "GET":
        query = "Select * FROM Employees WHERE employeeID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template('/delete-employee.html', data = data)

    elif request.method == "POST":
        query = "DELETE FROM Employees WHERE employeeID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        return redirect("/employees")



@app.route('/invoices', methods = ['POST', 'GET'])
def invoices():
     if request.method == "GET":
         query = "SELECT Invoices.invoiceID, Concat(Members.firstName, ' ', Members.lastName) as member, Invoices.date, Invoices.amountDue from Invoices inner join Members on Invoices.memberID = Members.memberID"
         cur = mysql.connection.cursor()
         cur.execute(query)
         invoices = cur.fetchall()
         query = "SELECT memberID, Concat(firstName, ' ', lastName) as member FROM Members"
         cur = mysql.connection.cursor()
         cur.execute(query)
         members = cur.fetchall()
         return render_template("invoices.html", data = invoices, members = members)
     if request.method == "POST":
         if request.form.get("addInvoice"):
             memberID = request.form["memberID"]
             date = request.form["date"]
             amountDue = request.form["amountDue"]
             query = "INSERT INTO Invoices (memberID, date, amountDue) VALUES (%s, %s, %2s)"
             cur = mysql.connection.cursor()
             cur.execute(query, (memberID, date, amountDue))
             mysql.connection.commit()
             return redirect("/invoices")
         

@app.route("/edit-invoice/<int:id>", methods = ['POST', 'GET'])
def editInvoice(id):
    if request.method == "GET":

        query = "SELECT Invoices.invoiceID, Concat(Members.firstName, ' ', Members.lastName) as member, Invoices.memberID, Invoices.date, Invoices.amountDue from Invoices inner join Members on Invoices.memberID = Members.memberID where Invoices.invoiceID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT memberID, Concat(firstName, ' ', lastName) as member FROM Members"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        members = cur.fetchall()
        return render_template("edit-invoice.html", data = data, members = members)
    
    if request.method == "POST":
        if request.form.get("editInvoice"):

            memberID = request.form["memberID"]
            date = request.form["date"]
            amountDue = request.form["amountDue"]

            query = "UPDATE Invoices SET memberID = %s, date = %s, amountDue = %s WHERE invoiceID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (memberID, date, amountDue, id))
            mysql.connection.commit()
            return redirect("/invoices")
        

@app.route('/delete-invoice/<int:id>', methods = ['POST', 'GET'])       
def deleteInvoice(id):
    if request.method == "GET":
        query = "SELECT Invoices.invoiceID, Concat(Members.firstName, ' ', Members.lastName) as member, Invoices.date, Invoices.amountDue from Invoices inner join Members on Invoices.memberID = Members.memberID where Invoices.invoiceID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("delete-invoice.html", data = data)

    if request.method == "POST":
        query = "DELETE FROM Invoices WHERE invoiceID = %s"%(id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        return redirect("/invoices")




# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2389))
    app.run(port=port, debug=True)