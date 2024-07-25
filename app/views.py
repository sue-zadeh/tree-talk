# app/routes.py
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import mysql.connector
from flask_hashing import Hashing
from datetime import datetime
from app import app


@app.route('/')
def home():
    return render_template('index.html')

# hashing = Hashing(app)
# db_connection = None  # Global variable for database connection

def getCursoe():
    """Gets a new dictionary cursor for the database."""
    global db_connection
    import connect
    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect(user=connect.dbuser,
                                                password=connect.dbpass, 
                                                host=connect.dbhost, 
                                                database=connect.dbname, 
                                                autocommit=True)
    cursor = db_connection.cursor(dictionary=True)
    return cursor

# Utility function to check file extensions
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        location = request.form['location']
        role = 'member'  # Role is set to 'member' by default
        file = request.files['profile_pic']

        if 'profile_pic' not in request.files or file.filename == '':
            profile_pic = 'default.png'
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_pic = filename
        else:
            msg = 'File not allowed'
            flash(msg, 'error')
            return render_template('register.html', msg=msg)
        
        cursor = getCursoe()
        cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            password_hash = hashing.hash_value(password, 'ExampleSaltValue')
            cursor.execute('INSERT INTO users (username, first_name, last_name, password_hash, email, date_of_birth, location, role, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                           (username, first_name, last_name, password_hash, email, date_of_birth, location, role, profile_pic))
            db_connection.commit()
            msg = 'You have successfully registered!'
            flash(msg, 'success')
            return redirect(url_for('login'))

    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        user_password = request.form['password']
        
        cursor = getCursoe()
        cursor.execute('SELECT user_id, username, password_hash, role FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            password_hash = account['password_hash']
            if hashing.check_value(password_hash, user_password, 'ExampleSaltValue'):
                session['loggedin'] = True
                session['id'] = account['user_id']
                session['username'] = account['username']
                session['role'] = account['role']
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                msg = 'Incorrect password!'
        else:
            msg = 'Incorrect username!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.clear()  # Session is cleared at logout
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    msg = ''
    if 'loggedin' in session:
        cursor = getCursoe()
        if request.method == 'POST':
            email = request.form['email']
            date_of_birth = request.form['date_of_birth']
            location = request.form['location']
            file = request.files['profile_pic']
            profile_pic = None

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_pic = filename

            cursor.execute('UPDATE users SET email = %s, date_of_birth = %s, location = %s, profile_pic = %s WHERE user_id = %s',
                           (email, date_of_birth, location, profile_pic, session['id']))
            db_connection.commit()
            msg = 'Profile updated successfully!'
            flash(msg, 'success')
        
        cursor.execute('SELECT username, first_name, last_name, email, date_of_birth, location, profile_pic, role FROM users WHERE user_id = %s', (session['id'],))
        account = cursor.fetchone()

        return render_template('profile.html', account=account, msg=msg)
    
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET'])
def edit_profile():
    if 'loggedin' in session:
        cursor = getCursoe()
        cursor.execute('SELECT username, first_name, last_name, email, date_of_birth, location, profile_pic FROM users WHERE user_id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('edit_profile.html', account=account)
    return redirect(url_for('login'))

@app.route('/admin_home')
def admin_home():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_home.html')

@app.route('/moderator_home')
def moderator_home():
    if 'role' not in session or session['role'] != 'moderator':
        return redirect(url_for('login'))
    return render_template('moderator_home.html')

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        userRole = session["role"]
        return f"<h1>{user}</h1>{user} {userRole}</h1>"
    else:
        return redirect(url_for('login'))

@app.route("/staff")
def staff():
    if "user" in session:
        if session["role"] == "staff":  # Check the role of the user
            return render_template('staff.html')
        else:
            return "Illegal Access"  # Anyone else other than staff
    else:
        return redirect(url_for('login'))

@app.route("/admin")
def admin():
    if "user" in session:
        if session["role"] == "admin":  # Check the role of the user
            return render_template('admin.html')
        else:
            return "Illegal Access"  # Anyone else other than admin
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
