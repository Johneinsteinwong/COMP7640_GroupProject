# COMP7640_GroupProject
 
# TODO

- Vender Administration
    - [x] Display a listing of all vendors
    - [x] Onboard new vendors onto the marketplace
- Product Catalog Management
    - [x] Browse all products offered by a specific vendor
    - [x] Introduce new products to a vendor's catalog
- Product Discovery
    - [x] Facilitate a search feature that allows users to discover products using tags,
    the search should return products where the tag matches any part of the product's name or its associated tags
- Product Purchase
    - [ ] You should support product purchase. Record in database which customer purchases which product
- Order Modification
    - [ ] Users must have the option to modify their orders, including the removal of specific products or the cancellation of the entire order before it enters the shipping process
	
# Getting Started


# Set up MySQL database	
- Go to MySQL workbench and create a database called 'ecommerce':
```
	CREATE DATABASE ecommerce;
```

- Go to global_profile.py and enter your MySQL credential:
```
	database_login_user = SqlAdmin(username, password, 'ecommerce')
```
Where username and password are your MySQL user and password respectively.

- To create the required tables, run initDB.py:
```
	python initDB.py
```

- To launch the website, run main.py:
```
	python main.py
```

- Go to http://127.0.0.1:5000 for the login and register page.