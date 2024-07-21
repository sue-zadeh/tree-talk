from flask import flask, render_template, request, redirect, url_for, session, flash
import re
import os
from werkzeug.utils import secure_filename
import mysql.connector
from flask_hashing import Hashing
from app import app, connect

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'ExampleSecretKey'

# IMPORTANT: Change 'ExampleSaltValue' to whatever salt value you'll use in
# your application. If you don't do this, your password hashes won't work!
PASSWORD_SALT = 'asdf'
# Default role assigned to new users upon registration.
DEFAULT_USER_ROLE = 'user'
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

hashing = Hashing(app)  #create an instance of hashing

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getCursor():
    """Gets a new dictionary cursor for the database.
    If necessary, a new database connection be created here and used for all
    subsequent to getCursor()."""
    global db_connection
    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect(user=connect.dbuser, \
            password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
            database=connect.dbname, autocommit=True)
    
    cursor = db_connection.cursor(dictionary=True)
    return cursor

@app.route('/register', method=['GET', 'POST'])
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
    file = request.files['profile_pic']
    
  if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    msg = 'Invalid email address !'
  elif  not re.match(r'[A-Za-z0-9]+', username):
    msg = 'Username must contain only characters and numbers !'
  elif not username or not first_name or not last_name or not password or not email or not date_of_birth or not location:
     msg = 'Please fill out the form !'
  elif len(password) <8:
    msg = 'Password must be at least 8 characters long !'
  elif not any(char.isdigit() for char in password) or not any (char.isalpha() for char in password):
    msg = 'Password must contain at least one letter and one number !'     
  if 'profile_pic' not in request.files or file.filename == '':
       filename = secure_filename('default.png')
  elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        profile_pic = filename
  else:
      msg ='file not allowed'
  if msg == '':    
      cursor = getCursor()
      cursor.excute('SELECT user_id FROM users WHERE username = %s', (username,))
      # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
      account = cursor.fetchone()
      
  if account:
      msg = 'Account already exists !'
  else:
      password_hash = hashing.hash_value(password, PASSWORD_SALT)
      cursor.execute = ('INSERT INTO users (username, first_name, last_name, password_hash, email, date_of_birth, location, role, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                       (username, first_name, last_name, password_hash, email, date_of_birth, location, DEFAULT_USER_ROLE, profile_pic))
      # cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (username, password, email, DEFAULT_USER_ROLE))
  db_connection.commit()
  msg = 'You have successfully registered !'
  flash(msg)
  return render_template('register.html', msg = msg)

  

if __name__ == '__main__':
    app.run(debug=True)



# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
# @app.route('/')
# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     # Output message if something goes wrong...
#     msg = ''
    
#     # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         # Create variables for easy access
#         username = request.form['username']
#         user_password = request.form['password']
        
#         # Check if account exists using MySQL
#         cursor = getCursor()
#         cursor.execute('SELECT user_id, username, password_hash, role FROM users WHERE username = %s', (username,))
        
#         # Fetch one record and return result
#         account = cursor.fetchone()
#         if account is not None:
#             password_hash = account['password_hash']
#             if hashing.check_value(password_hash, user_password, PASSWORD_SALT):

#             # If account exists in accounts table 
#             # Create session data, we can access this data in other routes
#                 session['loggedin'] = True
#                 session['id'] = account['user_id']
#                 session['username'] = account['username']
#                 session['role'] = account['role']
#                 # Redirect to home page
#                 if session['role'] == 'user':
#                     return redirect(url_for('user_home'))
#                 elif session['role'] == 'staff':
#                     return redirect(url_for('staff_home'))
#                 else:
#                     return redirect(url_for('admin_home'))
#             else:
#                 #password incorrect
#                 msg = 'Incorrect password!'
#         else:
#             # Account doesnt exist or username incorrect
#             msg = 'Incorrect username'

#     # Show the login form with message (if any)
#     return render_template('index.html', msg=msg)

# # http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     # Output message if something goes wrong...
#     msg = ''

#     # Check if "username", "password" and "email" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         # Create variables for easy access
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']

#         # Check if account exists using MySQL
#         cursor = getCursor()
#         cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
#         account = cursor.fetchone()

#         # If account exists show error and validation checks
#         if account:
#             msg = 'Account already exists!'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address!'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers!'
#         elif not username or not password or not email:
#             msg = 'Please fill out the form!'
#         else:
#             # Account doesn't exist and the form data is valid, now insert new account into accounts table
#             password_hash = hashing.hash_value(password, PASSWORD_SALT)
#             cursor.execute('INSERT INTO users (username, password_hash, email, role) VALUES (%s, %s, %s, %s)',
#                            (username, password_hash, email, DEFAULT_USER_ROLE))
#             db_connection.commit()
#             msg = 'You have successfully registered!'
#     elif request.method == 'POST':
#         # Form is empty... (no POST data)
#         msg = 'Please fill out the form!'

#     # Show registration form with message (if any)
#     return render_template('register.html', msg=msg)

# # http://localhost:5000/home - this will be the home page, only accessible for loggedin users
# @app.route('/user/home')
# def user_home():
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         # User is loggedin show them the home page
#         return render_template('home.html', username=session['username'], user_role=session['role'])
    
#     # User is not logged in - redirect to login page
#     return redirect(url_for('login'))

# # http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
# @app.route('/profile')
# def profile():
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         # We need all the account info for the user so we can display it on the profile page
#         cursor = getCursor()
#         cursor.execute('SELECT username, email, role FROM users WHERE user_id = %s', (session['id'],))
#         account = cursor.fetchone()

#         # Show the profile page with account info
#         return render_template('profile.html', account=account, username=session['username'], user_role=session['role'])
    
#     # User is not logged in - redirect to login page
#     return redirect(url_for('login'))

# # http://localhost:5000/logout - this will be the logout page
# @app.route('/logout')
# def logout():
#     # Remove session data, this will log the user out
#    session.pop('loggedin', None)
#    session.pop('id', None)
#    session.pop('username', None)

#    # Redirect to login page
#    return redirect(url_for('login'))
