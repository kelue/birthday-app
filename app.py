import os
from flask import Flask, render_template, redirect, request
from cs50 import SQL
from dotenv import load_dotenv
load_dotenv()

#configure flask app
app = Flask(__name__)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# connect to database
database = os.getenv("DB")
db = SQL(database)    

@app.route("/")
def index():

    rows = db.execute("SELECT * FROM messages")

    print(rows)

    return render_template("index.html")


@app.route("/thankyou", methods=["GET","POST"])
def thankyou():
    if request.method == "POST":

        sender = request.form.get("sender")
        message = request.form.get("message")

        db.execute("INSERT INTO messages VALUES( ?, ?)", sender, message)


        return render_template("thankyou.html")
    return redirect("/")

@app.route("/messages")
def messages():

    rows = db.execute("SELECT * FROM messages")

    return render_template("messages.html", messages=rows)