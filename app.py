from flask import Flask
from app.views import views

app = Flask(__name__)


if __name__ == "__main__":
    views.run(debug=True)