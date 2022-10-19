from flask import Flask, render_template

#configure flask app
app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")