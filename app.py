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
        print("in POST")
        if request.form.get("addMember"):
            print("Trying to add member")
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

@app.route('/classes')
def classes():
    return render_template("classes.html")

@app.route('/class-members')
def classMembeers():
    return render_template("class-members.html")

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
    port = int(os.environ.get('PORT', 2382))
    app.run(port=port, debug=True)