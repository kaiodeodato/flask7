from flask import Flask, render_template, redirect, request, session
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)

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
def call():
    responde = conect("SELECT * FROM users")
    return render_template("index.html", users=responde)

@app.route("/user/<username>", methods=['GET'])
def add_user(username):
    query = ("INSERT INTO users(user_name) VALUES ('{}')".format(username))
    conect(query)
    return redirect("/")

@app.route("/cli/<comand>", methods=['GET'])
def add_comand(comand):
    query = ("{}".format(comand))
    conect(query)
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
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
        profiles = conect("SELECT * FROM profiles")
        return render_template("index.html", users = profiles)
    return render_template("register.html")

if __name__ == "__main__":
    app.run()

