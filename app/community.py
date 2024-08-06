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
    
    if request.method == 'POST':
        content = request.form['content']
        file = request.files['media']
        filename = None
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor.execute("""
            INSERT INTO messages (user_id, title, content, created_at)
            VALUES (%s, %s, %s, %s)
        """, (session.get('user_id', 1), 'New Message', content, datetime.now()))
        
        message_id = cursor.lastrowid

        if filename:
            cursor.execute("""
                INSERT INTO media (message_id, filename)
                VALUES (%s, %s)
            """, (message_id, filename))

        conn.commit()
        flash('Message posted successfully!', 'success')
        return redirect(url_for('community'))

    cursor.execute("""
        SELECT m.message_id, m.content, m.created_at, u.username, media.filename 
        FROM messages m
        JOIN users u ON m.user_id = u.user_id
        LEFT JOIN media ON m.message_id = media.message_id
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

    cursor.close()
    conn.close()

    return render_template("community.html", messages=messages)



@app.route('/edit_message/<int:message_id>', methods=['GET', 'POST'])
def edit_message(message_id):
    cursor, conn = getCursor(dictionary=True)

    if request.method == 'POST':
        content = request.form['content']
        cursor.execute("""
            UPDATE messages SET content = %s WHERE message_id = %s
        """, (content, message_id))
        conn.commit()
        flash('Message updated successfully!', 'success')
        return redirect(url_for('community'))

    cursor.execute("SELECT * FROM messages WHERE message_id = %s", (message_id,))
    message = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit_message.html", message=message)

@app.route('/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    cursor, conn = getCursor()

    user_id = session.get('user_id', 1)
    cursor.execute("DELETE FROM replies WHERE message_id = %s", (message_id,))
    cursor.execute("DELETE FROM messages WHERE message_id = %s AND user_id = %s", (message_id, user_id))
    
    conn.commit()
    flash('Message deleted successfully!', 'success')
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
    user_id = session.get('user_id', 1)  # Replace with actual user session handling

    cursor.execute("""
        INSERT INTO replies (message_id, user_id, content, created_at)
        VALUES (%s, %s, %s, %s)
    """, (message_id, user_id, content, datetime.now()))
    conn.commit()

    flash('Reply posted successfully!', 'success')
    return redirect(url_for('community'))


@app.route('/edit_reply/<int:reply_id>', methods=['GET', 'POST'])
def edit_reply(reply_id):
    cursor, conn = getCursor(dictionary=True)

    if request.method == 'POST':
        content = request.form['content']
        cursor.execute("""
            UPDATE replies SET content = %s WHERE reply_id = %s
        """, (content, reply_id))
        conn.commit()
        flash('Reply updated successfully!', 'success')
        return redirect(url_for('community'))

    cursor.execute("SELECT * FROM replies WHERE reply_id = %s", (reply_id,))
    reply = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit_reply.html", reply=reply)

@app.route('/delete_reply/<int:reply_id>', methods=['POST'])
def delete_reply(reply_id):
    cursor, conn = getCursor()
    
    user_id = session.get('user_id', 1)
    cursor.execute("DELETE FROM replies WHERE reply_id = %s AND user_id = %s", (reply_id, user_id))
    
    conn.commit()
    flash('Reply deleted successfully!', 'success')
    return redirect(url_for('community'))