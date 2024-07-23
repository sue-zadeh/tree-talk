from flask import render_template, request, redirect, url_for, session, flash
import re
import os
from werkzeug.utils import secure_filename
import mysql.connector
from flask_hashing import Hashing
from app import app, connect

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
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        location = request.form['location']
        file = request.files['profile_pic']

        cursor = getCursor()
        cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif len(password) < 8 or not re.match(r'[A-Za-z0-9]+', password):
            msg = 'Password must be at least 8 characters long and contain letters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Save profile picture
            profile_pic = 'default.png'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_pic = filename

            password_hash = hashing.hash_value(password, PASSWORD_SALT)
            cursor.execute('INSERT INTO users (username, password_hash, email, role, first_name, last_name, date_of_birth, location, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (username, password_hash, email, DEFAULT_USER_ROLE, first_name, last_name, date_of_birth, location, profile_pic))
            db_connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)



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
    app.run(debug=True, port=5001)