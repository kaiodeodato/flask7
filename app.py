from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    name = 'kaio'
    return render_template("index.html", name=name)

@app.route("/<username>")
def user(username):
    return render_template("index.html", name=username)


if __name__ == "__main__":
    app.run()