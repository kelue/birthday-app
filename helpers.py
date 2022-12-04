from flask import redirect, render_template, request, session

def apology(template, message, code=500):
    """Render error on the same page with a message"""

    return render_template(template, error=message), code
