from flask import Flask
# from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'ffbdec42bf94eaefd93ed692f13af3f6'

# Default configurations
app.config['UPLOAD_FOLDER'] = 'app/static/uploads' # Folder to store uploaded images

# Utility function to check file extensions
def allowed_file(filename):
     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def register_routes():
    from app import views  # Import all routes from views.py

register_routes()

if __name__ == "__main__":
    app.run(debug=True, port=5001)