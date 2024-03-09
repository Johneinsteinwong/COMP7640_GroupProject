-- Onboard new vendors onto the marketplace
INSERT INTO Vender(vname, geographic)
VALUES (?,?)

-- Browse all products offered by a specific vendor
SELECT * FROM
(SELECT * FROM Product, Vender
WHERE Product.vid = Vender.vid)
WHERE vname = ?

WITH TMP AS 
    (SELECT * FROM Product, Vender
    WHERE Product.vid = Vender.vid)
SELECT * FROM TMP
WHERE vname = ?

-- Introduce new products to a vendor's catalog
cursor.execute('''
INSERT INTO Product(pname, price, vid) 
VALUES (%s,%f,%d)
''', () )

-- Facilitate a search feature that allows users to discover products using tags, 
-- the search should return products where the tag matches any part of the product's
-- name or its associated tags
SELECT * FROM Product
WHERE pname LIKE '%%s%' OR tag1 = %s OR tag2 = %s OR tag3 = %s

-- Customer Register
INSERT INTO Customer(contactNumber, shippingDetail)
VALUES (%d,%s)
-- support product purchase. Record in database which customer purchases which product
INSERT INTO Ordered(cid, pid, quantity, orderStatus, orderTime)
VALUES (%d,%d,%d,%s,%s)

-- cancellation of the entire order before it enters the shipping process
UPDATE Ordered
SET orderStatus = 'cancelled'
WHERE oid = ?

-- the removal of specific products
DELETE FROM Ordered
WHERE oid = ? AND pid = ?