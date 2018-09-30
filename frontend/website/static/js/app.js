function getHost() {
    let arr = window.location.href.split("/");
    return arr[0] + "//" + arr[2]
}

Vue.component('main-menu', {
    beforeMount() {
        window.hasAccessToken = initOAuth2();
    },
    data: function () {
        return {
            signed: window.hasAccessToken
        }
    },
});

let app = new Vue({
    beforeMount() {
        window.hasAccessToken = initOAuth2();
    },
    el: '#app',
    data: {
        message: window.hasAccessToken ? 'Hello, User!' : 'Hello, Anonymous!'
    }
});
