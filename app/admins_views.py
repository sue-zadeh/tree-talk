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

def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @views.route('/admin/dashboard')
# def admin_dashboard():
#   return "Admin Dashboard"

# @views.route('/admin/profile')
# def admin_profile():
#   return "Admin Profile

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
            SELECT user_id, COALESCE(profile_image, '/static/assets/default.png') AS profile_image, first_name, last_name, role
            FROM users 
            WHERE first_name LIKE %s OR last_name LIKE %s 
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

@app.route('/change_role/<int:user_id>', methods=['POST'])
def change_role(user_id):
    new_role = request.form.get('role')
    
    cursor, conn = getCursor()
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('admins'))

    try:
        cursor.execute("""
            UPDATE users
            SET role = %s
            WHERE user_id = %s
        """, (new_role, user_id))
        conn.commit()
        flash('User role updated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash('Failed to update user role.', 'error')
    
    return redirect(url_for('admins'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)