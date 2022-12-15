import os
from flask import Flask, render_template, redirect, request, session, url_for
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, allowed_file
from dotenv import load_dotenv
load_dotenv()

# configure image upload folder
UPLOAD_FOLDER = './static/users'

#configure flask app
app = Flask(__name__)

# set upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
database = os.getenv("DB").replace("://", "ql://", 1)
db = SQL(database)

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

        user = request.form.get("username").lower()
        password = request.form.get("password")

        # Ensure username was submitted
        if not user:
            return apology("login.html", "Must provide username!!!", 403)

        # Ensure password was submitted
        elif not password:
            return apology("login.html", "Must provide password!!!", 403)

        # Query database for username
        rows = db.execute("SELECT username, passhash FROM users WHERE username = ? OR email = ?", user, user)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["passhash"], password):
            return apology("login.html", "Invalid username and password!!!", 403)

        # Remember which user has logged in
        session["user"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/dashboard")

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
        name = request.form.get("name").lower()
        user = request.form.get("username").lower()
        email = request.form.get("email").lower()
        password = request.form.get("password")
        passConfirm = request.form.get("confirmpassword")

        # check for valid user name
        if not user:
            return apology("register.html", "Username cannot be blank!!!", 403)
        # check for valid password
        elif not password:
            return apology("register.html", "Must enter password!!!", 403)
        # check for valid name
        elif not name:
            return apology("register.html", "Must enter name!!!", 403)
        # check for valid email
        elif not email:
            return apology("register.html", "Must enter email!!!", 403)
        # check for confirm password input
        elif not passConfirm:
            return apology("register.html", "Retype password!!!", 403)
        # check that both password inputs match
        elif password != passConfirm:
            return apology("register.html", "passwords do not match!!!", 403)

        rows = db.execute("SELECT username, email FROM users WHERE username = ? OR email = ?", user, email)

        print({"rows": rows})

        names = []
        emails = []

        for row in rows:
            names.append(row["username"])

        for row in rows:
            emails.append(row["email"])

        if user in names:
            return apology("register.html", "user with this username already exists!!")

        if email in emails:
            return apology("register.html", "user with this email already exists!!")

        # hash password
        passhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        id = db.execute("INSERT INTO users (username, name, email, passhash) VALUES (?, ?, ?, ?) RETURNING id", user, name, email, passhash)

        # Remember which user has registered and log them in
        session["user"] = user

        # Redirect user to home page
        return redirect("/dashboard")
    else:
        return render_template("register.html")

# display user dashboard
@app.route("/dashboard")
def dashboard():
    user = session["user"]
    link = os.getenv("link")

    return render_template("dashboard.html", user=user, link=link)

# user setting page
@app.route("/settings")
def settings():
    
    return render_template("settings.html")

# route to handle user settings input
@app.route("/set", methods=['GET', 'POST'])
def upload_file():
    user = session["user"]

    if request.method == "POST":
        cover_image = request.files['coverImage']
        form_image = request.files['formImage']
        thank_image = request.files['thanksImage']

        # if user does not select file, browser also
        # submit an empty part without filename
        if cover_image.filename == '' or form_image.filename == '' or thank_image.filename == '':
            return apology('settings.html', 'Must select an image for all file parts!!!')

        else:
            if cover_image and allowed_file(cover_image.filename):
                cover_file = user + '-' + cover_image.filename
                cover_filename = secure_filename(cover_file)
            else:
                return apology('settings.html', 'Selected file must be either png, jpeg or jpg format!!!')


            if form_image and allowed_file(form_image.filename):
                form_file = user + '-' + form_image.filename
                form_filename = secure_filename(form_file)
                
            else:
                return apology('settings.html', 'Selected file must be either png, jpeg or jpg format!!!')

            if thank_image and allowed_file(thank_image.filename):
                thank_file = user + '-' + thank_image.filename
                thank_filename = secure_filename(thank_file)
            else:
                return apology('settings.html', 'Selected file must be either png, jpeg or jpg format!!!')

            # if all files are of the correct format, save to the filesystem
            cover_image.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))
            form_image.save(os.path.join(app.config['UPLOAD_FOLDER'], form_filename))
            thank_image.save(os.path.join(app.config['UPLOAD_FOLDER'], thank_filename))

            # save to database
            id = db.execute("INSERT INTO settings (username, cover_file, form_file, thanks_file) VALUES (?, ?, ?, ?) RETURNING id", user, cover_filename, form_filename, thank_filename)

            # return to settings page and display pictures
            if id:
                return redirect(url_for("settings", cover=cover_filename, form=form_filename, thanks=thank_filename))
    else:
        return redirect(url_for('settings'))


@app.route("/birthday/<user>")
def birthday(user):
    return render_template("birthday.html", user=user, birthday=True) # The birthday prop is used to remove the navbar in the pages they are sent

# route to handle birthday form
@app.route("/thanks", methods=["POST"])
def thanks():
    if request.method == "POST":

        sender = request.form.get("sender")
        message = request.form.get("message")
        user = request.form.get("user")

        if sender == '' or message == '':
            return apology("birthday.html", "Message must include a sender and a message", 403)

        db.execute("INSERT INTO messages (username, sender, message) VALUES(?, ?, ?) RETURNING id", user, sender, message)

        return redirect(url_for("thankyou", user=user))

# Page that says thankyou after after message is received
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html", birthday=True)

#Page to view messages
@app.route("/messages")
def messages():
    user = session["user"]

    rows = db.execute("SELECT * FROM messages WHERE user = ?", user)

    return render_template("messages.html", messages=rows, birthday=True)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
