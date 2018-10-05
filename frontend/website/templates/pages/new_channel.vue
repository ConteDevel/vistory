{% from "helpers/_form_helper.html" import render_field %}
<template>
    <div class="box">
        <div class="box-content">
            <form id="new_channel" method="post" v-on:submit.prevent="postValues" enctype="application/x-www-form-urlencoded">
                {{ form.csrf_token }}
                {{ render_field(form.name) }}
                {{ render_field(form.description) }}
                <div class="field vi-offset-top-sm">
                    <p class="control">
                        <button type="submit" class="button is-success">Create</button>
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
                name: '',
                description: ''
            }
        },
        methods: {
            'postValues': async function () {
                let config = {
                    headers: {
                        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                    }
                };
                let form = document.getElementById('new_channel');
                let formData = new FormData(form);
                let response = await axios.post('/pages/new_channel.vue', formData, config);
                console.log(response);
            }
        }
    }
</script>