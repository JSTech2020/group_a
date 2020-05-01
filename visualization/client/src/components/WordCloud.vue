<template>
    <div class="container">
        <h1 class="header">Word Cloud</h1>
        <hr>
        <div id="wordcloud-search"
             class="form-inline justify-content-center">
            <select class="form-control"
                    v-model="selected_id"
                    @change="getWordCloud()">
                <option v-for="story in stories"
                        v-bind:key="story.id"
                        v-bind:value="story.id">
                    {{story.title}}
                </option>
            </select>

            <a class="btn bg-primary2"
               v-bind:href="imgStr"
               v-bind:download="getFileName()"
                    @click="exportImage()">
                Export
            </a>
        </div>

        <div class="container">
            <img id="imgWordCloud"
                 v-bind:src="imgStr"
                 class="img-fluid img-thumbnail rounded mx-auto d-block"
                 alt="Word Cloud Image"

            />
        </div>

    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "WordCloud",
        data() {
            return {
                stories: [],
                selected_id: 0,
                status: "",
                imgStr: "",
            };
        },
        async created() {
            await this.getStories();
            await this.getWordCloud();
        },
        methods: {
            getStories() {
                const path = 'http://localhost:5000/stories';
                return axios.get(path)
                    .then((res) => {
                        this.stories = res.data.stories;
                        this.selected_id = this.stories[0]['id']
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });
            },
            getWordCloud() {
                const path = 'http://localhost:5000/tags/word_cloud/' + this.selected_id;
                return axios.get(path)
                    .then((res) => {
                        this.status = res.data.status;
                        if (this.status === "success") {
                            let temp = res.data.imgStr;
                            this.imgStr = 'data:image/png;base64,' + temp.substring(2, temp.length - 3)
                        } else {
                            alert("Error: " + res.data.error)
                        }


                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });
            },
            getFileName() {
                return "WORDCLOUD_" + this.selected_id + "_" + Date.now() + ".png"; //File name Here
            }
        },
    }
</script>

<style scoped>
    #imgWordCloud {
        margin-top: 50px;
    }

    #wordcloud-search {
        margin-top: 10px;
        padding-left: 20px;
    }

    .btn {
        margin-left: 2px;
        margin-right: 2px;
    }
</style>