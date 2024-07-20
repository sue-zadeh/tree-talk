from flask import Flask, redirect, url_for, render_template,request, session


app = Flask(__name__)
app.secret_key = 'Example Secret Key (i should take it from a config file)'

@app.route('/')
def home():
  return render_template('index.html')
 
@app.route("/login", methods = ['GET', 'POST'])
def login():
  if request.method == 'POST':
    user = request.form['nm']
    userRole = request.form['rl']
    session['user'] = user   #Set the session's user
    session['role'] = userRole #Set the session's role
    return redirect(url_for('user')) #Redirect to the user page
  else:
    if "user" in  session:
      return redirect(url_for('user'))
    
      return render_template('login.html')
 #user   
@app.route("/user")
def user():
  if "user" in session:
    user = session["user"]
    userRole = session["role"]
    return f"<h1>{user}</h1>{user} {userRole}</h1>"
  else:
    return redirect(url_for('login'))
  #staff   
@app.route("/staff")
def staff():
  if "user" in session:
    if session["role"] == "staff":   # check the role of the user
      return render_template('staff.html')
    else:
      return "Illegal Access"      # anyone else other than staff
  else:
    return redirect(url_for('login'))
  
  #admin
  @app.route("/admin")
  def admin():
    if "user" in session:
      if session["role"] == "admin":   # check the role of the user
        return render_template('admin.html')
      else:
        return "Illegal Access"      # anyone else other than staff
    else:
      return redirect(url_for('login'))
    
  @app.route("/logout") 
  def logout():
    session.pop('user', None)  #session is cleared at logout
    session.pop('role', None)
    return redirect(url_for('login'))
    
    
if __name__ == '__main__':
      app.run(debug = True)