from app.config import create_app

app = create_app()

with app.app_context():
    from app import views  # Import all routes from views.py

if __name__ == "__main__":
    app.run(debug=True, port=5001)
