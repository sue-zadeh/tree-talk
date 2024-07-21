from flask import render_template, redirect, url_for, request, session
from app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        userRole = request.form['rl']
        session['user'] = user  # Set the session's user
        session['role'] = userRole  # Set the session's role
        return redirect(url_for('user'))  # Redirect to the user page
    else:
        if "user" in session:
            return redirect(url_for('user'))
        return render_template('login.html')

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        userRole = session["role"]
        return f"<h1>{user}</h1>{user} {userRole}</h1>"
    else:
        return redirect(url_for('login'))

@app.route("/staff")
def staff():
    if "user" in session:
        if session["role"] == "staff":  # Check the role of the user
            return render_template('staff.html')
        else:
            return "Illegal Access"  # Anyone else other than staff
    else:
        return redirect(url_for('login'))

@app.route("/admin")
def admin():
    if "user" in session:
        if session["role"] == "admin":  # Check the role of the user
            return render_template('admin.html')
        else:
            return "Illegal Access"  # Anyone else other than admin
    else:
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('user', None)  # Session is cleared at logout
    session.pop('role', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
