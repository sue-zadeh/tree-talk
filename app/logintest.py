from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configurations
dbuser = "root" #PUT YOUR MySQL username here - usually root
dbpass = "123Suezx." #PUT YOUR PASSWORD HERE
dbhost = "localhost"
dbport = "3306"
dbname = "TreeTalk"

mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM users WHERE username=%s AND password=%s ''', (username, password))
        account = cursor.fetchone()
        
        if account:
            flash('Logged in successfully!', 'success')
            return redirect(url_for('community'))
        else:
            flash('Incorrect username/password!', 'danger')
    
    return render_template('login.html')

if __name__ == "__main__":
    app.run()
