import Vue from 'vue';
import Router from 'vue-router';
import UploadData from "../components/UploadData";
import Stories from "../components/Stories";
import Similarity from "../components/Similarity";
import TopicModeling from "../components/TopicModeling";
import WordCloud from "../components/WordCloud";

// import Temp from "../assets/lda.html"

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'Stories',
    component: Stories,
  },
  {
    path: '/topics',
    name: 'TopicModel',
    component: TopicModeling,
  },
  {
    path: '/similarity',
    name: 'Similarity',
    component: Similarity,
  },
  {
    path: '/wordcloud',
    name: 'WordCloud',
    component: WordCloud,
  },
  {
    path: '/upload',
    name: 'UploadData',
    component: UploadData,
  },
  // {
  //   path: '/temp',
  //   name: 'Temp',
  //   component: {template: Temp},
  // }

]

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
