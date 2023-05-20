from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def create_db_connection():
    connection = mysql.connector.connect(
        host='162.241.2.19',
        port='3306',
        database='kaiode77_memory',
        user='kaiode77_criptografado',
        password=os.getenv('chave')
    )
    return connection


def conect(query):
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=['GET', "POST"])
def login():
    if session:
        return redirect("/")
    session.clear()
    msg = ''
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        query = ("SELECT * FROM profiles WHERE profile_name = '{}' AND profile_hash = '{}'".format(name, password))
        result = conect(query)
        if result:
            session["name"] = name
            session["id"] = result[0][0]
            return redirect("/")
        else:
            return render_template("login.html", msg="Invalid user or password")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if session:
        return redirect("/")
    msg = ''
    if request.method == "POST":
        # todays date
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # inputs user
        name = request.form.get("name")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # if one input is empty
        if name == '' or password == '' or confirmation == '':
            return render_template("register.html", msg="all inputs are required")
        # check if the password checks
        if not password == confirmation:
            return render_template("register.html", msg="passwords not equal")
        # insert new profile to the database
        query = ("INSERT INTO profiles(profile_name, profile_hash, profile_signin) VALUES ('{}','{}','{}')".format(name, password, date))
        conect(query)
        return render_template("index.html")
    return render_template("register.html")

@app.route("/logout")
def loglogoutoff():
    session.clear()
    return redirect("/")

# @app.route("/cli/<comand>", methods=['GET'])
# def add_comand(comand):
#     query = ("{}".format(comand))
#     conect(query)
#     return redirect("/")

if __name__ == "__main__":
    app.run() 

