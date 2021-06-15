<script>
    import axios from 'axios';

    const isDev = true;
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

    export function ajaxPost(shortUrl, data, success) {
        axios.post(_concat(shortUrl), data).then(resp => {
            if (success) {
                success(resp.data);
            }
        }).catch(error => {
            alert("无法连接到服务器，请检查网络连接！");
        });
    }

    function _checkLocalStorage() {
        if (typeof (Storage) == "undefined") {
            alert("很遗憾，您的浏览器不支持LocalStorage！");
        }
    }

    export function storeToken(token) {
        _checkLocalStorage();
        localStorage.setItem('token', token);
    }

    export function getToken() {
        _checkLocalStorage();
        return localStorage.getItem('token');
    }
</script>
