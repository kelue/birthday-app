import os
from flask import Flask, render_template, redirect, request, session
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology
from dotenv import load_dotenv
load_dotenv()

#configure flask app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("login.html", "Must provide username!!!", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("login.html", "Must provide password!!!", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("login.html", "Invalid username and password!!!", 403)

        # Remember which user has logged in
        session["user"] = rows[0]["username"]
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # extract all details from form
        name = request.form.get("name")
        user = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        passConfirm = request.form.get("confirmpassword")

        # check for valid user name
        if not user:
            return apology("register.html", "Username cannot be blank", 403)
        # check for valid password
        elif not password:
            return apology("register.html", "Must enter password", 403)
        # check for valid name
        elif not name:
            return apology("register.html", "Must enter name", 403)
        # check for valid email
        elif not email:
            return apology("register.html", "Must enter email", 403)
        # check for confirm password input
        elif not passConfirm:
            return apology("register.html", "Retype password ", 403)
        # check that both password inputs match
        elif password != passConfirm:
            return apology("register.html", "passwords do not match", 403)

        rows = db.execute("SELECT username, email FROM users")

        names = []
        emails = []

        for row in rows:
            names.append(row["username"])

        for email in emails:
            emails.append(row["email"])

        if user in names:
            return apology("register.html", "user with this username already exists!!")

        if email in emails:
            return apology("register.html", "user with this email already exists!!")

        # hash password
        passhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        id = db.execute("INSERT INTO users (username, name, email, hash) VALUES (?, ?, ?, ?)", user, name, email, passhash)

        # Remember which user has registered and log them in
        session["user"] = user
        session["user_id"] = id

        # Redirect user to home page
        return redirect("/")

    else:
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
