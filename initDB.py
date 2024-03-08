import pymysql

db = pymysql.connect(host='localhost',
                     user='test',
                     password='1234567890-=',
                     database='ecommerce')
 


cursor = db.cursor()
 

cursor.execute("DROP TABLE IF EXISTS Customer, Vender, Product, Ordered, vAdmin;")

sql_customer = '''
    CREATE TABLE Customer(
        cid INTEGER NOT NULL AUTO_INCREMENT,
        contactNumber INTEGER(8) NOT NULL,
        shipping CHAR(20) NOT NULL,
        PRIMARY KEY(cid)
    );
'''
sql_vender = '''
    CREATE TABLE Vender(
        vid INTEGER NOT NULL AUTO_INCREMENT,
        vname CHAR(20) NOT NULL,
        score INTEGER NOT NULL,
        geographic CHAR(20) NOT NULL,
        PRIMARY KEY(vid)
    );
'''
sql_product = '''
    CREATE TABLE Product(
        pid INTEGER NOT NULL AUTO_INCREMENT,
        pname CHAR(20) NOT NULL,
        price REAL NOT NULL,
        vid INTEGER NOT NULL,
        tag1 CHAR(20),
        tag2 CHAR(20),
        tag3 CHAR(20),
        PRIMARY KEY(pid),
        FOREIGN KEY(vid) REFERENCES Vender(vid) 
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
'''
sql_order = '''
    CREATE TABLE Ordered(
        oid INTEGER NOT NULL AUTO_INCREMENT,
        cid INTEGER NOT NULL,
        pid INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        orderStatus ENUM('deliverying', 'fulfilled', 'cancelled') NOT NULL,
        time Timestamp NOT NULL,
        PRIMARY KEY(oid),
        FOREIGN KEY(cid) REFERENCES Customer(cid),
        FOREIGN KEY(pid) REFERENCES Product(pid)
    );
'''
sql_vender_admin = '''
    CREATE TABLE vAdmin(
        id INTEGER NOT NULL AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL,
        password CHAR(255) NOT NULL,
        salt INTEGER NOT NULL,
        PRIMARY KEY(id)
    )
'''
try:
    cursor.execute(sql_customer)
    cursor.execute(sql_vender)
    cursor.execute(sql_product)
    cursor.execute(sql_order)
    cursor.execute(sql_vender_admin)
    print ('Table created')
except ValueError as e:
    print(e)


cursor.close()
db.close()



