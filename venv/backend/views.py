import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash,g
# from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import mysql.connector
from flask_hashing import Hashing
from mysql.connector import connect, Error
from datetime import datetime
from app import app
import app.connect as connect

app.secret_key = 'e2e62cdb171271f0b12e5043f9f84208eba1f05c8658704e'
hashing = Hashing(app)

DEFAULT_USER_ROLE = 'user'

db_connection = None

def getCursor():
    """Gets a new dictionary cursor for the database.
    
    If necessary, a new database connection be created here and used for all
    subsequent to getCursor()."""
    global db_connection

    if db_connection is None or not db_connection.is_connected():
        db_connection = mysql.connector.connect(user=connect.dbuser, \
            password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
            database=connect.dbname, autocommit=True)
        print("Connection successful")
    
    cursor = db_connection.cursor(dictionary=True, buffered=True)
    
    return cursor
        

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@views.route("/")
def home():
    return render_template("community.html")
  
  # community center
  
  @views.route('/community', methods=['GET', 'POST'])
def post_message():
    cursor, conn = getCursor(dictionary=True)
    if request.method == 'POST':
        content = request.form['content']
        user_id = session.get('user_id')
        if not user_id:
            flash('Please login to post a message.', 'error')
            return redirect(url_for('login'))
        
        # Handle file upload
        file = request.files['media']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(views.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        
        cursor.execute("""
            INSERT INTO messages (user_id, title, content, created_at)
            VALUES (%s, %s, %s, %s)
        """, (user_id, 'New Message', content, datetime.now()))
        message_id = cursor.lastrowid

        if filename:
            cursor.execute("""
                INSERT INTO media (message_id, filename)
                VALUES (%s, %s)
            """, (message_id, filename))

        conn.commit()
        flash('Message posted successfully!', 'success')
        return redirect(url_for('post_message'))

    cursor.execute("""
        SELECT messages.*, users.username, media.filename 
        FROM messages 
        JOIN users ON messages.user_id = users.user_id 
        LEFT JOIN media ON messages.message_id = media.message_id
        ORDER BY messages.created_at DESC
    """)
    messages = cursor.fetchall()

    cursor.execute("""
        SELECT replies.*, users.username 
        FROM replies 
        JOIN users ON replies.user_id = users.user_id
    """)
    replies = cursor.fetchall()

    return render_template("community.html", messages=messages, replies=replies)

@views.route('/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    cursor, conn = getCursor()
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login to delete your message.', 'error')
        return redirect(url_for('login'))

    cursor.execute("DELETE FROM replies WHERE message_id = %s", (message_id,))
    cursor.execute("DELETE FROM messages WHERE message_id = %s AND user_id = %s", (message_id, user_id))
    conn.commit()

    flash('Message deleted successfully!', 'success')
    return redirect(url_for('post_message'))

@views.route('/like_message/<int:message_id>', methods=['POST'])
def like_message(message_id):
    cursor, conn = getCursor()
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login to like a message.', 'error')
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM likes WHERE user_id = %s AND message_id = %s", (user_id, message_id))
    like = cursor.fetchone()

    if like:
        cursor.execute("DELETE FROM likes WHERE like_id = %s", (like['like_id'],))
    else:
        cursor.execute("INSERT INTO likes (user_id, message_id, type) VALUES (%s, %s, %s)", (user_id, message_id, 'like'))
    
    conn.commit()
    return redirect(url_for('post_message'))

@views.route('/dislike_message/<int:message_id>', methods=['POST'])
def dislike_message(message_id):
    cursor, conn = getCursor()
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login to dislike a message.', 'error')
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM likes WHERE user_id = %s AND message_id = %s", (user_id, message_id))
    like = cursor.fetchone()

    if like:
        cursor.execute("DELETE FROM likes WHERE like_id = %s", (like['like_id'],))
    else:
        cursor.execute("INSERT INTO likes (user_id, message_id, type) VALUES (%s, %s, %s)", (user_id, message_id, 'dislike'))
    
    conn.commit()
    return redirect(url_for('post_message'))
  
  
  


@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        email = request.form['email']
        birth_date = request.form['birth_date']
        location = request.form['location']
        file = request.files['profile_image']
        profile_image = None

        cursor, conn = getCursor()
        
        #  DD-MM-YYYY format
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
            file.save(os.path.join(views.config['UPLOAD_FOLDER'], filename))
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


@views.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        userRole = request.form['rl']
        session['user'] = user  # Set the session's user
        session['role'] = userRole  # Set the session's role
        return redirect(url_for('community'))  # Redirect to the user page
    else:
        if "user" in session:
            return redirect(url_for('user'))
        return render_template('login.html')

# http://localhost:5000/logout - this will be the logout page
@views.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   flash('You have been logged out.', 'success')
   return redirect(url_for('home'))


# @app.route('/logout')
# def logout():
#     session.clear()  
#     flash('You have been logged out.', 'success')
#     return redirect(url_for('home'))

@views.route('/profile', methods=['GET'])
def profile():
    if 'user_id' in session:
        cursor, conn = getCursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM messages WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
        messages = cursor.fetchall()
        account_to_delete = cursor.fetchone()
        return render_template("profile.html", user=user, account_to_delete=account_to_delete)


@views.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' in session:
        cursor, conn = getCursor()
        if request.method == 'POST':
            email = request.form['email']
            birth_date = request.form['date_of_birth']
            location = request.form['location']
            file = request.files['profile_image']
            profile_image = None

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(views.config['UPLOADS_FOLDER'], filename))
                profile_image = filename

            cursor.execute("""
                UPDATE users SET email = %s, birth_date = %s, location = %s, profile_image = %s WHERE user_id = %s
            """, (email, birth_date, location, profile_image, session['user_id']))
            conn.commit()
            flash('Profile updated successfully!', 'success')
        
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()
        return render_template('edit_profile.html', user=user)
    return redirect(url_for('login'))
  
  
  
  
  
# memders(sidebar item)
@views.route('/members', methods=['GET', 'POST'])
def members():
    cursor, conn = getCursor()  # Ensure connection management is handled
    search_query = request.form.get('search', '').strip() if request.method == 'POST' else ''
    results = []
    message = ""

    if search_query:
        # Perform the search
        cursor.execute("""
            SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name 
            FROM users 
            WHERE (role = 'member') AND (first_name LIKE %s OR last_name LIKE %s) 
            ORDER BY first_name, last_name
        """, ('%' + search_query + '%', '%' + search_query + '%'))
        results = cursor.fetchall()
        if not results:
            message = f"Sorry, there are no results for '{search_query}'."

    # Always fetch all members for the gallery, regardless of search
    cursor.execute("""
        SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name
        FROM users
        WHERE role = 'member'
        ORDER BY first_name, last_name
    """)
    members = cursor.fetchall()
    return render_template("members.html", results=results, members=members, message=message)

    # admins(sidebar item)
@views.route('/admins', methods=['GET', 'POST'])
def admins():
    cursor, conn = getCursor()  # Ensure connection management is handled
    search_query = request.form.get('search', '').strip() if request.method == 'POST' else ''
    results = []
    message = ""

    if search_query:
        # Perform the search
        cursor.execute("""
            SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name 
            FROM users 
            WHERE (role = 'admin') AND (first_name LIKE %s OR last_name LIKE %s) 
            ORDER BY first_name, last_name
        """, ('%' + search_query + '%', '%' + search_query + '%'))
        results = cursor.fetchall()
        if not results:
            message = f"Sorry, there are no results for '{search_query}'."

    # Always fetch all members for the gallery, regardless of search
    cursor.execute("""
        SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name
        FROM users
        WHERE role = 'admin'
        ORDER BY first_name, last_name
    """)
    admins = cursor.fetchall()
    return render_template("admins.html", results=results, admins=admins, message=message)


   
  # moderators(sidebar item)
@views.route('/moderators' , methods=['GET', 'POST'])
def moderators():
    cursor, conn = getCursor()  # Ensure connection management is handled
    search_query = request.form.get('search', '').strip() if request.method == 'POST' else ''
    results = []
    message = ""

    if search_query:
        # Perform the search
        cursor.execute("""
            SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name 
            FROM users 
            WHERE (role = 'moderator') AND (first_name LIKE %s OR last_name LIKE %s) 
            ORDER BY first_name, last_name
        """, ('%' + search_query + '%', '%' + search_query + '%'))
        results = cursor.fetchall()
        if not results:
            message = f"Sorry, there are no results for '{search_query}'."

    # Always fetch all members for the gallery, regardless of search
    cursor.execute("""
        SELECT user_id, COALESCE(profile_image, '/static/assets/default.jpg') AS profile_image, first_name, last_name
        FROM users
        WHERE role = 'moderator'
        ORDER BY first_name, last_name
    """)
    moderators = cursor.fetchall()
    return render_template("moderators.html", results=results, moderators=moderators, message=message)


if __name__ == '__main__':
    views.run(debug=True, port=5002)
