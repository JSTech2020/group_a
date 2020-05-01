<template>
<div class="container">
  <div class="container alert alert-success">
      <div class="form-group">
        <label for="NumberOfTopics">Number Of Topics</label>
        <input
          class="form-control"
          type="number"
          id="NumberOfTopics"
          v-model.number="topics_input"
        />
      </div>
      <button @click="calltopicModeling()" class="btn btn-primary">Analyze</button>
  </div>
    <div v-if="topics > 0" class="container">
    <TopicModel v-bind:topics="topics"/>
    <TopicStories v-bind:topics="topics"/>
    </div> 
</div>
</template>

<script>
import TopicModel from "../components/TopicModel";
import TopicStories from "../components/TopicStories";
export default {
  components: {TopicModel,TopicStories},
  name: "TopicModeling",
  data() {
            return {
                topics_input: 10,
                topics: 0
            };
        },
  // data() {
  //     return {
  //       // status: "",
  //         // url: require('./../assets/lda.html')
  //     };
  // },
  // async created() {
  //     await this.runTopicModel();
  // },
  methods: {
      calltopicModeling() {
         this.topics = this.topics_input

      },
  },
};
</script>
