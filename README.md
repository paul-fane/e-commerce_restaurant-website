# E-COMMERCE RESTAURANT
#### Youtube Video Demo:  <[URL HERE](https://www.youtube.com/watch?v=dumYnaFjs30)>
#### Description:
Restaurant takeaway is a website for a restaurant that allows the customers to order their food and choose if they pick up the food from the restaurant, and eat elsewhere or deliver the food directly to their homes. There is also an administrator area, that allows a special user (admin) to add and change products, orders, and accounts, allows also to archive and unarchive products and do an advanced search in the existing orders.

### **Architecture** <br>
- Frontend - Javascript, HTML, CSS, Bootstrap, Jinja templates
- Backend – Python (Flask)
- Database - SQLite 

### **app.py** <br>
Atop the file is a bunch of ```imports```. After that, the ```flask app``` is ```configured```.  It then further configures Flask to ```store sessions``` on the ```local filesystem``` (as opposed to storing them inside of cookies, which is Flask’s default). The file then configures ```CS50’s SQL library``` to use the ```SQLite database```.<br>
Most routes support ```GET``` and ```POST```. Most routes are ```“decorated”``` with ```@login_required``` and ```@admin_required``` (functions defined in helpers.py). That decorator ensures that, if a user tries to visit any of those routes, he or she will have to be logged in or logged in as admin.

This application supports the following ```API routes```:

* **GET /index (return index.html)** <br>
Visiting the index page it possible to see the restaurant's description 

* **GET /pickup-menu (return menu-take-away.html)** <br>
On the route “/pickup-menu” it is possible to see a ```list of all the products available``` and the ```description``` of any product (```name```, ```category```, ```price```). The products are divided by category. For any product, it is possible to choose the ```quantity``` and ```add it to the cart```. When the product is added to the cart, in local storage will be created a list with the id of any product, and the quantity of any product. In the ```navbar```, the ```cart button``` will show a badge with the ```number of products``` in the cart.

* **GET  /cart (return cart.html)** <br>
After adding all the products to the cart, the customer can visit the route /cart. <br>
In the ```cart```, there are: <br>
   - a list with the ```products``` (if the user adds some) and for any product, the user can see ```the price``` based on the ```quantity```, can also ```change the quantity``` (and also the price will change), or can ```delete``` it from the list (implemented in JavaScript).
   - ```total price```
   - an input to select the ```date and time```, when to deliver or pick up the food
   - an input to choose the ```type of order``` (delivery or pickup)
   - if the type is delivery, another input will be required, the ```address```
   - ```order button```

   In ```local storage```, using JavaScript will be added also a variable for the ```date```, ```type```, and ```address```. All the variables in local storage will change when the user makes some changes in the cart.
To show the products in the cart, it is necessary to ```fetch```(“/search-products” this route will return the details) the detail about the products, and for any id in local storage show in the cart the detail of any product (image, name, category).
When the user ```completes the order```, the variables in local storage will be removed and ```the cart will be empty```.

* **POST /cart** <br>
For this project, to conclude the order, a ```login is required```. 
If the user is logged in and ```does not miss any field``` of the cart, then can click the order button and ```conclude the order```, the order will be posted to the server using JavaScript and then the server will add it to the database and the user will see a ```successful alert``` otherwise, the user will see an alert with the name of the ```missing input``` that can be “Date missed!”, “Product missed!”, “Type missed! Choose between Delivery and Pickup” or “Address missed!” if the address is required.
If the user is not logged in will not be able to order and will receive an alert “Login required!”.

* **GET /Register (return register.html)**  <br>
By visiting the ```/register``` route the user can compile the form and send it to the server by clicking the “Register” button. 
The form requires that a user input a ```username``` (if the user’s input is blank or the username already exists, the user will receive an apology), requires that a user inputs a ```full name```, an ```email```, and a ```password```, and then that ```same password again``` (if either input is blank or the passwords do not match, then the user will receive an apology)

* **POST /register** <br>
The user will be inserted in the database storing a ```hash``` of the user’s ```password```, not the password itself.
After sending the form, the user has redirected to the index page with the possibility to order from the cart and with other routes available like “/account” and “/logout”. Logout will simply log out of the user from his account.

* **GET POST /login (return login.html)** <br>
The ```/login``` route is for users that ```have already an account``` and want to log in. The form that the user get requires that a user inputs his ```username``` and his ```password``` (if either input is blank, the username does not exist or the passwords do not match, then the user will receive an apology).

* **GET /account (return account.html)** <br>
For the ```/account``` route the ```login is required```. Here we can see the ```description of our profile``` and the ```list of our orders```. By clicking on any ```order``` we will be redirected to a route ```“/account/orders/<order_id>”``` (return ```orderDetails.html```) where we can see all the ```details about the order``` including the ```list of the products``` in that order. ```<order_id>``` is the id of the order in the list that I select. 

* **GET /admin (return admin.html)** <br>
There is an ```administrator area```. Only a ```special user``` can visit the ```admin route```, any other user who is trying to visit the admin route will receive an ```alert```. The admin is the ```user id number 1```, the first user registered on the database. To ```log in as admin``` it is necessary to use ```“username: admin”``` and ```“password: admin”```.
This area allows the admin to ```add``` and ```change``` ```products```, ```orders```, and ```customers```. For each table, there is a button to ```“Add”``` and a button to ```“Change”```. 

* **GET /admin/products (return products.html)** <br>
By clicking the Change button on the products table, the ```“/admin/products”``` route can be visited. Here, there are ```a list of all the products``` in the database and another ```list of archived products```. Any product in the list, by clicking it, will redirect to a route ```“/admin/products/<product_id>/change”``` that allows you to ```change``` anything about that product, including ```archive``` it or ```unarchive``` it. In the “/pickup-menu” route, the archived products are not listed.
* **GET POST /admin/products/<product_id>/change (return changeProduct.html)** <br>
  Return a form populated with the current value of the product selected. Give the possibility to change the value and submit them. <product_id> is the id of the product that was selected to be changed.

* **GET POST /admin/products/add (return addProduct.html)** <br>
Clicking the ```“Add” products``` button will return an empty ```form``` that allows adding a ```new product```. For the ```category```, it is possible to select an ```existing category``` or ```create a new one``` by writing a new name. 

* **GET /admin/customers (return customers.html)** <br>
The same for the ```change customers```, there is ```a list of all customers```. By clicking on any customer it is possible to ```change``` his information in the route ```“/admin/customers/<customer_id>/change”```.

* **GET POST /admin/customers/add (return addCustomer.html)** <br>
```Add customers``` allows you to add a new customer, similar with add products.

* **GET /admin/orders (return orders.html)** <br>
Will return a ```list with all the orders``` in the database and the possibility to ```change``` the information about any order similar to changing products and customers. ```“/admin/orders/<order_id>/change”``` will be the route to change and “order_id” is the id of the order selected.
In this route, the admin can also do an ```advanced search``` to see only the orders of his interest. The search form will give the possibility to search by ```“Type”```, ```“Customer Name”```, ```“Unique ID”```, ```“Pickup/Delivery date”```. The admin can search by ```one``` or ```many``` inputs. Searching by ```Customer Name``` will also return ```similar names```. 

* **GET POST /admin/orders/add** <br>
Not implemented yet.

* **POST /search-orders** <br>
When the form for ```searching``` inside the ```“orders.html”``` is ```submitted``` select all its inputs and post them to the server using ```“fetch”``` (using ```JavaScript```).<br> When the server will receive the post will set an empty value for the empty inputs necessary for making the search later. <br>
**```If```** in the search there is also a ```“customerName”``` then search ```similar name``` in the ```customer``` table. 
   - **```If```** the length of the customer’s search is ```“0”``` return to the client the message ```“No user with that name!”```,<br> 
   - **```else```** for any customer with a similar name do an advanced search in the orders table including the other inputs (type, uniqueID, pickup_deliveryTime) then add all the results to an array and send it to the client.<br>
  
   **```Else```** if the ```customerName``` input is ```empty``` then search (```type```, ```uniqueID```, ```pickup_deliveryTime```) in the ```orders table``` and send it to the client.

### **helpers.py**

There’s the implementation of ```apology```, it renders a ```message``` as an apology ```to users```, rendering a template, ```apology.html```. The function takes as input a message and an error code number. It also defines within itself another function, ```escape```, that it simply uses to replace special characters in apologies. <br>
Next in the file are ```login_required``` and ```admin_required``` functions each of them ```returns another function```.  The first will check if there is a user in the session (```logged in```), and the second will check if there is a special user (```logged in as admin```) in the session (user number 1), ```otherwise```, the ```access will be denied``` and the user will be redirected to another route whit a message.

### **takeaway.db** 
DATABASE

Within ```“/project”``` it is possible to run ```“sqlite3 takeaway.db”``` to open ```takeaway.db``` with ```sqlite3```. If you run ```.schema``` in the SQLite prompt, notice how takeaway.db comes with some ```tables```:
- ```customer``` (<br>
customerID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,<br> 
customerName varchar(40) NOT NULL,<br>
username varchar(40) NOT NULL,<br> 
email varchar(40) NOT NULL,<br> 
hashPassword TEXT NOT NULL,<br> 
created_at DATETIME);
- ```orders``` (<br>
orderID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, <br>
uniqueID TEXT NOT NULL, <br>
customerID INTEGER NOT NULL, <br>
created_at DATETIME NOT NULL, <br>
pickup_delivery_time DATETIME NOT NULL, <br>
total_price FLOAT NOT NULL,<br>
type varchar(40) NOT NULL, <br>
address TEXT); 
- ```order_details``` (<br>
order_detailsID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,<br> 
uniqueID TEXT NOT NULL, <br>
productID INTEGER NOT NULL, <br>
quantity INTEGER NOT NULL);
- ```product``` (<br>
productID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, <br>
productName varchar(300) NOT NULL, <br>
price FLOAT NOT NULL, <br>
archive BOOLEAN DEFAULT false, <br>
category varchar(300), <br>
image varchar(255));

### **requirements.txt**
That file simply prescribes the ```packages``` on which this app will depend.

### **/static**
 inside of which is an ```images``` folder, ```style.css```, and ```javascript.js```. Inside the images folder, there are some images used for the products. 

### **/static/javascript.js**
- ```Set cart length```.<br> 
  In the first function, if there is an array of the cart in local storage, then in the badge of the ```cart button``` in the ```navbar``` set the ```length of the cart```.
- ```Add functionality to addToCartButtons```.<br>
   **For each** ```“Add to cart”``` button inside ```“menu-take-away.html”``` when the button is ```clicked```, select its inner ```dataset``` (the ```ID``` of the product), select also the ```quantity``` that the user inputs for the same product, and ```add``` them to the ```local storage```. <br>
   **If** the cart array is not yet created in local storage, then create it and add the new product.<br> 
   **Else if** the cart already exists check if the product is in the cart, then if not, add it to the cart. Update also the length of the cart in the navbar cart button.
- ```Shadow the card```.<br> 
   **For every** ```card class```<br>
   **if** the ```mouse is over``` set the style shows a ```big shadow```<br>
   **if** the ```mouse out``` shows a ```small shadow```.<br> The ```card class``` is used in many places: for the ```products``` in “menu-take-away.html”, for the ```account description``` in “account.html”, for the ```order details``` in “orderDetails.html”, and for the ```search orders``` in “orders.html”.
- ```Search orders```.<br>
   When the ```form``` for searching inside the ```“orders.html”``` is ```submitted```, select all its inputs and send them to the server using ```“fetch”```. The server inside the “searchOrders” function will do the advanced search and will ```return a response```.<br>
   **If** the response is ```“no user with that name”``` adds that message as a result of the search,<br>
   **otherwise**, <br>
    - **if** there is an ```old search```, ```remove``` it before adding the new one. 
    - **If** the new one is ```empty``` then show a message that says ```“No result!”```, 
    - **else**, show the ```list with all the specific orders``` send from the server. Every order in the list will show the “orderID”, “uniqueID”, and “customerName”.  For the customer name, it is necessary to search in the customer’s list, because in the orders it is stored only the customer ID.
- ```Function selector in admin area “change order”```.<br>
  In the admin area (“changeOrder.html”) when an order is selected to be changed, will return a form that will be populated with the current information about that order. The type of order can be Pickup or Delivery. In the select tag where the user can change the type, the selected value will be the current value of the order. In this function, if the current option selected is “Pickup” the other option will be set as “Delivery”, otherwise, if the selected option is “Delivery” the other option will be set as “Pickup”.
- ```Create the cart```. <br>
  When a user visits the ```/cart``` route, the cart will be populated with the products from ```local storage```.<br>
  **If** the cart does not exist in local storage then the cart will show the message ```“The cart is empty”```.<br>
In local storage, there is only the id and quantity of any products. When the cart is created it is necessary to fetch the ```product details``` from the server. Then for any id in local storage, show all the details fetched from the server(```imageUrl```, ```product name```, ```category```), show also an input whit the ```quantity``` value from the local storage, show the ```price``` based on the quantity, show a ```delete button```, and calculate also the ```total price``` and show it after the list of products.<br>
Inside the ```“createTheCart”``` function there are a bunch of ```other functions```:
  - If there is no ```date```, ```type```, and ```address``` in ```local storage``` then create it, else populate the cart with the variables that already exist in local storage. 
  - Create ```“deleteItem”``` function, when the delete button is clicked, the product will be removed and the total price will be updated.
  - ```Change price```. The function will change the price when the quantity is changed.
  - ```On change```, add type, date, and address to local storage.
  - When the ```cart``` is ```submitted```, the local storage variables will be selected and sent to the server. If there are no products in the cart or if other inputs are missed, the user will see an alert, otherwise, the user will see a successful alert.
- ```Checkbox``` in the admin area products. Set the checkbox (checked/not-checked) based on the value received from the server and ad functionality, on change, change also the inner value.
- In the cart ```show/hide address```. If the type of order is “Delivery” then show the address input, else hide the address input.

### **/templates** <br>
In the folder named templates are all HTML files.<br>
**layout.html**<br>
```Layout.html``` is the ```structure``` of the page, ```any other HTML``` file in this project will be an ```extension of layout.html```. <br>
In the **head** tag, there are:
- some **meta** tags that are necessary for making the website mobile responsive
- some tags that import the **Bootstrap** Framework, the **javascript.js** file, and the **style.css** file 
- a **title** tag. Inside the title tag using Jinja syntax, there is a **```“block title”```**. All the block tag does is to tell the template engine that a child template (an extension) may override those portions of the template.<br>
  
In the **body** tag, there are:
- the **navbar** that allows the user to navigate through the website. The navbar change based on the fact that a user or the admin is logged in. 
- **header** tag that shows an alert if receives a flashed message from the server
- **main** tag. Inside the main tag, there is a **```“block main”```**.
