<template>
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info" class="tertiary2">
            <b-navbar-brand href="/">
                <img width="50px" height="50px" src="../assets/logo2.png">
            </b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav class="float-right">
                    <b-nav-item @click="preProcessData()">Preprocess</b-nav-item>
                    <b-nav-item @click="generateTags()">Generate Tags</b-nav-item>
                    <b-nav-item href="/topics">Topics</b-nav-item>
                    <b-nav-item href="/wordcloud">Word Cloud</b-nav-item>
                    <b-nav-item href="/similarity">Similarity</b-nav-item>
                </b-navbar-nav>


            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Navbar",
        methods: {
            async generateTags() {
                let prompt = confirm("Generating tags can change data in the system, and may take some time to process.");
                if (prompt) {
                    const path = 'http://localhost:5000/tags';
                    return await axios.get(path)
                        .then((res) => {
                            alert(res.data.status)
                        })
                        .catch((error) => {
                            // eslint-disable-next-line
                            console.error(error);
                        });
                }
            },
            async preProcessData() {
                let prompt = confirm("Preprocessing can change data in the system, and may take some time to process.");
                if (prompt) {
                    const path = 'http://localhost:5000/preprocess';
                    return await axios.get(path)
                        .then((res) => {
                            alert(res.data.status)
                        })
                        .catch((error) => {
                            // eslint-disable-next-line
                            console.error(error);
                        });

                }
            }
        }
    }
</script>

<style scoped>

</style>