import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import mysql.connector
from flask_hashing import Hashing
from app import app

@app.route('/')
def home():
    return render_template('index.html')

def getCursor():
    """Gets a new dictionary cursor for the database."""
    global db_connection

    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect(user=connect.dbuser,
                                                password=connect.dbpass, 
                                                host=connect.dbhost, 
                                                database=connect.dbname, 
                                                autocommit=True)
    
    cursor = db_connection.cursor(dictionary=True)
    return cursor


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
        role = request.form['role']
        file = request.files['profile_pic']

        if 'profile_pic' not in request.files or file.filename == '':
            profile_pic = None
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_pic = filename
        else:
            msg = 'File not allowed'
        
        cursor = getCursor()
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
            if role == 'user':
                table = 'users'
            elif role == 'staff':
                table = 'staffs'
            elif role == 'admin':
                table = 'admins'
            else:
                table = 'users'
            cursor.execute(f'INSERT INTO {table} (username, first_name, last_name, password_hash, email, date_of_birth, location, role, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                           (username, first_name, last_name, password_hash, email, date_of_birth, location, role, profile_pic))
            db_connection.commit()
            msg = 'You have successfully registered!'
            session['loggedin'] = True
            session['username'] = username
            session['role'] = role
            return redirect(url_for(f'{role}_home'))

    return render_template('register.html', msg=msg)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    msg = ''
    if 'loggedin' in session:
        cursor = getCursor()
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
        
        cursor.execute('SELECT username, first_name, last_name, email, date_of_birth, location, profile_pic, role FROM users WHERE user_id = %s', (session['id'],))
        account = cursor.fetchone()

        return render_template('profile.html', account=account, msg=msg)
    
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET'])
def edit_profile():
    if 'loggedin' in session:
        cursor = getCursor()
        cursor.execute('SELECT username, first_name, last_name, email, date_of_birth, location, profile_pic FROM users WHERE user_id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('edit_profile.html', account=account)
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        userRole = request.form['rl']
        session['user'] = user  # Set the session's user
        session['role'] = userRole  # Set the session's role
        return redirect(url_for('user'))  # Redirect to the user page
    else:
        if "user" in session:
            return redirect(url_for('user'))
        return render_template('login.html')


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
      
      

@app.route("/logout")
def logout():
    session.pop('user', None)  # Session is cleared at logout
    session.pop('role', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)