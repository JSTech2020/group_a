<template>
    <div id="zs-nav">
        <b-navbar toggleable="lg" type="dark" variant="info" class="tertiary2">
            <b-navbar-brand href="/">
                <img width="50px" height="50px" src="../assets/logo2.png">
            </b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item href="/"
                                v-bind:class="(isActive==='home')?'active':''">
                        Home
                    </b-nav-item>
                    <b-nav-item href="/topics"
                                v-bind:class="(isActive==='topics')?'active':''">
                        Topics
                    </b-nav-item>
                    <b-nav-item href="/wordcloud"
                                v-bind:class="(isActive==='wordcloud')?'active':''">
                        Word Cloud
                    </b-nav-item>
                    <b-nav-item href="/similarity"
                                v-bind:class="(isActive==='similarity')?'active':''">
                        Similarity
                    </b-nav-item>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-item href="/upload"
                                v-bind:class="(isActive==='upload')?'active':''">
                        Upload File
                    </b-nav-item>
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

        <div v-if="isWaiting"
             class="container">
            <span class="mt-3 mb-3 form-inline text-center alert alert-warning">
                <b-spinner small></b-spinner>
                <h5 class="ml-4"> {{ waitMsg }}</h5>
            </span>
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
                isWaiting: false,
                waitMsg: "",
                isActive: "home"
            }

        },
        async created() {
            this.errors = [];
            this.isWaiting = false
            this.waitMsg = ""
            this.setActiveTab()
            await this.checkForErrors();
        },
        methods: {
            checkForErrors() {
                this.errors = [];
                const path = 'http://localhost:5000/check_db';

                this.isWaiting = true
                this.waitMsg = "Checking server status. Please wait ..."
                return axios.get(path)
                    .then((res) => {
                        if (res.data.status === "fail") {
                            let temp = res.data.errors
                            for (let e in temp) {
                                this.errors.push(temp[e]);
                            }
                        }
                        this.isWaiting = false
                        this.waitMsg = ""
                    })
                    .catch((error) => {

                        // eslint-disable-next-line
                        console.error(error);
                        this.errors.push(error)
                        this.isWaiting = false
                        this.waitMsg = ""
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
                        self.isWaiting = true
                        self.waitMsg = "Generating Tag. Please wait ..."
                        return await axios.get(path)
                            .then((res) => {
                                if (res.data.status === "success") {
                                    self.$swal.fire(
                                        'Success!',
                                        'Tags generated successfully!',
                                        'success'
                                    ).then(() => document.location.href = "/")
                                }
                                self.isWaiting = false
                                self.waitMsg = ""
                            })
                            .catch((error) => {
                                // eslint-disable-next-line
                                console.error(error);
                                self.isWaiting = false
                                self.waitMsg = ""
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
                        self.isWaiting = true
                        self.waitMsg = "Pre-processing data. Please wait ..."
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
            },
            setActiveTab(){
                this.isActive = "home";
                let urlList = window.location.href.split('/')
                // let str = urlList[urlList.length-2]
                if(
                    urlList[urlList.length-1] === "" ||
                    urlList[urlList.length-1] === undefined ||
                    urlList[urlList.length-1] === null
                ){
                    this.isActive = "home";
                }else{
                    this.isActive = urlList[urlList.length-1];
                }

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

