from flask import render_template

from main import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message='Such page does not exist. Please try something else'), 404


@app.errorhandler(401)
def access_restricted(e):
    return render_template('error.html', message='You do not hve access to this page. Try to log in'), 401


@app.errorhandler(403)
def access_denied(e):
    return render_template('error.html', message='You do not have access to this part of site'), 403


@app.errorhandler(405)
def invalid_method(e):
    return render_template('error.html', message='Used invalid method'), 405
