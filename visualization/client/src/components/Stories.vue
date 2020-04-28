<template>
    <div class="container">

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

        </div>


        <div class="row">
            <div class="col-sm-10">
                <h1>Stories</h1>
                <hr>
                <table class="table table-hover">
                    <thead>
                    <tr>
                        <th scope="col">S.N.</th>
                        <th scope="col">Title</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="(story, index) in stories" :key="index">
                        <td>{{index+1}}</td>
                        <td>{{story.title}}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button type="button"
                                        class="btn btn-info btn-sm"
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
                 v-bind:title="story.title"
                 hide-footer>
            id: {{story.id}}<br/>
            title: {{story.title}}<br/>
            abstract:<br>
            {{story.abstract}}
        </b-modal>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Stories",
        data() {
            return {
                stories: [],
                story:{}
            };
        },
        created() {
            this.getStories();
        },
        methods: {
            getStories() {
                const path = 'http://localhost:5000/stories';
                axios.get(path)
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
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });

            }
        }
    }
</script>

<style scoped>

</style>