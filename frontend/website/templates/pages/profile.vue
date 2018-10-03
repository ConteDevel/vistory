<template>
    <div class="card">
        <div class="card-content">
            <div class="media">
                <div class="media-left">
                    <figure class="image is-48x48">
                        <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image">
                    </figure>
                </div>
                <div class="media-content">
                    <p class="title is-4">{( me.first_name + ' ' + me.last_name )}</p>
                    <p class="subtitle is-6">{( me.email )}</p>
                    <p class="subtitle is-6">
                        <strong>Role: </strong>{( me.role )}<br/>
                        <strong>Gender: </strong>{( me.gender )}<br/>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    module.exports = {
        beforeMount() {
            getMe().then(response => {
                this.me = JSON.parse(response.data);
                console.log(this.me);
            });
        },
        delimiters: ['{(', ')}'],
        data: function () {
            return {
                me: {}
            }
        }
    }
</script>