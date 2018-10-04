{% from "helpers/_form_helper.html" import render_field %}
<template>
    <div class="box">
        <div class="box-content">
            <form id="new_post" method="post" v-on:submit.prevent="postValues" enctype="multipart/form-data">
                {{ form.csrf_token }}
                {{ form.channel_id }}
                {{ render_field(form.description) }}
                {{ render_field(form.file) }}
                <div class="field vi-offset-top-sm">
                    <p class="control">
                        <button type="submit" class="button is-success">Post</button>
                    </p>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
    module.exports = {
        delimiters: ['{(', ')}'],
        data: function () {
            return {
                description: '',
                channel_id: '',
                attachment: null
            }
        },
        methods: {
            'postValues': async function () {
                let rawData = JSON.stringify({
                    description: this.description,
                    channel_id: this.channel_id
                });
                let form = document.getElementById('new_post');
                let formData = new FormData(form);
                //formData.append('file', this.attachment, this.attachment.name);
                //formData.append('data', rawData);
                console.log(formData);
                let response = await axios.post('/pages/new_post.vue', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                console.log(response);
            },
            'processFile': function(event) {
                this.attachment = event.target.files[0];
            }
        }
    }
</script>