
from flask import Flask

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'

app.secret_key = 'ffbdec42bf94eaefd93ed692f13af3f6'  

from app import views # Import all routes from views.py
   
    
# from flask import Flask

# app = Flask(__name__)
# app.secret_key = 'Example Secret Key (Change this!)'

# from loginapp import user
# from loginapp import staff
# from loginapp import admin
