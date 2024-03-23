import pymysql
from global_profile import database_login_user
import query

db = pymysql.connect(host='localhost',
                     user=database_login_user.name,
                     password=database_login_user.password,
                     database=database_login_user.database)
 


cursor = db.cursor()
 

cursor.execute("DROP TABLE IF EXISTS Customer, Vendor, Product, Ordered, vAdmin;")

sql_customer = '''
    CREATE TABLE Customer(
        cid INTEGER NOT NULL AUTO_INCREMENT,
        contactNumber INTEGER(8) NOT NULL,
        shippingDetail CHAR(20) NOT NULL,
        username VARCHAR(50) NOT NULL,
        password CHAR(255) NOT NULL,
        salt INTEGER NOT NULL,
        PRIMARY KEY(cid)
    );
'''
sql_Vendor = '''
    CREATE TABLE Vendor(
        vid INTEGER NOT NULL AUTO_INCREMENT,
        vname CHAR(20) NOT NULL,
        score INTEGER,
        geographic CHAR(20) NOT NULL,
        password CHAR(255) NOT NULL,
        salt INTEGER NOT NULL,
        PRIMARY KEY(vid)
    );
'''
sql_product = '''
    CREATE TABLE Product(
        pid INTEGER NOT NULL AUTO_INCREMENT,
        pname CHAR(20) NOT NULL,
        price REAL NOT NULL,
        vid INTEGER NOT NULL,
        inventory INTEGER NOT NULL,
        tag1 CHAR(20),
        tag2 CHAR(20),
        tag3 CHAR(20),
        PRIMARY KEY(pid),
        FOREIGN KEY(vid) REFERENCES Vendor(vid) 
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
        orderStatus ENUM('order received', 'shipping', 'fulfilled', 'cancelled') NOT NULL,
        orderTime Timestamp NOT NULL,
        PRIMARY KEY(oid, cid, pid),
        FOREIGN KEY(cid) REFERENCES Customer(cid),
        FOREIGN KEY(pid) REFERENCES Product(pid)
    );
'''
sql_Vendor_admin = '''
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
    cursor.execute(sql_Vendor)
    cursor.execute(sql_product)
    cursor.execute(sql_order)
    cursor.execute(sql_Vendor_admin)
    print ('Table created')

    cursor.execute(query.addVendor(), ('V001', 'Apple', 'apple2024', 4.9, 'California, USA',))
    cursor.execute(query.addVendor(), ('V002', 'Samsung', 'samsung2024', 4.8, 'Seoul, Korea'))
    cursor.execute(query.addVendor(), ('V003', 'Xiaomi', 'xiaomi2024', 4.7, 'Beijing, China'))
    cursor.execute(query.addVendor(), ('V004', 'Huawei', 'huawei2024', 4.6, 'Shenzhen, China'))
    cursor.execute(query.addProduct(), ('P001', 'iPhone 13', 999.99, 'V001', 100, 'smartphone', 'apple', 'ios'))
    cursor.execute(query.addProduct(), ('P002', 'Galaxy S21', 899.99, 'V002', 100, 'smartphone', 'samsung', 'android'))
    cursor.execute(query.addProduct(), ('P003', 'Mi 11', 799.99, 'V003', 100, 'smartphone', 'xiaomi', 'android'))
    cursor.execute(query.addProduct(), ('P004', 'P50', 699.99, 'V004', 100, 'smartphone', 'huawei', 'android'))
    cursor.execute(query.addProduct(), ('P005', 'MacBook Pro', 1999.99, 'V001', 100, 'laptop', 'apple', 'macos'))
    cursor.execute(query.addProduct(), ('P006', 'Galaxy Book Pro', 1799.99, 'V002', 100, 'laptop', 'samsung', 'windows'))
    cursor.execute(query.addProduct(), ('P007', 'Mi Notebook Pro', 1599.99, 'V003', 100, 'laptop', 'xiaomi', 'windows'))
    cursor.execute(query.addProduct(), ('P008', 'MateBook X Pro', 1499.99, 'V004', 100, 'laptop', 'huawei', 'windows'))
    cursor.execute(query.addProduct(), ('P009', 'AirPods Pro', 199.99, 'V001', 100, 'earphone', 'apple', 'ios'))
    cursor.execute(query.addProduct(), ('P010', 'Galaxy Buds Pro', 179.99, 'V002', 100, 'earphone', 'samsung', 'android'))
    cursor.execute(query.addProduct(), ('P011', 'Mi True Wireless Earbuds', 159.99, 'V003', 100, 'earphone', 'xiaomi', 'android'))
    cursor.execute(query.addProduct(), ('P012', 'FreeBuds 4', 139.99, 'V004', 100, 'earphone', 'huawei', 'android'))
    cursor.execute(query.addProduct(), ('P013', 'iPad Pro', 799.99, 'V001', 100, 'tablet', 'apple', 'ios'))
    db.commit()
except ValueError as e:
    print(e)


cursor.close()
db.close()




