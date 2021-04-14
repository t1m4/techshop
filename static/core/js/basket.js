"use strict";

var div_products = document.querySelector(".product_list")
var template = document.querySelector("template").content;

function get(onSuccess, onError, url) {
    var URL = url;
    var xhr = new XMLHttpRequest();
    xhr.responseType = "json";
    //обработчик события
    xhr.addEventListener("load", function () {
        if (xhr.status === 200) {
            onSuccess(xhr.response);
        } else {
            onError("Статус ответа: " + xhr.status + " " + xhr.statusText);
        }
    });
    xhr.addEventListener("error", function () {
        console.log("Произошла ошибка соединения")
        onError("Произошла ошибка соединения");
    });
    xhr.addEventListener("timeout", function () {
        onError("Запрос не успел выполниться за " + xhr.timeout + "мс");
    });

    xhr.timeout = 3000; //10s
    //открываем запрос на сервер
    xhr.open("GET", URL);
    //отправляем запрос на сервер
    xhr.send();
}

function post_order(onSuccess, onError, url, data) {
    var URL = url;
    var xhr = new XMLHttpRequest();
    xhr.responseType = "json";
    //обработчик события
    xhr.addEventListener("load", function () {
        if (xhr.status === 200) {
            onSuccess(xhr.response);
        } else {
            onError("Статус ответа: " + xhr.status + " " + xhr.statusText);
        }
    });
    xhr.addEventListener("error", function () {
        console.log("Произошла ошибка соединения")
        onError("Произошла ошибка соединения");
    });
    xhr.addEventListener("timeout", function () {
        onError("Запрос не успел выполниться за " + xhr.timeout + "мс");
    });

    xhr.timeout = 3000; //10s
    //открываем запрос на сервер
    xhr.open("POST", URL);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    //отправляем запрос на сервер
    // xhr.send(JSON.stringify({
    //     "products": [
    //         {"id": 2, "amount": 1},
    //     ]
    // }));
    xhr.send(JSON.stringify(data))
}

function ok(data) {
    // addElement(data)
    console.log(data)
//    alert( "Загружен пользователь " + data.login );

}

function fail(url) {
    alert('Ошибка при запросе: ' + url);
}


// create products
function createProduct(element) {
    var operation_element = template.cloneNode(true);
    var product_id = operation_element.querySelector('.product_list__product');
    product_id.id = element.id

    var name = operation_element.querySelector('.product_list__product__name');
    name.textContent = element.name.toString()
    var price = operation_element.querySelector('.product_list__product__price');
    price.textContent = "Цена: " + element.price.toString();
    price.dataset.price = element.price
    var amount = operation_element.querySelector('.product_list__product__count input');
    amount.value = element.amount;
    var total_price = operation_element.querySelector('.product_list__product__total_price');
    total_price.textContent = "Итого: " + element.price * element.amount

    amount.addEventListener('input', function () {
        total_price.textContent = "Итого: " + element.price * amount.value
        updateTotalPrice()
    })
    var button_minus = operation_element.querySelector('.button_minus')
    button_minus.addEventListener('click', function () {
        amount.value -= 1
        total_price.textContent = "Итого: " + element.price * amount.value
        updateTotalPrice()
    })
    var button_plus = operation_element.querySelector('.button_plus')
    button_plus.addEventListener('click', function () {
        amount.value = parseInt(amount.value, 10) + 1
        total_price.textContent = "Итого: " + element.price * amount.value
        updateTotalPrice()
    })

    var button_delete = operation_element.querySelector('.delete_button')
    button_delete.addEventListener('click', function () {
        let url = "/api/v1/basket/delete/" + product_id.id
        get(success_delete, fail, url)
        product_id.remove()
        updateTotalPrice();
    })


    return operation_element;
}

function success_delete(data) {
    if (data.status === 'ok') {
        console.log('delete')
        updateTotalPrice();
    }
}

// success function for load products
function success_products(data) {
    if (data.status === 'ok') {
        var fragment = document.createDocumentFragment();
        if (data.products.length > 0) {
            for (var i = 0; i < data.products.length; i++) {
                fragment.appendChild(createProduct(data.products[i]))
                div_products.appendChild(fragment)
            }
        }
        updateTotalPrice()
    }
}

// Load products
function getAllProduct() {
    let url = "/api/v1/basket/products"
    get(success_products, fail, url)
}

function updateTotalPrice() {
    var products = document.querySelectorAll(".product_list__product__price")
    var amounts = document.querySelectorAll(".product_list__product__count input")
    var total_result = document.querySelector(".total_result__sum")
    var total_price = 0
    if (products.length > 0) {
        for (var i = 0; i < products.length; i++) {
            total_price += parseInt(products[i].dataset.price, 10) * amounts[i].value
        }
    }
    total_result.textContent = "Сумма: " + total_price.toString()
}

function success_post(data) {
    if (data.status === 'ok') {
        console.log(data)
        window.location.href = "/account/orders/"+data.id;
        // window.location.href = "http://127.0.0.1:8000/";
    }
}
function buttonPay() {
    var button = document.querySelector('.pay_button')
    button.addEventListener('click', function () {
        var data = {'products': []}
        var products = document.querySelectorAll(".product_list__product")
        var amounts = document.querySelectorAll(".product_list__product__count input")
        if (products.length > 0) {
            for (var i = 0; i < products.length; i++) {
                data['products'].push({"id":  products[i].id, "amount":  amounts[i].value})
            }
        }
        post_order(success_post, fail, '/api/v1/order/create/', data)
    })
}

(function () {
    getAllProduct();
    // setTimeout(updateTotalPrice, 3000);
    // buttonClick();
    // loadScript();
    // post(ok, fail, '/api/v1/order/create/')
    buttonPay()
})();