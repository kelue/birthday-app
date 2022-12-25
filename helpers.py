from flask import redirect, render_template, session
from functools import wraps

# extensions for image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def apology(template, message, code=500):
    """Render error on the same page with a message"""

    return render_template(template, error=message), code

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
