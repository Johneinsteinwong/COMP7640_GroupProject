# COMP7640_GroupProject
 
# TODO

- Vendor Administration
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


# Setting up MySQL database	
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

- [Optional] To change the password for Vendor Admin login, go to setVendorAdminCredential.py and change the values for the variables 'username' and 'password', the default values are 'testing' and '1234' respectively.
 
- To set up a vendor admin login credential, run setVendorAdminCredential.py:
```
	python setVendorAdminCredential.py
```
- To launch the website, run main.py:
```
	python main.py
```

- Go to http://127.0.0.1:5000 for the login and register page.

# Logging in Vendor Admin page
- Click the 'Login' tab, choose 'Admin' from the dropdown menu.
- Enter the username and password for Vendor Admin page, default values are 'testing' and '1234' respectively.
- Click the 'Login' button.

# Vender Management
- Click "Go to vendor list" to view the list of all vendors.
- To add a new vendor, click "Add Vendor", enter the fields for "Business Name", "Score", and "Address", click "Save".
![](/img/admin_login.JPG)
# Registering a Vendor account

# Registering a Customer account