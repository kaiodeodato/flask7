from flask import Flask, render_template, redirect,request
import mysql.connector
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

   
if __name__ == "__main__":
    app.run()