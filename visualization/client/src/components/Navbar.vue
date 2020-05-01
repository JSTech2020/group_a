<template>
    <div id="zs-nav">
        <b-navbar toggleable="lg" type="dark" variant="info" class="tertiary2">
            <b-navbar-brand href="/">
                <img width="50px" height="50px" src="../assets/logo2.png">
            </b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item href="/topics">Topics</b-nav-item>
                    <b-nav-item href="/wordcloud">Word Cloud</b-nav-item>
                    <b-nav-item href="/similarity">Similarity</b-nav-item>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-item href="/upload">Upload File</b-nav-item>
                    <b-nav-item @click="preProcessData()">Preprocess</b-nav-item>
                    <b-nav-item @click="generateTags()">Generate Tags</b-nav-item>
                </b-navbar-nav>


            </b-collapse>
        </b-navbar>

        <div class="error bg-warning" v-if="errors.length>0">
            <h1 class="text-danger">Error</h1>
            <ul class="list-group">
                <li v-for="(error,index) in errors"
                    v-bind:key="index">
                    {{ error }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Navbar",
        data() {
            return {
                errors: [],
            }

        },
        async created() {
            this.errors = [];
            await this.checkForErrors();
        },
        methods: {
            checkForErrors() {
                this.errors = [];
                const path = 'http://localhost:5000/check_db';
                return axios.get(path)
                    .then((res) => {
                        if (res.data.status === "fail") {
                            let temp = res.data.errors
                            for (let e in temp) {
                                this.errors.push(temp[e]);
                            }

                        }
                    })
                    .catch((error) => {

                        // eslint-disable-next-line
                        console.error(error);
                        this.errors.push(error)
                    });
            },
            generateTags() {
                let self = this
                self.$swal({
                    title: 'Are you sure?',
                    text: "Generating tags can change data in the system, and may take some time to process.",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Yes'
                }).then(async (result) => {
                    if (result.value) {
                        const path = 'http://localhost:5000/tags';
                        return await axios.get(path)
                            .then((res) => {
                                if (res.data.status === "success") {
                                    self.$swal.fire(
                                        'Success!',
                                        'Tags generated successfully!',
                                        'success'
                                    ).then(() => document.location.href = "/")
                                }
                            })
                            .catch((error) => {
                                // eslint-disable-next-line
                                console.error(error);
                            });
                    }
                })


            },
            async preProcessData() {
                let self = this
                self.$swal({
                    title: 'Are you sure?',
                    text: "Preprocessing can change data in the system, and may take some time to process.",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Yes'
                }).then(async (result) => {
                    if (result.value) {
                        const path = 'http://localhost:5000/preprocess';
                        return await axios.get(path)
                            .then((res) => {
                                if (res.data.status === "success") {
                                    self.$swal(
                                        'Success!',
                                        'Data processed successfully!',
                                        'success'
                                    ).then(() => document.location.href = "/")
                                }
                            })
                            .catch((error) => {
                                // eslint-disable-next-line
                                console.error(error);
                            });
                    }
                })
            }
        }
    }
</script>

<style scoped>
    #zs-nav {
        font-size: 18px;
    }

    .error {
        padding: 10px;
    }

</style>

