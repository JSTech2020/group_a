<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Stories for Topic</h1>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Document No</th>
              <th scope="col">Story ID</th>
              <th scope="col">Topic_Perc_Contrib</th>
              <th scope="col">Title</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(story, index) in stories" :key="index">
              <td>{{ story.Document_No }}</td>
              <td>{{ story.Title }}</td> <!-- title -> id -->
              <td>{{ story.Topic_Perc_Contrib }}</td>
              <td>{{ story.Abstract }}</td><!-- abstract -> title -->
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn bg-secondary btn-sm"
                    v-b-modal.story-modal
                    @click="getStory(story.Title)"
                  >
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
            <td scope="row">Title:</td>
            <td>{{story.title}}</td>
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

export default {
  name: "TopicStory",
  props: {
    topic_id: Number,
    num_topics: Number
  },
  data() {
    return {
      story: {
        id:"",
        title:"",
        abstract: "",
      },
      stories: []
    };
  },
  async created() {
    await this.getStories();
  },
  methods: {
    getStories() {
       const path =
      "http://localhost:5000/topic_model_stories?num_topics=" +
      this.num_topics.toString() +
      "&topic_id=" +
      (this.topic_id -1).toString();
      return axios
        .get(path)
        .then(res => {
          this.stories = JSON.parse(res.data.topics);
          console.log(this.stories[1])
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    async getStory(id) {
      const path = "http://localhost:5000/stories/" + id;
      await axios
        .get(path)
        .then(res => {
          this.story = res.data.story[0];
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  } 
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}
</style>
