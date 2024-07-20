from flask import Flask

app = Flask(__name__)
app.secret_key = 'Example Secret Key (Change this!)'
from app import views
from app import admin_views
from app import staff_views
from loginapp import user
from loginapp import staff
from loginapp import admin