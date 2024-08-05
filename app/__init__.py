from flask import Flask

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'

app.secret_key = 'e2e62cdb171271f0b12e5043f9f84208eba1f05c8658704e'

from app import views     # Import all routes from views.py
from app import logintest 
if __name__ == '__main__':
    app.run(debug=True, port=5000)
 
    
# app = Flask(__name__)
# app.secret_key = 'Example Secret Key (Change this!)'

# from loginapp import user
# from loginapp import staff
# from loginapp import admin
