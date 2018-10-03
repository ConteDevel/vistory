<template>
    <div>
        <div v-for="item in items" class="box">
            <div class="card-image">
                <figure class="image is-4by3">
                    <img :src="fs_url + item.attachment_id + '/file'" alt="Placeholder image">
                </figure>
            </div>
            <div class="card-content">
                <div class="content">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    Phasellus nec iaculis mauris. <a>@bulmaio</a>.
                    <a href="#">#css</a> <a href="#">#responsive</a>
                    <br>
                    <time>{( item.updated_at )}</time>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    module.exports = {
        beforeMount() {
            axios.get('/api/posts').then(response => {
                let page = JSON.parse(response.data);
                this.items = page.items;
            });
        },
        delimiters: ['{(', ')}'],
        data: function () {
            return {
                items: [],
                fs_url: '{{ config['FS_SERVICE'] + '/api/images/' }}'
            }
        }
    }
</script>