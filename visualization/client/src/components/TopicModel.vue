<template>
    <div class="container">
<!--        {{status}}-->
<!--        <iframe v-bind:src="url" height="500" width="500"></iframe>-->
    </div>
</template>

<script>
    import axios from "axios";
    export default {
        name: "TopicModel",
        data() {
            return {
                status: "",
                // url: require('./../assets/lda.html')
            };
        },
        async created() {
            await this.runTopicModel();
        },
        methods: {
            runTopicModel() {
                const path = 'http://localhost:5000/stories';
                return axios.get(path)
                    .then((res) => {
                        this.status = res.data.status;
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