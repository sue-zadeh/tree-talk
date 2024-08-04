from flask import Flask
from backend.views import app

if __name__ == "__main__":
    app.run(debug=True)