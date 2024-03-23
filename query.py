import pymysql
from global_profile import database_login_user
from hashlib import sha256

db = pymysql.connect(host='localhost',
                     user=database_login_user.name,
                     password=database_login_user.password,
                     database=database_login_user.database)
 


cursor = db.cursor()

# TODO: Change the following functions from in-function execute to return the sql string

def checkUsername():
    sql = '''
    SELECT * FROM Customer
    WHERE username = %s '''
    return sql

# Onboard new vendors onto the marketplace
def addVendor():
    # password = sha256(str.encode(password + str(salt))).hexdigest()
    sql = '''
    INSERT INTO Vendor(vname, geographic, password, salt)
    VALUES (%s,%s,%s,%s)
    '''
    return sql

def addCustomer():
    # password = sha256(str.encode(password + str(salt))).hexdigest()
    sql = '''
    INSERT INTO Customer(contactNumber, shippingDetail, username, password, salt)
    VALUES (%s,%s,%s,%s,%s)
    '''
    return sql

def customerProducts():
    sql = '''
    WITH TMP AS
        (SELECT Ordered.*, pname FROM Ordered INNER JOIN Product 
            ON Ordered.pid = Product.pid)

    SELECT TMP.*, username FROM TMP INNER JOIN Customer 
            ON TMP.cid = Customer.cid
            WHERE username = %s;
    '''
    # cursor.execute(sql,(cname,))
    return sql
# Browse all products offered by a specific vendor
#SELECT * FROM
#(SELECT * FROM Product, Vendor
#WHERE Product.vid = Vendor.vid)
#WHERE vname = ?
def browseAllProducts(vname):
    sql = '''
    WITH TMP AS 
        (SELECT * FROM Product, Vendor
        WHERE Product.vid = Vendor.vid)
    SELECT * FROM TMP
    WHERE vname = %s
    '''
    cursor.execute(sql,(vname,))
    db.commit()


# Introduce new products to a vendor's catalog
def addProduct(pname, price, vid, inventory):
    sql = '''
    INSERT INTO Product(pname, price, vid, inventory) 
    VALUES (%s,%s,%s,%s)
    '''
    cursor.execute(sql,(pname, price, vid, inventory))
    db.commit()
  


# Facilitate a search feature that allows users to discover products using tags, 
# the search should return products where the tag matches any part of the product's
# name or its associated tags
def searchProduct(tag):
    sql = '''
    SELECT * FROM Product
    WHERE pname LIKE '%%s%' OR tag1 = %s OR tag2 = %s OR tag3 = %s
    '''
    cursor.execute(sql,(tag,))
    db.commit()


# Customer Register
def register(contactNumber, shippingDetail, username, password, salt):
    password = sha256(str.encode(password + str(salt))).hexdigest()
    sql = '''
    INSERT INTO Customer(contactNumber, shippingDetail, username, password, salt)
    VALUES (%s,%s,%s,%s,%s)
    '''
    cursor.execute(sql,(contactNumber, shippingDetail, username, password, salt))
    db.commit()



# support product purchase. Record in database which customer purchases which product
def purchase(cid, pid, quantity, orderTime):
    orderStatus = 'order received'
    sql = '''
    INSERT INTO Ordered(cid, pid, quantity, orderStatus, orderTime)
    VALUES (%s,%s,%s,%s,%s)
    '''
    cursor.execute(sql,(cid, pid, quantity, orderStatus, orderTime))
    db.commit()
 


# cancellation of the entire order before it enters the shipping process
def cancelOrder(oid):
    sql = '''
    UPDATE Ordered
    SET orderStatus = 'cancelled'
    WHERE oid = %s
    '''
    cursor.execute(sql,(oid,))
    db.commit()



# the removal of specific products
def removeProduct(oid,pid):
    sql = '''
    DELETE FROM Ordered
    WHERE oid = %s AND pid = %s
    '''
    cursor.execute(sql, (oid,pid))
    db.commit()
