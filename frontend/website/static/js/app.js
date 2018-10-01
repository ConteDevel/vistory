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
        mainTitle: null
    },
    methods: {
        /**
        * On right menu item selected listener
        */
        onItemSelected(index) {
            this.selectedIndex = index;
            this.mainTitle = this.sections[index].title
        }
    }
});
