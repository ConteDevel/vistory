<template>
    <div>
        <div v-for="item in items" class="box">
            <div class="card-content">
                <div class="media">
                    <div class="media-left">
                        <figure class="image is-48x48">
                            <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image">
                        </figure>
                    </div>
                    <div class="media-content">
                        <p class="title is-4">{( item.first_name + ' ' + item.last_name )}</p>
                        <p class="subtitle is-6">{( item.email )}</p>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
    module.exports = {
        beforeMount() {
            axios.get('/api/users').then(response => {
                let page = JSON.parse(response.data);
                this.items = page.items;
            });
        },
        delimiters: ['{(', ')}'],
        data: function () {
            return {
                items: []
            }
        }
    }
</script>