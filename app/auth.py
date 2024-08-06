import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
import mysql.connector
from flask_hashing import Hashing
from mysql.connector import connect, Error
from datetime import datetime
from app import app
from app.database import getCursor  # Importing the centralized getCursor function
import app.connect as connect


PASSWORD_SALT = 'abcd'
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Configuring the upload folder

hashing = Hashing(app)

#---for uploading pics
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
 
 
 
      #------register form-------#
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']  
        email = request.form['email']
        birth_date = request.form['birth_date']
        location = request.form['location']
        file = request.files['profile_image']
        profile_image = None

        # Check if password matches confirm password
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        cursor, conn = getCursor()
        if not cursor or not conn:
            flash('Database connection error', 'error')
            return redirect(url_for('register'))

        try:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
            birth_date = birth_date_obj.strftime('%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD', 'error')
            return redirect(url_for('register'))

        if not re.match(r'^[A-Za-z\s,]+$', location):
            flash('Location must contain only letters, spaces, and commas.', 'error')
            return redirect(url_for('register'))

        if 'profile_image' not in request.files or file.filename == '':
            profile_image = 'default.png'
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_image = filename
        else:
            flash('File not allowed', 'error')
            return redirect(url_for('register'))

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        account = cursor.fetchone()

        if account:
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))

        password = hashing.hash_value(password, '1234abcd')

        cursor.execute("""
            INSERT INTO users (username, first_name, last_name, email, password, birth_date, location, profile_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, first_name, last_name, email, password, birth_date, location, profile_image))
        conn.commit()

        flash('Registration successful. Please login now.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html")
  
  
   #----- login------#
  
@app.route("/login", methods=['POST', 'GET'])
def login():
    toLogin = True
    if request.method == 'POST':
        session.permanent = True
        username = request.form.get('username')
        password = request.form.get('password')
        hashed = hashing.hash_value(password, PASSWORD_SALT)
         
        cursor, conn = getCursor(dictionary=True)
        if not cursor or not conn:
            flash('Database connection error', 'error')
            return redirect(url_for('login'))

        cursor.execute("SELECT username, password FROM users WHERE username=%s AND password=%s AND status=1", (username, hashed))
        user = cursor.fetchone()
        cursor.execute("SELECT username, password FROM users WHERE username=%s AND password=%s AND status=0", (username, hashed))
        inactive_user = cursor.fetchone()

        cursor.execute("SELECT username, password, role FROM users WHERE username=%s AND password=%s AND role != 'admin' AND status=1", (username, hashed))
        moderator = cursor.fetchone()
        cursor.execute("SELECT username, password, role FROM users WHERE username=%s AND password=%s AND status=0", (username, hashed))
        inactive_moderator = cursor.fetchone()

        cursor.execute("SELECT username, password, role FROM users WHERE username=%s AND password=%s AND role='admin'", (username, hashed))
        admin = cursor.fetchone()

        cursor.close()
        conn.close()
        
        if user:
            session["member"] = username
            return redirect(url_for("community"))
        elif moderator:
            session["moderator"] = username
            return redirect(url_for("community"))
        elif admin:
            session["admin"] = username
            return redirect(url_for("community"))
        elif inactive_user:
            msg = 'User is not active. Please contact an admin to solve the issue - admin email: sara.hey@admin.com'
            return render_template("login.html", msg=msg, toLogin=toLogin)
        elif inactive_moderator:
            msg = 'Moderator account is not active. Please contact an admin to solve the issue - admin email: john.murray123@admin.com'
            return render_template("login.html", msg=msg, toLogin=toLogin)
        else:
            msg = 'Username or password not correct. Please try again.'
            return render_template("login.html", msg=msg, toLogin=toLogin)
    else:
        return redirect_based_on_role('login.html')

#----logout---#

@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("moderator", None)
    session.pop("admin", None) 
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))