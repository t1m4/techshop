"use strict";

function get(onSuccess, onError) {
    var URL = "/api/v1/basket/delete/1/" ;
    var xhr = new XMLHttpRequest();
    xhr.responseType = "json";
    //обработчик события
    xhr.addEventListener("load", function() {
      if (xhr.status === 200) {
        onSuccess(xhr.response);
      } else {
        onError("Статус ответа: " + xhr.status + " " + xhr.statusText);
      }
    });
    xhr.addEventListener("error", function() {
        console.log("Произошла ошибка соединения")
      onError("Произошла ошибка соединения");
    });
    xhr.addEventListener("timeout", function() {
      onError("Запрос не успел выполниться за " + xhr.timeout + "мс");
    });

    xhr.timeout = 3000; //10s
    //открываем запрос на сервер
    xhr.open("GET", URL);
    //отправляем запрос на сервер
    xhr.send();
}

function addElement(client) {
    for (var i in client) {
        var elem = document.createElement("p");
        elem.innerHTML = i.toString() + " " + client[i]
        document.body.appendChild(elem);
    }

}

function ok(data) {
    // addElement(data)
    console.log(data)
//    alert( "Загружен пользователь " + data.login );

}

function fail(url) {
    alert( 'Ошибка при запросе: ' + url );
}

function loadScript(src) {
    let button = document.querySelector('.button')
    console.log(button)
    button.addEventListener("click", () => get(ok, fail));
}
(function() {
    loadScript();
})();