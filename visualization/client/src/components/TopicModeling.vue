<template>
<div class="container">
  <div class="container alert alert-success">
    <form>
      <div class="form-group">
        <label for="NumberOfTopics">Number Of Topics</label>
        <input
          class="form-control"
          id="NumberOfTopics"
        />
      </div>
      <button type="submit" class="btn btn-primary">Analyze</button>
    </form>
  </div>
    <TopicModel/>
</div>
</template>

<script>
import TopicModel from "../components/TopicModel";
//import axios from "axios";
export default {
  components: {TopicModel},
  name: "TopicModeling"
  // data() {
  //     return {
  //       // status: "",
  //         // url: require('./../assets/lda.html')
  //     };
  // },
  // async created() {
  //     await this.runTopicModel();
  // },
  // methods: {
  //     runTopicModel() {
  //         const path = 'http://localhost:5000/stories';
  //         return axios.get(path)
  //             .then((res) => {
  //                 this.status = res.data.status;
  //             })
  //             .catch((error) => {
  //                 // eslint-disable-next-line
  //                 console.error(error);
  //             });

  //     },
  // },
};
</script>
