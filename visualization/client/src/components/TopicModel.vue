<template>
    <div class="container">

        <div class="embed-responsive embed-responsive-16by9">
<!--            we can keep scrolling=no but it hampers responsievness of app -->
            <iframe class="embed-responsive-item"
                    src="http://localhost:5000/topic_model"
                    allowfullscreen></iframe>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "TopicModel",
        data() {
            return {
                status: "",
                input: "test",
            };
        },
        async created() {
            // await this.runTopicModel();
            // await this.loadFile();
        },
        computed: {
            compiledHtml: function() {
                return this.input;
            }
        },
        methods: {
            runTopicModel() {
                const path = 'http://localhost:5000/topic_model';
                return axios.get(path)
                    .then((res) => {
                        let parser = new DOMParser();
                        this.input = parser.parseFromString(res.data, "text/html");

                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });

            },
        },

    }
</script>

<style scoped>

</style>