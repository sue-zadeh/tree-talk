import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
import mysql.connector
from flask_hashing import Hashing
from mysql.connector import connect, Error
from datetime import datetime
from app import app
import connect as connect


app.secret_key = 'e2e62cdb171271f0b12e5043f9f84208eba1f05c8658704e'
PASSWORD_SALT = '1234abcd'

hashing = Hashing(app)

db_connection = None

def getCursor(dictionary=False, buffered=False):
    global db_connection

    try:
        if db_connection is None or not db_connection.is_connected():
            db_connection = mysql.connector.connect(
                user=connect.dbuser,
                password=connect.dbpass,
                host=connect.dbhost,
                database=connect.dbname,
                auth_plugin='mysql_native_password',
                autocommit=True
            )
            print("Connection successful")

        cursor = db_connection.cursor(dictionary=dictionary, buffered=buffered)
        return cursor, db_connection

    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        return None, None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


# ------ members, moderators, admins
def redirect_based_on_role(html_file):
     if "member" in session:
         return redirect(url_for("community"))
     elif "moderator" in session:
        return redirect(url_for("community"))
     elif "admin" in session:
        return redirect(url_for("community"))
     else:
         return render_template(html_file)
    
def render_login_or_register(registered, toLogin, msg, username):
    if toLogin:
        return render_template('login.html', msg=msg, toLogin=toLogin, registered=registered, username=username) 
    else:
        return render_template("register.html", msg=msg, toLogin=toLogin)
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#-- home page
@app.route("/")
def home():
    return render_template("index.html")

# @app.route('/uploads/<filename>')

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
  
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor, conn = getCursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and hashing.check_value(user['password'], password, PASSWORD_SALT):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('community'))

        flash('Invalid username or password.', 'danger')
        return redirect(url_for('login'))

    return render_template("login.html")
#----logout---#

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
  
   #------- Profile view
   
# Profile route
@app.route('/profile')
def profile():
    if 'user_id' in session:
        cursor, conn = getCursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()
        return render_template("profile.html", user=user)
    return redirect(url_for('login'))

# Edit Profile view
@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'user' in session:
        cursor = getCursor(dictionary=True)
        email = request.form['email']
        location = request.form['location']
        file = request.files['profile_image']

        profile_image = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_image = filename

        cursor.execute("""
            UPDATE users SET email = %s, location = %s, profile_image = %s WHERE username = %s
        """, (email, location, profile_image, session['user']))
        db_connection.commit()
        cursor.close()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

# Change Password view
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user' in session:
        if request.method == 'POST':
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            if new_password == confirm_password:
                cursor = getCursor(dictionary=True)
                cursor.execute("SELECT password FROM users WHERE username = %s", (session['user'],))
                user = cursor.fetchone()
                
                if hashing.check_value(user['password'], old_password, PASSWORD_SALT):
                    hashed_password = hashing.hash_value(new_password, PASSWORD_SALT)
                    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, session['user']))
                    db_connection.commit()
                    flash('Password changed successfully!', 'success')
                else:
                    flash('Old password is incorrect', 'error')
                
                cursor.close()
            else:
                flash('New passwords do not match', 'error')
        return render_template('change_password.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    
