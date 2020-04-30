<template>
    <div>
        <router-link
                to="/similarity"
        >
            Similarity
        </router-link>

        <br>

        <router-link
                to="/topics"
        >
            Topic Model
        </router-link>

        <!-- Insert stories component -->
        <stories></stories>

    </div>


</template>

<script>
    import Stories from "../components/Stories";

    export default {
        name: "Main",
        components:{
            "stories": Stories,
        }
    }
</script>

<style scoped>

</style>