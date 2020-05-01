<template>
  <div class="container">
    <ul class="nav nav-tabs">
      <li v-for="index in parseInt(topics)" :key="index" class="nav-item">
        <a
          class="nav-link"
          @click.prevent="setActive(index)"
          :class="{ active: isActive(index) }"
          :href="index"
          >Topic {{ index }}</a
        >
      </li>
    </ul>

    <div class="tab-content py-3" id="myTabContent">
      <div v-for="index in parseInt(topics)" :key="index" class="tab-pane fade" :class="{ 'active show': isActive(index) }" :id=index>
        <TopicKeywords v-bind:num_topics="topics" v-bind:topic_id="index"/>
        <TopicStory v-bind:num_topics="topics" v-bind:topic_id="index"/>
      </div>
      
    </div>
  </div>
</template>

<script>
import TopicKeywords from "../components/TopicKeywords";
import TopicStory from "../components/TopicStory";
export default {
  name: "TopicStories",
  components: {TopicKeywords,TopicStory},
  props: {
    topics: Number
  },
  data() {
    return {
      current_topic: 0
    };
  },
  methods: {
    isActive(menuItem) {
      return this.current_topic === menuItem;
    },
    setActive(menuItem) {
      this.current_topic = menuItem;
    }
  }
};
</script>

<style scoped></style>
