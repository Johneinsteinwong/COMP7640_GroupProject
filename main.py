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

@app.route('/product_update_data', methods=['POST'])
def product_update_data():
    pid = request.json['pid']
    price = request.json['price']
    # vid = request.json['vid']
    p_tag1 = request.json['p_tag1']
    p_tag2 = request.json['p_tag2']
    p_tag3 = request.json['p_tag3']
    inventory = request.json['inventory']
    cursor = mysql.cursor()
    cursor.execute(query.updateProduct(), (price, inventory, p_tag1, p_tag2, p_tag3, pid))
    mysql.commit()
    return {'success': True}

@app.route('/product_add_data', methods=['POST'])
def product_add_data():
    cursor = mysql.cursor()
    cursor.execute(query.browseVendorByVname(), (request.json['vname'],))
    vendor = cursor.fetchone()
    vid = vendor[0]
    pname = request.json['pname']
    price = request.json['price']
    # vid = session['vendor_id']
    p_tag1 = request.json['p_tag1']
    p_tag2 = request.json['p_tag2']
    p_tag3 = request.json['p_tag3']
    inventory = request.json['inventory']
    cursor = mysql.cursor()
    cursor.execute(query.addProduct(), (pname, price, vid, inventory, p_tag1, p_tag2, p_tag3, ''))
    mysql.commit()
    return {'success': True}

@app.route('/vendor_add_data', methods=['POST'])
def vendor_add_data():
    vname = request.json['vname']
    # password = request.json['password']
    geographic = request.json['vgeographic']
    vpassword = vname + '2024'
    password = sha256(str.encode(vpassword + str(1))).hexdigest()
    score = request.json['vscore']
    cursor = mysql.cursor()
    cursor.execute(query.addVendor(), (vname, score, geographic, password, '1'))
    mysql.commit()
    return {'success': True}

@app.route('/get_new_pid', methods=['POST'])
def get_new_pid():
    cursor = mysql.cursor()
    cursor.execute(query.getNewPid())
    data = cursor.fetchone()
    print(data)
    return {'pid': str(int(data[0]) + 1)}

@app.route('/get_new_vid', methods=['POST'])
def get_new_vid():
    cursor = mysql.cursor()
    cursor.execute(query.getNewVid())
    data = cursor.fetchone()
    print(data)
    return {'vid': str(int(data[0]) + 1)}

# @app.route('/product_delete_data', methods=['POST'])


# @app.route('/add_product', methods=['POST'])
# def add_product():
#     pname = request.json['pname']
#     price = request.json['price']
#     vid = request.json['vid']
#     inventory = request.json['inventory']
#     cursor = mysql.cursor()
#     cursor.execute(query.addProduct(), (pname, price, vid, inventory))
#     mysql.commit()
#     return {'success': True}

@app.route('/search_product', methods=['GET', 'POST'])
def search_product():
    pname = request.form['search_info']
    # pname = request.json['search_info']
    # print(pname)
    search_info = '%' + pname + '%'
    # print(search_info)
    # mysql.connect()
    cursor = mysql.cursor()

    exe_str = cursor.mogrify(query.searchProductByNameAndTag(), (search_info, search_info, search_info, search_info))
    # print(exe_str)
    cursor.execute(exe_str)
    data = cursor.fetchall()
    datalist = list(data)

    # exe_str = cursor.mogrify(query.searchProductByName(), (search_info,))
    # print(exe_str)
    # cursor.execute(exe_str)
    # data = cursor.fetchall()
    # datalist = list(data)

    # exe_tag_str = cursor.mogrify(query.searchProductByTag(), (search_info, search_info, search_info,))
    # data = cursor.execute(exe_tag_str)
    # tag_data = cursor.fetchall()
    # datalist += list(tag_data)

    hint_word = set_hint_word()
    customer_name = set_customer_name()
    # print(data)
    return render_template('products.html', data=datalist, hint_word=hint_word, customer_name=customer_name)


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

@app.route('/customer_page/<customer_id>')
def customer_page(customer_id):
     # Check if the user is logged in
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute(query.browseAllProductsByCustomer(), (session['customer_name'],))
        data = cursor.fetchall()
        # User is loggedin show them the home page
        return render_template('customer_page.html', customer_name=session['customer_name'], data=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('loginOrRegister'))

@app.route('/vendor_page/<vendor_id>')
def vendor_page(vendor_id):
    if 'loggedin' in session:
        # cursor = mysql.cursor()
        # cursor.execute(query.browseAllProductsByVendor(), (session['vendor_name'],))
        # data = cursor.fetchall()
        # print(session['vendor_score'])
        hint_word = set_hint_word_vendor()
        
        cursor = mysql.cursor()
        cursor.execute(query.browseVendorByVid(), (vendor_id,))
        data = cursor.fetchone()

        return render_template('vendor_page.html', vendor_id=vendor_id ,vendor_name=data[1], vendor_score=data[2], vendor_geographic=data[3], hint_word=hint_word)
    return redirect(url_for('loginOrRegister'))

@app.route('/admin_page')
def admin_page():
    if 'loggedin' in session:
        # cursor = mysql.cursor()
        # cursor.execute(query.browseAllProducts())
        # data = cursor.fetchall()
        return render_template('admin_page.html', admin_name=session['admin_name'], admin_id=session['admin_id'])
    return redirect(url_for('loginOrRegister'))

@app.route('/v_p_list/<vendor_id>')
def v_p_list(vendor_id):
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute(query.browseVendorByVid(), (vendor_id,))
        vendor = cursor.fetchone()
        vendor_name = vendor[1]
        cursor.execute(query.browseAllProductsByVendor(), (vendor_name,))
        data = cursor.fetchall()
        hint_word = set_hint_word()
        return render_template('vendor_product_list.html', products=data, hint_word=hint_word, vendor_name=vendor_name)
    return redirect(url_for('login'))
    # return render_template('vendor_product_list.html')

@app.route('/vendor_list')
def vendor_list():
    if 'loggedin' in session:
        cursor = mysql.cursor()
        cursor.execute(query.browseAllVendors())
        data = cursor.fetchall()
        return render_template('vendor_list.html', vendors=data, admin_name=session['admin_name'])
    return redirect(url_for('login'))

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
    login_activate = "active"
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
            cursor.execute('SELECT * FROM Vendor WHERE vname = %s AND password = %s', (username, password))
        elif login_type == 'admin':
            cursor.execute('SELECT * FROM vAdmin WHERE username = %s AND password = %s', (username, password))
        
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        # If account exists in accounts table in out database
        if account:
            session['loggedin'] = True
            if login_type == 'customer':
                session['customer_name'] = account[3]#['customer_name']
                return redirect(url_for('products'))
            # Create session data, we can access this data in other routes
            elif login_type == 'vendor':
                session['vendor_id'] = account[0]#['vid']
                session['vendor_name'] = account[1]#['vname']
                session['vendor_score'] = account[2]#['score']
                session['vendor_geographic'] = account[3]#['geographic']
                # print('Here')
                return redirect(url_for('vendor_page', vendor_id=account[0]))
            elif login_type == 'admin':
                session['admin_id'] = account[0]#['id']
                session['admin_name'] = account[1]#['username']
                return redirect(url_for('admin_page'))
            # session['id'] = account[0]#['id']
            # session['username'] = account[1]#['username']
            # Redirect to home page
            
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg, login_activate=login_activate, register_activate="")

def set_hint_word():
    if 'customer_name' not in session or session['customer_name'] == '':
        return 'Please login first!'
    else:
        return 'Welcome back,'

def set_hint_word_vendor():
    if 'vendor_name' not in session or session['vendor_name'] == '':
        return 'Please login first!'
    else:
        return 'Welcome back,'

def set_customer_name():
    if 'customer_name' not in session or session['customer_name'] == '':
        return ''
    else:
        return session['customer_name']

@app.route('/products', methods=['GET', 'POST'])
def products():
    mysql.connect()
    cursor = mysql.cursor()
    cursor.execute(query.browseAllProducts())
    mysql.commit()
    data = cursor.fetchall()
    hint_word = set_hint_word()
    customer_name = set_customer_name()

    return render_template('products.html', data=data, hint_word=hint_word, customer_name=customer_name)

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
            phone = request.form['reg_phone']
            loc = request.form['reg_loc']

            usertype = request.form.get('reg_usertype')

            password = sha256(str.encode(password + str(1))).hexdigest()

            # Check if account exists using MySQL
            cursor = mysql.cursor()#.connection.cursor(MySQLdb.cursors.DictCursor)

            # Detect which type of user is logging in
            if usertype == 'customer':
                cursor.execute(query.addCustomer(), (phone, loc, username, password, '1'))
                mysql.commit()
            elif usertype == 'vendor':
                cursor.execute(query.addVendor(), (username, loc, password, '1'))
                mysql.commit()
            msg = 'Congras! Now you are one of the user'
            # # Fetch one record and return result
            # account = cursor.fetchone()
            # print(account)
            # # If account exists in accounts table in out database
            # if account:
            #     session['loggedin'] = True
            #     if login_type == 'customer':
            #         session['customer_name'] = account[3]#['customer_name']
            #         return redirect(url_for('customer_page'))
            #     # Create session data, we can access this data in other routes
            #     elif login_type == 'vendor':
            #         session['vendor_name'] = account[1]#['vname']

    # Show the login form with message (if any)
    return render_template('index.html', msg=msg, register_activate=register_activate, login_activate="")



if __name__ == '__main__':
    app.run(debug=True)