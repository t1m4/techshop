function post(onSuccess, onError, url, data) {
    var URL = url;
    var xhr = new XMLHttpRequest();
    //обработчик события
    xhr.addEventListener("load", function () {
        console.log(xhr.status)
        if (xhr.status === 200) {
            onSuccess(xhr.response);
            // window.location = '/search/';
        } else if (xhr.status === 301) {
            onSuccess(xhr.response);
            window.location = '/search/';
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
    xhr.open("POST", URL, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    //отправляем запрос на сервер
    xhr.send(data);
}

function get(onSuccess, onError, url) {
    var URL = url;
    var xhr = new XMLHttpRequest();
    //обработчик события
    xhr.addEventListener("load", function () {
        if (xhr.status === 200) {
            onSuccess(xhr.response);
            // window.location = '/search/';
        } else if (xhr.status === 301) {
            onSuccess(xhr.response);
            // window.location = '/search/';
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
    xhr.open("GET", URL, true);
    // xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    //отправляем запрос на сервер
    xhr.send();
}

function ok(data) {
    console.log('ok')

}

function fail(url) {
    console.log('Ошибка при запросе: ' + url)
    // alert('Ошибка при запросе: ' + url);
}

(function () {
    // post(ok, fail, '/search/', 'search=honor')
    buttonSearch()
})();

function buttonSearch() {
    var input = document.querySelector('.search_input')
    var button = document.querySelector('.search_submit')
    button.addEventListener('click', function () {
        // get(ok, fail, par)
        post(ok, fail, '/search/?search='+input.value, 'search=' + input.value)
    })
}