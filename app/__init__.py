from flask import Flask

app = Flask(__name__)

# Default configurations
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.secret_key = 'ExampleSecretKey'

def register_routes():
    from app import views
    from app import admin_views
    from app import staff_views
    from app import user
    from app import admin
    from app import staff
    from app import connect

register_routes()

if __name__ == "__main__":
    app.run(debug=True)
