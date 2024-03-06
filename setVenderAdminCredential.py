import pymysql
from hashlib import sha256

db = pymysql.connect(host='localhost',
                     user='test',
                     password='1234567890-=',
                     database='ecommerce')
 
username = 'hi'
password = '1234'
salt = 1 #generate a CPRN
hashed_pw = sha256(str.encode(password + str(salt))).hexdigest()

cursor = db.cursor()

sql = '''
    INSERT INTO vAdmin (username, password, salt)
    VALUES (%s, %s, %s)
'''

cursor.execute(sql, (username, hashed_pw, salt))

cursor.close()
db.commit()
db.close()