<template>
  <div class="container w-100" >
    <h1 class="header">Topic Model</h1>
    <hr>
    <div class="container alert tertiary3">
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
      
    </div> 
    <div v-if="topics > 0" class="container">
      
   
      <TopicStories v-bind:topics="topics"/>
    </div> 
</div>
</template>

<script>
    import TopicModel from "../components/TopicModel";
    import TopicStories from "../components/TopicStories";

    export default {
        components: {TopicModel, TopicStories},
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
