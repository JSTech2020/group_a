import Vue from 'vue';
import Router from 'vue-router';
import Stories from "../components/Stories";
import Similarity from "../components/Similarity";
import TopicModel from "../components/TopicModel";

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
    component: TopicModel,
  },
  {
    path: '/similarity',
    name: 'Similarity',
    component: Similarity,
  }
]

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
