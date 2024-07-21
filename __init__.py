from flask import Flask

app = Flask(__name__)
import app.views
# from app import views
# from app import admin
# from app import staff
# from app import admin_views
# from app import staff_views
# # from loginapp import user
# # from loginapp import staff
# # from loginapp import admin

if __name__ == "__main__":
  app.run(debug=True)