from flask import render_template, redirect, url_for, session
from app import app

@app.route('/admin/home')
def admin_home():
    if 'loggedin' in session and session['role'] == 'admin':
        return render_template('admin_home.html', username=session['username'], user_role=session['role'])
    return render_template('error.html')
