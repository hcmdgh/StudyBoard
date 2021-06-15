const isDev = false;
const baseUrl = isDev ? 'http://localhost:5000' : 'http://study.genghao.xyz/api';

function _concat(url) {
    if (!url.startsWith('/')) {
        url = '/' + url;
    }
    if (!url.endsWith('/')) {
        url = url + '/';
    }
    return baseUrl + url;
}

// function ajaxGet(url) {
//     let resp = null;
//     $.ajax({
//         type: 'GET',
//         async: false,
//         url: url,
//         success: function (resp_) {
//             resp = resp_;
//         }
//     });
//     if (!resp) {
//         alert('无法连接到服务器，请检查您的网络连接！');
//     }
//     return resp;
// }

function ajaxPost(url, data) {
    let resp = null;
    $.ajax({
        type: 'POST',
        async: false,
        url: _concat(url),
        contentType: "application/json;charset=utf-8",
        data: JSON.stringify(data),
        success: function (resp_) {
            resp = resp_;
        }
    });
    if (!resp) {
        alert('无法连接到服务器，请检查您的网络连接！');
    }
    return resp;
}

function _checkLocalStorage() {
    if (typeof (Storage) == "undefined") {
        alert("很遗憾，您的浏览器不支持LocalStorage！");
    }
}

function storeToken(token) {
    _checkLocalStorage();
    localStorage.setItem('token', token);
}

function getToken() {
    _checkLocalStorage();
    return localStorage.getItem('token');
}
