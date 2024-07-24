from flask import render_template, redirect, url_for, session
from app import app

@app.route('/staff/home')
def staff_home():
    if 'loggedin' in session and session['role'] == 'staff':
        return render_template('staff_home.html', username=session['username'], user_role=session['role'])
    return redirect(url_for('login'))
