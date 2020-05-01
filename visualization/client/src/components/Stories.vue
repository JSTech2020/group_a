<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-10">
                <h1>Stories</h1>
                <hr>
                <export-data class="btn bg-primary pointer-event "
                             v-bind:data="stories"
                             v-bind:name="getExportName()"
                             v-bind:delimiter="';'"
                             v-bind:encoding="'utf-8'"
                             v-bind:labels="['id','title','related_story_id', 'tags']"
                             type="button"
                             role="button">
                    Export
                </export-data>
                <hr>

                <table class="table table-hover">
                    <thead>
                    <tr>
                        <th scope="col">S.N.</th>
                        <th scope="col">Story ID</th>
                        <th scope="col">Title</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="(story, index) in stories" :key="index">
                        <td>{{index+1}}</td>
                        <td>{{story.id}}</td>
                        <td>{{story.title}}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button type="button"
                                        class="btn bg-secondary btn-sm"
                                        v-b-modal.story-modal
                                        @click="getStory(story.id)">
                                    Detail
                                </button>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <b-modal ref="showStoryDetail"
                 id="story-modal"
                 size="lg"
                 hide-footer
                 v-bind:title="story.title">
            <div class="responsive">
                <table class="table table-striped table-condensed">
                    <tbody>
                        <tr>
                            <td scope="row">Story Id:</td>
                            <td>{{story.id}}</td>
                        </tr>
                        <tr>
                            <td scope="row">Tags:</td>
                            <td>{{listToString(story.tags)}}</td>
                        </tr>
                        <tr>
                            <td scope="row">Related Story Ids:</td>
                            <td>{{listToString(story.related_story_id)}}</td>
                        </tr>
                        <tr>
                            <td scope="row">Abstract:</td>
                            <td>{{story.abstract}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </b-modal>
    </div>
</template>

<script>
    import axios from "axios";
    import JsonCSV from 'vue-json-csv'

    export default {
        name: "Stories",
        components: {
            "export-data": JsonCSV,
        },
        data() {
            return {
                stories: [],
                similarities: [],
                story: {},
                tags: [],
            };
        },
        async created() {
            await this.getStories();
            await this.getSimilarStories();
            await this.updateStories();
        },
        methods: {
            getStories() {
                const path = 'http://localhost:5000/stories';
                return axios.get(path)
                    .then((res) => {
                        this.stories = res.data.stories;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });
            },
            async getStory(id) {
                const path = 'http://localhost:5000/stories/' + id;
                await axios.get(path)
                    .then((res) => {
                        this.story = res.data.story[0];
                        let temp = this.stories.find(x => x.id === this.story.id)
                        if (temp !== null && temp !== undefined) {
                            this.story.related_story_id = temp.related_story_id;
                            this.story.tags = temp.tags;
                        }
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });

            },
            getSimilarStories() {
                const path = 'http://localhost:5000/similarities';
                return axios.get(path)
                    .then((res) => {
                        this.similarities = res.data.similarities;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });
            },
            updateStories() {
                let temp = [];
                for (let i = 0; i < this.stories.length; i++) {
                    temp.push({
                        ...this.stories[i],
                        'related_story_id': this.similarities[i]['related_story_id'],
                        'tags': this.similarities[i]['tags']
                    })
                }
                this.stories = temp;
                return temp;
            },
            getExportName() {
                return "Export_" + Date.now() + ".csv";
            },
            listToString(li) {
                if (li !== null && li !== undefined && li !== []) {
                    return li.join(", ");
                }else{
                    return ""
                }
            }
        },
    }
</script>

<style scoped>
    .container {
        margin-top: 20px;
    }
</style>