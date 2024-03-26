import pymysql
from global_profile import database_login_user
from hashlib import sha256

db = pymysql.connect(host='localhost',
                     user=database_login_user.name,
                     password=database_login_user.password,
                     database=database_login_user.database)
 


cursor = db.cursor()

# TODO: Change the following functions from in-function execute to return the sql string

# Check class function
def checkUsername():
    sql = '''
    SELECT * FROM Customer
    WHERE username = %s '''
    return sql

def browseAllProducts():
    sql = '''
    SELECT * FROM Product
    '''
    return sql

# Browse all products offered by a specific vendor
def browseAllProductsByVendor():
    sql = '''
    WITH TMP AS 
        (SELECT Product.*, Vendor.vname FROM Product, Vendor
        WHERE Product.vid = Vendor.vid)
    SELECT * FROM TMP
    WHERE vname = %s
    '''
    # cursor.execute(sql,(vname,))
    return sql

def browseAllProductsByCustomer():
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

def getVid():
    sql = '''
    SELECT vid FROM Vendor
    WHERE vname = %s
    '''
    return sql
# Check class function end
# =================================================================================================

# Update class function
# Onboard new vendors onto the marketplace
def addVendor():
    # password = sha256(str.encode(password + str(salt))).hexdigest()
    sql = '''
    INSERT INTO Vendor(vname, score, geographic, password, salt)
    VALUES (%s,%s,%s,%s,%s)
    '''
    return sql

def addCustomer():
    # password = sha256(str.encode(password + str(salt))).hexdigest()
    sql = '''
    INSERT INTO Customer(contactNumber, shippingDetail, username, password, salt)
    VALUES (%s,%s,%s,%s,%s)
    '''
    return sql

# Introduce new products to a vendor's catalog
def addProduct():
    sql = '''
    INSERT INTO Product(pname, price, vid, inventory, tag1, tag2, tag3, url) 
    VALUES (%s,%s,%s,%s, %s, %s, %s, %s)
    '''
    return sql
# Update class function end
# =================================================================================================



# Facilitate a search feature that allows users to discover products using tags, 
# the search should return products where the tag matches any part of the product's
# name or its associated tags
def searchProductByName():
    sql = '''
    SELECT * FROM Product WHERE pname LIKE %s
    '''
    # print(sql)
    return sql

def searchProductByTag():
    sql = '''
    SELECT * FROM Product
    WHERE tag1 LIKE %s OR tag2 LIKE %s OR tag3 LIKE %s
    '''
    return sql

def searchProductByNameAndTag():
    sql = '''
    SELECT * FROM Product
    WHERE pname LIKE %s OR tag1 LIKE %s OR tag2 LIKE %s OR tag3 LIKE %s
    '''
    return sql

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
