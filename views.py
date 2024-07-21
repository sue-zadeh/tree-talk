from flask import render_template, redirect, url_for, session
from app import app

@app.route('/')
@app.route('/login/')
def login():
    # Login view code here
    pass

@app.route('/register')
def register():
    # Register view code here
    pass

