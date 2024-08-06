from flask import Flask
from app.views import views

if __name__ == "__main__":
    views.run(debug=True)