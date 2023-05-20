from flask import Flask, render_template, redirect
import mysql.connector
import os

app = Flask(__name__)

def create_db_connection():
    
    connection = mysql.connector.connect(
        host='162.241.2.19',
        port='3306',
        database='kaiode77_memory',
        user='kaiode77_criptografado',
        password=os.getenv(chave)
    )
    return connection

@app.route("/")
def call():
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("index.html", users=result)

@app.route("/user/<username>", methods=['POST','GET'])
def add_user(username):
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users(user_name) VALUES (%s)"
    cursor.execute(query, (username,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect("/")


# @app.route("/")
# def home():
#     name = 'kaio'
#     return render_template("index.html", name=name)

# @app.route("/<username>")
# def user(username):
#     return render_template("index.html", name=username)


if __name__ == "__main__":
    app.run()