document.addEventListener('DOMContentLoaded', function() {
    var burger = document.querySelector(".navbar-burger");
    burger.addEventListener('click', function() {
        burger.classList.toggle("is-active");
        var menu = document.querySelector(".navbar-menu");
        menu.classList.toggle("is-active");
    });
});

let rightMenuItem = {
    delimiters: ['{(', ')}'],
    template: '#right-menu-item',
    props: ['title', 'icon', 'active', 'index', 'listener'],
    methods: {
        toggleRowActive() {
            this.$emit('newactive', this.index);
            this.listener(this.index);
        }
    }
};

let app = new Vue({
    delimiters: ['{(', ')}'],
    beforeMount() {
        window.hasAccessToken = initOAuth2();
        this.signed = window.hasAccessToken;
        this.mainTitle = this.sections[this.selectedIndex].title;
        if (this.signed) {
            getMe().then(response => (console.log(response)));
        }
    },
    el: '#page',
    components: {
        'right-menu-item': rightMenuItem
    },
    data: {
        signed: window.hasAccessToken,
        sections: [
            {id: 'profile', title: 'Profile', icon: 'fa-user'},
            {id: 'posts', title: 'Posts', icon: 'fa-images'},
            {id: 'people', title: 'People', icon: 'fa-users'},
            {id: 'channels', title: 'Channels', icon: 'fa-stream'}
        ],
        selectedIndex: 1,
        mainTitle: null,
        searchRequest: null,
        content: ''
    },
    methods: {
        loadPage: function(title, url) {
            this.mainTitle = title;
            axios.get(url)
                .then(response => (this.content = response.data));
        },
        /**
        * On right menu item selected listener
        */
        onItemSelected: function(index) {
            this.selectedIndex = index;
            let title = this.sections[index].title;
            let id = this.sections[index].id;
            this.loadPage(title, '/pages/' + id);
        },
        onSearch: function() {
            if (this.searchRequest) {
                let title = 'Search results for \"' + this.searchRequest + '\"...';
                this.loadPage(title, '/pages/search_results');
            }
        },
        onNewPost: function() {
            this.loadPage('New post', '/pages/new_post');
        },
        onNewChannel: function() {
            this.loadPage('New channel', '/pages/new_channel');
        }
    }
});
