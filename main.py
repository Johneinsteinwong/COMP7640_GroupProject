from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
#import MySQLdb.cursors, re, hashlib
import pymysql
from hashlib import sha256


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = '1234567890-='
app.config['MYSQL_DB'] = 'ecommerce'
app.secret_key = 'hihi'

mysql = pymysql.connect(
    host = app.config['MYSQL_HOST'],
    user = app.config['MYSQL_USER'],
    password= app.config['MYSQL_PASSWORD'],
    db = app.config['MYSQL_DB']
)

@app.route('/pythonlogin/vAdminHome')
def vAdminHome():
     # Check if the user is logged in
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM Vender")
        data = cursor.fetchall()
        # User is loggedin show them the home page
        return render_template('vAdminHome.html', username=session['username'], data=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        password = sha256(str.encode(password + str(1))).hexdigest()
        # Check if account exists using MySQL
        cursor = mysql.cursor()#.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vadmin WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]#['id']
            session['username'] = account[1]#['username']
            # Redirect to home page
            return redirect(url_for('vAdminHome'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('vAdmin.html', msg=msg)



if __name__ == '__main__':
    app.run(debug=True)