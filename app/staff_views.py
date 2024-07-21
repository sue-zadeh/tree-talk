from flask import render_template, redirect, url_for, session
from app import app

def staff_home():
    @app.route('/staff/home')
    def staff_home_route():
        if 'loggedin' in session and session['role'] == 'staff':
            return render_template('staff_home.html', username=session['username'])
        return render_template('error.html')


# @app.route('/staff/home')
# def staff_dashboard():
#   return "Staff Dashboard"
# @app.route('/staff/profile')
# def staff_profile():
#   return "Staff Profile"