# import os
# import re
# from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
# from werkzeug.utils import secure_filename
# import mysql.connector
# from flask_hashing import Hashing
# from mysql.connector import connect, Error
# from datetime import datetime
# from app import app
# import app.connect as connect


# app.secret_key = 'e2e62cdb171271f0b12e5043f9f84208eba1f05c8658704e'
# PASSWORD_SALT = 'abcd'
# app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Configuring the upload folder

# hashing = Hashing(app)

# db_connection = None

# def getCursor(dictionary=False, buffered=False):
#     global db_connection

#     try:
#         if db_connection is None or not db_connection.is_connected():
#             db_connection = mysql.connector.connect(
#                 user=connect.dbuser,
#                 password=connect.dbpass,
#                 host=connect.dbhost,
#                 database=connect.dbname,
#                 auth_plugin='mysql_native_password',
#                 autocommit=True
#             )
#             print("Connection successful")

#         cursor = db_connection.cursor(dictionary=dictionary, buffered=buffered)
#         return cursor, db_connection

#     except mysql.connector.Error as e:
#         print("Error while connecting to MySQL", e)
#         return None, None

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
  
  
#   ##========login
  
#   @app.routes('/login')