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


# Uncomment when login is working
# @app.before_request
# def require_login():
#     if 'user_id' not in session and request.endpoint not in ['login', 'register']:
#         return redirect(url_for('login'))


   #---uploading pictures
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


   #--- role of user
def redirect_based_on_role(html_file):
    if "user" in session:
        return redirect(url_for("user"))
    elif "moderator" in session:
        return redirect(url_for("moderator"))
    elif "admin" in session:
        return redirect(url_for("admin"))
    else:
        return render_template(html_file)
    
def choosing_role():
    if "user" in session:
        return session["user"]
    elif "moderator" in session:
        return session["moderator"]
    elif "admin" in session:
        return session["admin"]

def render_login_or_register(registered, toLogin, msg, username):
    if toLogin:
        return render_template('login.html', msg=msg, toLogin=toLogin, registered=registered, username=username) 
    else:
        return render_template("register.html", msg=msg, toLogin=toLogin)


#-----community center - sending message and reply

@app.route('/community', methods=['GET', 'POST'])
def community():
    cursor, conn = getCursor(dictionary=True)
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        content = request.form['content']
        file = request.files['media']
        filepath = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = filename

        cursor.execute("""
            INSERT INTO messages (user_id, content, created_at, filepath)
            VALUES (%s, %s, %s, %s)
        """, (session.get('user_id'), content, datetime.now(), filepath))
        conn.commit()
        return redirect(url_for('community'))

    cursor.execute("""
        SELECT m.*, u.username
        FROM messages m
        JOIN users u ON m.user_id = u.user_id
        ORDER BY m.created_at DESC
    """)
    messages = cursor.fetchall()

    for message in messages:
        cursor.execute("""
            SELECT r.reply_id, r.content, r.created_at, u.username 
            FROM replies r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.message_id = %s
            ORDER BY r.created_at ASC
        """, (message['message_id'],))
        message['replies'] = cursor.fetchall()

    return render_template("community.html", messages=messages)

@app.route('/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    cursor, conn = getCursor(dictionary=True)
    user_id = session.get('user_id', 1)
    cursor.execute("DELETE FROM replies WHERE message_id = %s", (message_id,))
    cursor.execute("DELETE FROM messages WHERE message_id = %s AND user_id = %s", (message_id, user_id))
    conn.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('community'))

@app.route('/edit_message/<int:message_id>', methods=['POST'])
def edit_message(message_id):
    cursor, conn = getCursor(dictionary=True)
    content = request.form['content']
    cursor.execute("""
        UPDATE messages SET content = %s WHERE message_id = %s
    """, (content, message_id))
    conn.commit()
    flash('Message updated successfully!', 'success')
    return redirect(url_for('community'))

@app.route('/like_message/<int:message_id>', methods=['POST'])
def like_message(message_id):
    cursor, conn = getCursor()
    user_id = session.get('user_id', 1)

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
    user_id = session.get('user_id', 1)

    cursor.execute("SELECT * FROM likes WHERE user_id = %s AND message_id = %s", (user_id, message_id))
    like = cursor.fetchone()

    if like:
        cursor.execute("DELETE FROM likes WHERE like_id = %s", (like['like_id'],))
    else:
        cursor.execute("INSERT INTO likes (user_id, message_id, type) VALUES (%s, %s, %s)", (user_id, message_id, 'dislike'))

    conn.commit()
    return redirect(url_for('community'))

@app.route('/post_reply/<int:message_id>', methods=['POST'])
def post_reply(message_id):
    cursor, conn = getCursor(dictionary=True)
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('community'))

    content = request.form['content']
    user_id = session.get('user_id', 1)

    cursor.execute("""
        INSERT INTO replies (message_id, user_id, content, created_at)
        VALUES (%s, %s, %s, %s)
    """, (message_id, user_id, content, datetime.now()))
    conn.commit()

    flash('Reply posted successfully!', 'success')
    return redirect(url_for('community'))

@app.route('/like_reply/<int:reply_id>', methods=['POST'])
def like_reply(reply_id):
    cursor, conn = getCursor()
    user_id = session.get('user_id', 1)

    cursor.execute("SELECT * FROM likes WHERE user_id = %s AND reply_id = %s", (user_id, reply_id))
    like = cursor.fetchone()

    if like:
        cursor.execute("DELETE FROM likes WHERE like_id = %s", (like['like_id'],))
    else:
        cursor.execute("INSERT INTO likes (user_id, reply_id, type) VALUES (%s, %s, %s)", (user_id, reply_id, 'like'))

    conn.commit()
    return redirect(url_for('community'))

@app.route('/dislike_reply/<int:reply_id>', methods=['POST'])
def dislike_reply(reply_id):
    cursor, conn = getCursor()
    user_id = session.get('user_id', 1)

    cursor.execute("SELECT * FROM likes WHERE user_id = %s AND reply_id = %s", (user_id, reply_id))
    like = cursor.fetchone()

    if like:
        cursor.execute("DELETE FROM likes WHERE like_id = %s", (like['like_id'],))
    else:
        cursor.execute("INSERT INTO likes (user_id, reply_id, type) VALUES (%s, %s, %s)", (user_id, reply_id, 'dislike'))

    conn.commit()
    return redirect(url_for('community'))


@app.route('/edit_reply/<int:reply_id>', methods=['POST'])
def edit_reply(reply_id):
    cursor, conn = getCursor(dictionary=True)
    content = request.form['content']
    cursor.execute("""
        UPDATE replies SET content = %s WHERE reply_id = %s
    """, (content, reply_id))
    conn.commit()
    flash('Reply updated successfully!', 'success')
    return redirect(url_for('community'))

@app.route('/delete_reply/<int:reply_id>', methods=['POST'])
def delete_reply(reply_id):
    cursor, conn = getCursor()
    user_id = session.get('user_id', 1)
    cursor.execute("DELETE FROM replies WHERE reply_id = %s AND user_id = %s", (reply_id, user_id))
    conn.commit()
    flash('Reply deleted successfully!', 'success')
    return redirect(url_for('community'))
  

if __name__ == '__main__':
    app.run(debug=True)
    