from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
#import MySQLdb.cursors, re, hashlib
import pymysql
from hashlib import sha256
from global_profile import database_login_user
from json import dump
from query import db
import query

# In different environment, the usename of database and password may be
# different, you can specify your name, password and database in the
# database_login_user

# comment here
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = database_login_user.name
app.config['MYSQL_PASSWORD'] = database_login_user.password
app.config['MYSQL_DB'] = database_login_user.database
app.secret_key = 'hihi'

mysql = pymysql.connect(
    host = app.config['MYSQL_HOST'],
    user = app.config['MYSQL_USER'],
    password= app.config['MYSQL_PASSWORD'],
    db = app.config['MYSQL_DB']
)

# Functional check method
@app.route('/check_username', methods=['POST'])
def check_username():
    username = request.json['username']
    cursor = mysql.cursor()
    cursor.execute(query.checkUsername(), (username,))
    data = cursor.fetchone()
    if data:
        return {'is_taken': True}
    return {'is_taken': False}


# Page represent function
# Kinney route
@app.route('/vAdminHome')
# John app route
# @app.route('/pythonlogin/vAdminHome')
def vAdminHome():
     # Check if the user is logged in
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM Vender")
        data = cursor.fetchall()
        # User is loggedin show them the home page
        return render_template('vAdminHome.html', username=session['username'], data=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('admin_login'))

@app.route('/customer_page')
def customer_page():
     # Check if the user is logged in
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute(query.customerProducts(), (session['customer_name'],))
        # query.customerProducts(session['username'])
        # cursor.execute("SELECT * FROM Product WHERE  = %s", (session['id'],))
        data = cursor.fetchall()
        # User is loggedin show them the home page
        return render_template('customer_page.html', customer_name=session['customer_name'], data=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('loginOrRegister'))

# Kinney route
@app.route('/vAdmin', methods=['GET', 'POST'])
# John route
# @app.route('/pythonlogin/', methods=['GET', 'POST'])
def admin_login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        
        # TODO: Need to update the salt here
        password = sha256(str.encode(password + str(1))).hexdigest()

        # Check if account exists using MySQL
        cursor = mysql.cursor()#.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vadmin WHERE username = %s AND password = %s', (username, password))
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

@app.route('/')
def loginOrRegister():
    login_activate = ""
    register_activate = ""
    return render_template('index.html', login_activate=login_activate, register_activate=register_activate)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    login_activate = "active"
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # DONE: realising getting the user type(customer/vendor)
        login_type = request.form.get('usertype')

        # print(dump(request.form))

        print(request.form.get('usertype'))

        # TODO: Need to update the salt here
        password = sha256(str.encode(password + str(1))).hexdigest()

        # Check if account exists using MySQL
        cursor = mysql.cursor()#.connection.cursor(MySQLdb.cursors.DictCursor)

        # Detect which type of user is logging in
        if login_type == 'customer':
            cursor.execute('SELECT * FROM Customer WHERE username = %s AND password = %s', (username, password))
        elif login_type == 'vendor':
            cursor.execute('SELECT * FROM Vender WHERE vname = %s AND password = %s', (username, password))
        
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        # If account exists in accounts table in out database
        if account:
            session['loggedin'] = True
            if login_type == 'customer':
                session['customer_name'] = account[3]#['customer_name']
                return redirect(url_for('customer_page'))
            # Create session data, we can access this data in other routes
            elif login_type == 'vendor':
                session['vendor_name'] = account[1]#['vname']

            # session['id'] = account[0]#['id']
            # session['username'] = account[1]#['username']
            # Redirect to home page
            
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg, login_activate=login_activate, register_activate="")

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    register_activate = "active"
    if request.method == 'POST' and 'reg_username' in request.form and 'reg_password' in request.form:
        if request.form.get('reg_password') != request.form.get('reg_re_password'):
            msg = 'Fuck you, what you are fucking doing?'
        else:
            # TODO: Input the message into the database

            username = request.form['reg_username']
            password = request.form['reg_password']

            usertype = request.form.get('reg_usertype')

            password = sha256(str.encode(password + str(1))).hexdigest()

            # Check if account exists using MySQL
            cursor = mysql.cursor()#.connection.cursor(MySQLdb.cursors.DictCursor)

            # Detect which type of user is logging in
            if usertype == 'customer':
                cursor.execute('SELECT * FROM Customer WHERE username = %s AND password = %s', (username, password))
            elif usertype == 'vendor':
                cursor.execute(query.addVendor, (username, password))

            # Fetch one record and return result
            account = cursor.fetchone()
            print(account)
            # If account exists in accounts table in out database
            if account:
                session['loggedin'] = True
                if login_type == 'customer':
                    session['customer_name'] = account[3]#['customer_name']
                    return redirect(url_for('customer_page'))
                # Create session data, we can access this data in other routes
                elif login_type == 'vendor':
                    session['vendor_name'] = account[1]#['vname']

    # Show the login form with message (if any)
    return render_template('index.html', msg=msg, register_activate=register_activate, login_activate="")



if __name__ == '__main__':
    app.run(debug=True)