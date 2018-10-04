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
            getMe().then(response => {
                if (response.status === 200) {
                    let user = JSON.parse(response.data);
                    if (user.type === 'user') {
                        this.username = user.first_name + ' ' + user.last_name;
                    }
                }
            });
        }
    },
    el: '#page',
    components: {
        'right-menu-item': rightMenuItem,
        'profile': httpVueLoader('/pages/profile.vue'),
        'posts': httpVueLoader('/pages/posts.vue'),
        'people': httpVueLoader('/pages/people.vue'),
        'channels': httpVueLoader('/pages/channels.vue'),
        'search_results': httpVueLoader('/pages/search_results.vue'),
        'new_post': httpVueLoader('/pages/new_post.vue'),
        'new_channel': httpVueLoader('/pages/new_channel.vue'),
    },
    data: {
        signed: window.hasAccessToken,
        username: 'User',
        sections: [
            {id: 'profile', title: 'Profile', icon: 'fa-user'},
            {id: 'posts', title: 'Posts', icon: 'fa-images'},
            {id: 'people', title: 'People', icon: 'fa-users'},
            {id: 'channels', title: 'Channels', icon: 'fa-stream'}
        ],
        selectedIndex: 1,
        mainTitle: null,
        searchRequest: null,
        content: 'posts'
    },
    methods: {
        signOut: function() {
            if (localStorage.hasOwnProperty('access_token')) {
                localStorage.removeItem('access_token');
            }
            if (localStorage.hasOwnProperty('refresh_token')) {
                localStorage.removeItem('refresh_token');
            }
            window.location.reload();
        },
        loadPage: function(title, id) {
            this.mainTitle = title;
            this.content = id;
        },
        /**
        * On right menu item selected listener
        */
        onItemSelected: function(index) {
            this.selectedIndex = index;
            let title = this.sections[index].title;
            let id = this.sections[index].id;
            this.loadPage(title, id);
        },
        onSearch: function() {
            if (this.searchRequest) {
                let title = 'Search results for \"' + this.searchRequest + '\"...';
                this.loadPage(title, 'search_results');
            }
        },
        onNewPost: function() {
            this.loadPage('New post', 'new_post');
        },
        onNewChannel: function() {
            this.loadPage('New channel', 'new_channel');
        }
    }
});
