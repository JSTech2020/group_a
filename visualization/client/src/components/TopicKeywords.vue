<template>
  <div class="container">Topic Keywords {{ topic_id }} {{ num_topics }}</div>
</template>

<script>
import axios from "axios";
export default {
  name: "TopicKeywords",
  props: {
    topic_id: Number,
    num_topics: Number
  },
  data() {
    return {
      current_topic: 0,
      keywords: []
    };
  },
  created: function() {
    const path =
      "http://localhost:5000/topic_model_word_cloud?num_topics=" +
      this.num_topics.toString() +
      "&topic_id=" +
      (this.topic_id -1).toString();
    axios
      .get(path)
      .then(res => {
        this.keywords = res.data;
        console.log(JSON.parse(this.keywords));
      })
      .catch(error => {
        // eslint-disable-next-line
        console.error(error);
      });
  },

  methods: {}
};
</script>

<style scoped></style>
