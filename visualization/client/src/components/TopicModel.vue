<template>
    <div style="
    max-width: 1600px;
" >
       
        <iframe class="embed-responsive-item" v-bind:src="src" sandbox="allow-scripts" style="
    width: 115%;
    height: 880px;
    margin-left: -71px;
"  allowfullscreen noborder></iframe>
    

<!--        <div v-html="compiledHtml.outerHTML">-->
<!--        </div>-->
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "TopicModel",
        props: {
        topics: Number,
        },
        data() {
            return {
                src: "http://localhost:5000/topic_model?num_topics=" + this.topics.toString(),
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