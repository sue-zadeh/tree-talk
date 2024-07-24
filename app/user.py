from flask import render_template, redirect, url_for, session
from app import app

@app.route('/user/home')
def user_home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'], user_role=session['role'])
    return redirect(url_for('login'))
