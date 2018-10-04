<template>
    <div class="tile is-ancestor">
        <div v-for="item in items" class="tile is-parent">
            <article class="tile is-child">
                <div class="box">
                    <div class="card-image">
                        <figure class="image is-4by3" style="max-height: 320px;">
                            <img :src="fs_url + item.attachment_id + '/file'" alt="Placeholder image"
                                 style="object-fit: cover;">
                        </figure>
                    </div>
                    <div class="card-content">
                    </div>
                    <div class="card-footer">
                        <a href="#" class="card-footer-item">Like: {( item.likes )}</a>
                    </div>
                </div>
            </article>
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