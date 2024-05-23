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
        print(data)
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
        return render_template("edit_classes.html", data = data, instructors = instructors)
    if request.method == "POST":
        if request.form.get("editClass"):
            instructor = request.form['employeeID']
            classDescription = request.form['classDescription']
            classDate = request.form['classDate']
            startTime = request.form['startTime']
            endTime = request.form['endTime']
            roomNumber = request.form['roomNumber']
            print(instructor, classDescription, classDate, startTime, endTime, roomNumber)
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
            print(data)
            return render_template("class-members.html", data = data)

@app.route('/edit_classMembers/<int:id>',  methods = ['POST', 'GET'])
def editClassMembers(id):
    print("in edit")
    if request.method == "GET":
        query = "SELECT Classes_Members.classMemberID, Concat(Members.firstName, ' ', Members.lastName) as member, Concat(Classes.classDescription, ' ' ,Classes.classDate, ' ', Classes.startTime) as class from Classes_Members inner join Members on Classes_Members.memberID = Members.memberID inner join Classes on Classes_Members.classID = Classes.classID WHERE classMemberID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        print(data)
        query = "SELECT memberID, Concat(firstName, ' ', lastName) as member FROM Members"
        cur = mysql.connection.cursor()
        cur.execute(query)
        members = cur.fetchall()
        query = "SELECT classID, Concat(classDescription, ' ', classDate, ' ', startTime) as class FROM Classes"
        cur = mysql.connection.cursor()
        cur.execute(query)
        classes = cur.fetchall()
        print(classes)
        return render_template("edit_class-members.html", data = data, members = members, classes= classes)
    if request.method == "POST":
        if request.form.get("editClassMember"):
            print('editing class member')
            memberID = request.form["memberID"]
            classID = request.form["classID"]
            print(memberID, classID, id)
            query = "UPDATE Classes_Members SET memberID = %s, classID = %s WHERE classMemberID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (memberID, classID, id))
            mysql.connection.commit()
            return redirect("/class-members")
        
@app.route('/member-visits')
def membeerVisits():
    return render_template("member-visits.html")

@app.route('/employees')
def employees():
    return render_template("employees.html")

@app.route('/invoices')
def invoices():
    return render_template("invoices.html")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2389))
    app.run(port=port, debug=True)