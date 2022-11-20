import os
from flask import Flask, render_template, redirect, request
from cs50 import SQL
from dotenv import load_dotenv
load_dotenv()

#configure flask app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#This is production connection
# connect to database
# database = os.getenv("DB").replace("://", "ql://", 1)
# db = SQL(database)

db = SQL("sqlite:///birthday.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/birthday")
def birthday():
    return render_template("birthday.html", birthday=True) # The birthday prop is used to remove the navbar in the pages they are sent

#Page that says thankyou after after message is received
@app.route("/thankyou", methods=["GET","POST"])
def thankyou():
    if request.method == "POST":

        sender = request.form.get("sender")
        message = request.form.get("message")

        db.execute("INSERT INTO messages VALUES( ?, ?)", sender, message)


        return render_template("thankyou.html")
    return redirect("/birthday")

#Page to view messages
@app.route("/messages")
def messages():

    rows = db.execute("SELECT * FROM messages")

    return render_template("messages.html", messages=rows)