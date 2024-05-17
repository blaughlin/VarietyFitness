from flask import Flask, render_template
import os

# Configuration

app = Flask(__name__)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/members')
def members():
    return render_template("members.html")

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
    port = int(os.environ.get('PORT', 2389))
    app.run(port=port, debug=True)