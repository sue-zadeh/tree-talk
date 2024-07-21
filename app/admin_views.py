from flask import render_template, redirect, url_for, session
from app import app

def admin_home():
    @app.route('/admin/home')
    def admin_home_route():
        if 'loggedin' in session and session['role'] == 'admin':
            return render_template('admin_home.html', username=session['username'])
        return render_template('error.html')
