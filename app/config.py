from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'ffbdec42bf94eaefd93ed692f13af3f6'
    
    # Default configurations
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
    
    return app
