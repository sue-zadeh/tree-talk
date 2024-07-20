from app import app

@app.route('/')
def index():
  return "<h1 style = 'color:blue'>Welcome to COMP639 Semester 2 2024</h1>"

@app.route('/about')
def about():
  return "<h1 style = 'color:red'>This is the About Page</h1>"