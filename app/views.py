import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import mysql.connector
from flask_hashing import Hashing
from mysql.connector import connect, Error
from datetime import datetime
from app import app
import app.connect as connect

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

@app.route("/")
@app.route("/community")
def home():
    return render_template("community.html")

  
@app.route('/community', methods=['GET', 'POST'])
def community():
    cursor, conn = getCursor(dictionary=True)
    print("Cursor obtained:", cursor)  # Debugging: Check if the cursor is correct
    if request.method == 'POST':
        print("Processing POST request")  # Debugging: Check if this is printed

        content = request.form['content']
        
        # Handle file upload
        file = request.files['media']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        
        # Insert the new message into the database
        cursor.execute("""
            INSERT INTO messages (user_id, title, content, created_at)
            VALUES (%s, %s, %s, %s)
        """, (1, 'New Message', content, datetime.now()))  # Temporary user_id for simplicity
        message_id = cursor.lastrowid

        if filename:
            cursor.execute("""
                INSERT INTO media (message_id, filename)
                VALUES (%s, %s)
            """, (message_id, filename))

        conn.commit()  # Use the 'conn' to commit changes
        flash('Message posted successfully!', 'success')
        return redirect(url_for('community'))

    # Fetch messages to display on the page
    cursor.execute("""
        SELECT messages.*, users.username, media.filename 
        FROM messages 
        JOIN users ON messages.user_id = users.user_id 
        LEFT JOIN media ON messages.message_id = media.message_id
        ORDER BY messages.created_at DESC
    """)
    messages = cursor.fetchall()

    print("Fetched messages:", messages)  # Debugging: Check fetched messages

    return render_template("community.html", messages=messages)





@app.route('/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    cursor, conn = getCursor()
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('community'))

    # Temporarily bypass login for message deletion
    # user_id = session.get('user_id')
    user_id = 1  # Hardcoded user_id for demonstration
    if not user_id:
        flash('Please login to delete your message.', 'error')
        return redirect(url_for('login'))

    cursor.execute("DELETE FROM replies WHERE message_id = %s", (message_id,))
    cursor.execute("DELETE FROM messages WHERE message_id = %s AND user_id = %s", (message_id, user_id))
    conn.commit()

    flash('Message deleted successfully!', 'success')
    return redirect(url_for('community'))


@app.route('/like_message/<int:message_id>', methods=['POST'])
def like_message(message_id):
    cursor, conn = getCursor()
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('community'))

    # Temporarily bypass login for liking a message
    # user_id = session.get('user_id')
    user_id = 1  # Hardcoded user_id for demonstration
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
    return redirect(url_for('community'))


@app.route('/dislike_message/<int:message_id>', methods=['POST'])
def dislike_message(message_id):
    cursor, conn = getCursor()
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('community'))

    # Temporarily bypass login for disliking a message
    # user_id = session.get('user_id')
    user_id = 1  # Hardcoded user_id for demonstration
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
    return redirect(url_for('community'))



#register
@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        user_password = request.form['password']
        
        cursor, conn = getCursor()
        if not cursor or not conn:
            flash('Database connection error', 'error')
            return render_template('index.html', msg='Database connection error')
        
        cursor.execute('SELECT user_id, username, password_hash, role FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account and hashing.check_value(account['password_hash'], user_password, PASSWORD_SALT):
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['username'] = account['username']
            session['role'] = account['role']
            
            if session['role'] == 'user':
                return redirect(url_for('user_home'))
            elif session['role'] == 'staff':
                return redirect(url_for('staff_home'))
            else:
                return redirect(url_for('admin_home'))
        else:
            msg = 'Incorrect username or password!'
    
    return render_template('index.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))


@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' in session:
        cursor, conn = getCursor()
        if not cursor or not conn:
            flash('Database connection error', 'error')
            return redirect(url_for('home'))

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM messages WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
        messages = cursor.fetchall()
        return render_template("profile.html", user=user, messages=messages)
    
    return redirect(url_for('login'))


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' in session:
        cursor, conn = getCursor()
        if not cursor or not conn:
            flash('Database connection error', 'error')
            return redirect(url_for('login'))

        if request.method == 'POST':
            email = request.form['email']
            birth_date = request.form['date_of_birth']
            location = request.form['location']
            file = request.files['profile_image']
            profile_image = None

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
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


@app.route('/members', methods=['GET', 'POST'])
def members():
    cursor, conn = getCursor()
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('home'))

    search_query = request.form.get('search', '').strip() if request.method == 'POST' else ''
    results = []
    message = ""

    if search_query:
        cursor.execute("""
            SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name 
            FROM users 
            WHERE (role = 'member') AND (first_name LIKE %s OR last_name LIKE %s) 
            ORDER BY first_name, last_name
        """, ('%' + search_query + '%', '%' + search_query + '%'))
        results = cursor.fetchall()
        if not results:
            message = f"Sorry, there are no results for '{search_query}'."

    cursor.execute("""
        SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name
        FROM users
        WHERE role = 'member'
        ORDER BY first_name, last_name
    """)
    members = cursor.fetchall()
    return render_template("members.html", results=results, members=members, message=message)


@app.route('/admins', methods=['GET', 'POST'])
def admins():
    cursor, conn = getCursor()
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('home'))

    search_query = request.form.get('search', '').strip() if request.method == 'POST' else ''
    results = []
    message = ""

    if search_query:
        cursor.execute("""
            SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name 
            FROM users 
            WHERE (role = 'admin') AND (first_name LIKE %s OR last_name LIKE %s) 
            ORDER BY first_name, last_name
        """, ('%' + search_query + '%', '%' + search_query + '%'))
        results = cursor.fetchall()
        if not results:
            message = f"Sorry, there are no results for '{search_query}'."

    cursor.execute("""
        SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name
        FROM users
        WHERE role = 'admin'
        ORDER BY first_name, last_name
    """)
    admins = cursor.fetchall()
    return render_template("admins.html", results=results, admins=admins, message=message)


@app.route('/moderators' , methods=['GET', 'POST'])
def moderators():
    cursor, conn = getCursor()
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('home'))

    search_query = request.form.get('search', '').strip() if request.method == 'POST' else ''
    results = []
    message = ""

    if search_query:
        cursor.execute("""
            SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name 
            FROM users 
            WHERE (role = 'moderator') AND (first_name LIKE %s OR last_name LIKE %s) 
            ORDER BY first_name, last_name
        """, ('%' + search_query + '%', '%' + search_query + '%'))
        results = cursor.fetchall()
        if not results:
            message = f"Sorry, there are no results for '{search_query}'."

    cursor.execute("""
        SELECT user_id, COALESCE(profile_image, '/static/assets/default.jpg') AS profile_image, first_name, last_name
        FROM users
        WHERE role = 'moderator'
        ORDER BY first_name, last_name
    """)
    moderators = cursor.fetchall()
    return render_template("moderators.html", results=results, moderators=moderators, message=message)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
