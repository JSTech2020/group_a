<template>
  
<wordcloud
      :data="keywords"
      nameKey="word"
      valueKey="prob"
      color="Accent"
    >
      </wordcloud>


</template>

<script>
import axios from "axios";
import wordcloud from 'vue-wordcloud'
export default {
  name: "TopicKeywords",
  components: {
    wordcloud
  },
  props: {
    topic_id: Number,
    num_topics: Number
  },
  data() {
    return {
      current_topic: 1,
      keywords: [],
      defaultWords: [{
          "name": "Cat",
          "value": 26
        },
        {
          "name": "fish",
          "value": 19
        },
        {
          "name": "things",
          "value": 18
        },
        {
          "name": "look",
          "value": 16
        },
        {
          "name": "two",
          "value": 15
        },
        {
          "name": "fun",
          "value": 9
        },
        {
          "name": "know",
          "value": 9
        },
        {
          "name": "good",
          "value": 9
        },
        {
          "name": "play",
          "value": 6
        }
      ]
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
        this.keywords = res.data.topics;
        console.log(this.keywords[1].word);
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
