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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ------ members, moderators, admins
def redirect_based_on_role(html_file):
    if "member" in session:
        return redirect(url_for("member"))
    elif "moderator" in session:
        return redirect(url_for("moderator"))
    elif "admin" in session:
        return redirect(url_for("admin"))
    else:
        return render_template(html_file)
    
def choosing_role():
    if "member" in session:
        return session["member"]
    elif "moderator" in session:
        return session["moderator"]
    elif "admin" in session:
        return session["admin"]

def render_login_or_register(registered, toLogin, msg, username):
    if toLogin:
        return render_template('login.html', msg=msg, toLogin=toLogin, registered=registered, username=username) 
    else:
        return render_template("register.html", msg=msg, toLogin=toLogin)
#-- home page
@app.route("/")
def home():
   return render_template("index.html")


   

@app.route('/profile', methods=['GET'])
def profile():
    if 'user' in session:
        cursor, conn = getCursor(dictionary=True)
        if not cursor or not conn:
            flash('Database connection error', 'error')
            return redirect(url_for('community'))

        cursor.execute("SELECT * FROM users WHERE username = %s", (session['user'],))
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM messages WHERE user_id = %s ORDER BY created_at DESC", (user['user_id'],))
        messages = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template("profile.html", user=user, messages=messages)
    
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' in session:
        cursor, conn = getCursor(dictionary=True)
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
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_image = filename

            cursor.execute("""
                UPDATE users SET email = %s, birth_date = %s, location = %s, profile_image = %s WHERE username = %s
            """, (email, birth_date, location, profile_image, session['user']))
            conn.commit()
            
            cursor.close()
            conn.close()

            flash('Profile updated successfully!', 'success')
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (session['user'],))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('edit_profile.html', user=user)
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
