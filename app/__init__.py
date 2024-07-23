from flask import Flask

app = Flask(__name__)
app.secret_key = 'YourSecretKeyHere'

# Default configurations
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

def register_routes():
    from app import views  # Import all routes from views.py

register_routes()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
