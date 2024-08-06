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

PASSWORD_SALT = '1234abcd'

hashing = Hashing(app)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

#moderators
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