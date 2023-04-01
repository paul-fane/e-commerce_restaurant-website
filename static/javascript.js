// Select the cart in local storage
let cart = JSON.parse(localStorage.getItem("cart"));

// Set the notification number in the navbar button of the cart
const cartNavButton = document.querySelector('.cart-nav-button');
if (cart){
    cartNavButton.innerHTML = cart.length;
}

// Add to cart button
const addToCartButtons = document.querySelectorAll('.add-to-cart');
addToCartButtons.forEach(button => {addToCart(button)});

// Shadow the card 
const cards = document.querySelectorAll('.card');
cards.forEach(card => {
    card.addEventListener('mouseover', ()=>{
        card.className = "card shadow-lg p-3 mb-5 bg-body rounded";
    });
    card.addEventListener('mouseout', ()=>{
        card.className = "card shadow p-3 mb-5 bg-body rounded";
    });
})


// Search orders
if(document.querySelector('#search-order-button')){
    document.querySelector('#search-order-button').addEventListener('click', ()=>{
        // Select value input
        let type = document.querySelector('#type-search').value;
        let customerName = document.querySelector('#customerName-search').value;
        let uniqueID = document.querySelector('#uniqueID-search').value;
        let pickup_deliveryTime = document.querySelector('#pickup_delivery_time-search').value;

        
        fetch('/search-orders', {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({type, customerName, uniqueID, pickup_deliveryTime})
        })
        .then(response => response.json())
        .then(resp => {
            // Await the response
            console.log(resp);
            if (resp === 'No user with that name!'){
                // Show the response of the search
                document.querySelector('.result-search-order').innerHTML = `
                <tr class="table-design">
                    <td>
                        'No user with that name!'
                    </td>
                </tr>
                `;
                document.querySelector('#length-search').innerHTML = `RESULT SEARCH (0)`;
            } else {

                // Delete the old search
                const list = document.querySelector(".result-search-order");

                while (list.hasChildNodes()) {
                list.removeChild(list.firstChild);
                }

                // If the lenght of the orders = 0 then show no result 
                if (resp[0].length === 0){
                    document.querySelector('.result-search-order').innerHTML = `
                        <tr class="table-design">
                            <td>
                                No result!
                            </td>
                        </tr>
                        `;
                    document.querySelector('#length-search').innerHTML = `RESULT SEARCH (0)`;
                }
                // resp[0] => orders, resp[1]=> customers
                for (let order of resp[0]){
                    let customerName = ""
                    for (let customer of resp[1]){
                        // For every order, search the customer name in the customers list
                        if(order.customerID === customer.customerID){
                            customerName = customer.customerName;
                        }
                    }
                    // for every order create a row in the table 
                    let tr = document.createElement('tr');
                    tr.className = 'result-search-order';
                    tr.innerHTML = `
                        <td>
                            <div class="table-title">
                                <a class="table-font" href="/admin/orders/${order.orderID}/change">
                                    ${order.orderID}. ID(${order.uniqueID})  -  ${customerName} 
                                </a>
                                <small class="table-design text-muted">Created: ${order.created_at}</small>
                            </div>
                        </td>
                    `;
                    document.querySelector('#length-search').innerHTML = `RESULT SEARCH (${resp[0].length})`;
                    document.querySelector('.result-search-order').append(tr);

                }
            }
            return false;
        })
        .catch(err => {
            console.log(err);
        }); 
    });
}


// Function selector in admin area-change order
if(document.querySelector('#value-type-order-database')){
    if(document.querySelector('#value-type-order-database').value === "Pickup"){
        var opt = document.createElement('OPTION');
        opt.text = 'Delivery';
        opt.value = 'Delivery';
        document.querySelector('.second-option').options.add(opt);
    } else {
        var opt = document.createElement('OPTION');
        opt.text = 'Pickup';
        opt.value = 'Pickup';
        document.querySelector('.second-option').options.add(opt);
    }
}

// Create the cart
// If the cart page is open, and select query available
if (document.querySelector('#cart-body')){
    // If cart in local storage => Show the cart in the cart route
    if (cart){
        createTheCart(cart);
    } else {
        // If no cart in local storage => Show message "empty cart"
        const tr = document.createElement('tr');
        tr.innerHTML = "The cart is empty";
        document.querySelector('#cart-body').append(tr);
    }
}


// Checkbox in adminarea
archive = document.querySelector('#change-archive');
if (archive){
    // Set checkbox based on the value recived from the database
    if(archive.value == 1){
        // If value = 1 => checkbox checked
        archive.checked = true;
    }else {
        // If value = 0 => checkbox not checked
        archive.checked = false;
    }
    // Add functionaliti to the checkbox
    archive.onchange = ()=>{
        // Set the value of the checkbox based on the user input
        if (archive.checked === true){
            archive.value = 1;
            return false
        } else {
            archive.value = 0;
            return false
       }
    }
}


// CART => If delivery required => add also the address input
if(JSON.parse(localStorage.getItem("type")) && document.querySelector('#address-order')){
    if(JSON.parse(localStorage.getItem("type")) === "Delivery"){
        document.querySelector('#address-order').style='display:table-row;';
    } else {
        document.querySelector('#address-order').style='display:none;';
    }
} else {
    if(document.querySelector('#address-order')){
        document.querySelector('#address-order').style='display:none;';
    }
}



// Add item to cart
function addToCart(button){
    button.addEventListener('click', ()=>{
        // Select the productID and the quantity
        const productID = button.dataset.id;
        const quantity = document.querySelector(`#quantity-${productID}`).value;
        
        // Create an object with the id and quantity
        let product = {
            id: productID,
            quantity: quantity
        }

        // If no array cart in local storage, create it
        if(!localStorage.getItem("cart")){
            localStorage.setItem("cart", "[]");
        }

        // Select the cart in local storage
        let cart = JSON.parse(localStorage.getItem("cart"));

        // If len cart = 0 push the product
        if(cart.length == 0){
            cart.push(product);
        }else{
            // Else check if the product is in the cart and then push
            let findProduct = cart.find(item => item.id == productID);
            if(findProduct === undefined){
                cart.push(product);
            }
        }

        // Set the notification number in the navbar button of the cart
        const cartNavButton = document.querySelector('.cart-nav-button');
        if (cart && cartNavButton){
            cartNavButton.innerHTML = cart.length;
        }

        // Set the local storage with  the new update cart
        localStorage.setItem("cart", JSON.stringify(cart));
    });
}


// Create the cart, the local storage variable
// Add functionalities
function createTheCart(cart){
    totalPrice = 0;

    //fetch all the products information to create the product in the cart
    fetch(`/search-products`)
    .then(response => response.json())
    .then(products => {
        // For every product in the cart
        for (let product of cart){
            // Filter the fetch products to return the product in the cart
            let itemInProducts = products.filter(item => item.productID == product.id)[0];

            // Create the body of the cart in cart.html
            const tr = document.createElement('tr');
            tr.setAttribute("id", `item-cart-${product.id}`);
            
            tr.innerHTML = `
                <td class="text-start">
                    <div class="card mb-3" style="max-width: 540px;">
                        <div class="row g-0">
                            <div class="col-md-4">
                                <img src="${itemInProducts.image}" height="5px" class="img-fluid rounded-start card-img-top-cart" alt="...">
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h5 class="card-title">${itemInProducts.productName}</h5>
                                    <p class="card-text">${itemInProducts.category}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </td>

                <td class="text-end">
                    <input type="number" class="input-cart-quantity" id="quantity-${product.id}" data-idproduct="${product.id}" data-unitprice="${itemInProducts.price}" value="${product.quantity}" min="1" step="1">
                </td>

                <td class="text-end">
                    <p id="price-${product.id}">${(product.quantity * itemInProducts.price)}</p>
                </td>

                <td>
                    <button  type="submit" id="delete-btn-${product.id}" data-idproduct="${product.id}" class="btn-close button-close-cart" aria-label="Close"></button>
                </td>`;

            totalPrice += (product.quantity * itemInProducts.price);
            document.querySelector('#cart-body').append(tr);

            document.querySelector('#cart-price').innerHTML = Math.round(totalPrice * 100) / 100 + "$";

        }

        // If no date, type and address in local storage, create it
        // Else populate the cart with the variable from the local storage
        // Date
        if(!localStorage.getItem("date")){
            let date = document.querySelector('#date-cart').value;
            localStorage.setItem("date", JSON.stringify(date));
        } else {
            let localStorageDate = JSON.parse(localStorage.getItem("date"));
            document.querySelector('#date-cart').value = localStorageDate;
        }
        // Type
        if(!localStorage.getItem("type")){
            let type = document.querySelector('#pickup-delivery').value;
            localStorage.setItem("type", JSON.stringify(type));
        } else {
            let localStorageType = JSON.parse(localStorage.getItem("type"));
            document.querySelector('#pickup-delivery').value = localStorageType;
        }
        // Address
        if(!localStorage.getItem("address")){
            let address = document.querySelector('#address-order-input').value;
            localStorage.setItem("address", JSON.stringify(address));
        } else {
            let localStorageAddress = JSON.parse(localStorage.getItem("address"));
            document.querySelector('#address-order-input').value = localStorageAddress;
        }
        


        // Delete item (button) in cart
        const deleteItem = document.querySelectorAll('.button-close-cart');
        deleteItem.forEach(item => {
            item.addEventListener('click', ()=>{
                
                const itemId = item.dataset.idproduct;
                
                // Global variable let cart is not update => Check the update cart 
                let updateCart = JSON.parse(localStorage.getItem("cart"));

                let tempCart = updateCart.filter(item => item.id != itemId);
                localStorage.setItem("cart", JSON.stringify(tempCart));

                // Select the total price of the item that will be remove
                let price = document.querySelector(`#price-${itemId}`).innerHTML;
                totalPrice = totalPrice - price;
        
                // Remove the item
                document.querySelector(`#item-cart-${itemId}`).remove();

                // Set the new total price
                document.querySelector('#cart-price').innerHTML = Math.round(totalPrice * 100) / 100 + "$";

                // After delet an item, set the length of the new cart in the navbar
                cartNavButton.innerHTML = tempCart.length;

            }); 
        });


        // Change price
        const changePrice = document.querySelectorAll('.input-cart-quantity');
        changePrice.forEach(item => {
            item.addEventListener('input', ()=>{

                // Select the id, unitPrice, quantity => all stored in the input tag
                const itemId = item.dataset.idproduct;
                const unitPrice = item.dataset.unitprice;
                const quantity = item.value;

                // Select old price of product
                let oldPrice = document.querySelector(`#price-${itemId}`).innerHTML;
                
                // Global variable let cart is not update => Check the update cart 
                let updateCart = JSON.parse(localStorage.getItem("cart"));

                //Find index of specific object to chang quantity using findIndex method
                let objIndex = updateCart.findIndex((obj => obj.id == itemId)); 
                updateCart[objIndex].quantity = quantity;

                localStorage.setItem("cart", JSON.stringify(updateCart));

                // Set the new price x quantity
                document.querySelector(`#price-${itemId}`).innerHTML = Math.round(quantity * unitPrice * 100) / 100;
        
                // Set the new total price
                totalPrice = totalPrice - oldPrice + (quantity * unitPrice);
                document.querySelector('#cart-price').innerHTML = Math.round(totalPrice * 100) / 100 + "$";
            }); 
        });

        // On change, add pickup-delivery, date and address to local storage
        // Date
        document.querySelector('#date-cart').addEventListener('change',()=>{
            let date = document.querySelector('#date-cart').value;
            localStorage.setItem("date", JSON.stringify(date));
        });
        // Pickup/Delivery
        document.querySelector('#pickup-delivery').addEventListener('change',()=>{
            let type = document.querySelector('#pickup-delivery').value;
            localStorage.setItem("type", JSON.stringify(type));

            // If delivery required => add also the address else remove the address
            if(type === "Delivery"){
                document.querySelector('#address-order').style='display:table-row;';
                // If the usere chose delivery and there are an old input => change the value
                document.querySelector('#address-order-input').value = "";
            } else {
                document.querySelector('#address-order').style='display:none;';
                // When the user chose pickup => remove the address from local storage
                localStorage.removeItem("address");
            }
        });
        // Address
        document.querySelector('#address-order-input').addEventListener('input', ()=>{
            let address = document.querySelector('#address-order-input').value
            localStorage.setItem("address", JSON.stringify(address));
        });

        // Sent the cart
        const formCartButton = document.querySelector("#form-cart-button");
        if (formCartButton){
            // If the form is submitted
            formCartButton.addEventListener('click', ()=>{
                // Select the cart detail
                let cart = JSON.parse(localStorage.getItem("cart"));
                let type = JSON.parse(localStorage.getItem("type"));
                let date = JSON.parse(localStorage.getItem("date"));
                let address = JSON.parse(localStorage.getItem("address"));
                // Send the data to the server
                fetch('/cart', {
                    method: 'POST',
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({cart, date, type, address})
                })
                .then(response => response.json())
                .then(resp => {
                    // Await the response
                    if(document.querySelector('.alert-cart')){
                        document.querySelector('.alert-cart').remove();
                    }
                    if (resp === "Type missed! Choose betwen Delivery and Pickup"){
                        // If input missed => create alert
                        const div = document.createElement('div');
                        div.className = "alert alert-primary mb-0 text-center alert-cart";
                        div.setAttribute('role',"alert");
                        div.innerHTML = resp;
                        document.querySelector('header').append(div);
                        return false;
                    } else if (resp === "Successfuly order!"){
                        // If success => remove the cart and redirect with success
                        localStorage.removeItem("cart");
                        localStorage.removeItem("type");
                        localStorage.removeItem("date");
                        localStorage.removeItem("address");

                        window.location.href = '/pickup-menu';
                    } else if (resp === "Date missed!"){
                        // If input missed => create alert
                        const div = document.createElement('div');
                        div.className = "alert alert-primary mb-0 text-center alert-cart";
                        div.setAttribute('role',"alert");
                        div.innerHTML = resp;
                        document.querySelector('header').append(div);
                        return false;
                    } else if (resp === "Products missed!"){
                        // If input missed => create alert
                        const div = document.createElement('div');
                        div.className = "alert alert-primary mb-0 text-center alert-cart";
                        div.setAttribute('role',"alert");
                        div.innerHTML = resp;
                        document.querySelector('header').append(div);
                        return false;
                    } else if (resp === "Address missed!"){
                        // If input missed => create alert
                        const div = document.createElement('div');
                        div.className = "alert alert-primary mb-0 text-center alert-cart";
                        div.setAttribute('role',"alert");
                        div.innerHTML = resp;
                        document.querySelector('header').append(div);
                        return false;
                    }
                })
                .catch(err => {
                    console.log(err);
                }); 
            });
        }
    })
    .catch(err => {
        console.log(err);
    });    
}
