<template>
  <div class="container">
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a class="nav-link active" href="#">Topic 1</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Topic 2</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Topic 3</a>
      </li>
      <li class="nav-item">
        <a class="nav-link disabled" href="#">Topic 4</a>
      </li>
    </ul>
  </div>
</template>



<script>

    export default {
        name: "TopicStories",
        props: {
        topics: String,
        },
        data() {
            return {
            
            };
        },
        methods: {
            // runTopicModel() {
            //     const path = 'http://localhost:5000/topic_model';
            //     return axios.get(path)
            //         .then((res) => {
            //             let parser = new DOMParser();
            //             this.input = parser.parseFromString(res.data, "text/html");

            //         })
            //         .catch((error) => {
            //             // eslint-disable-next-line
            //             console.error(error);
            //         });

            // },
        },

    }
</script>

<style scoped>

</style>