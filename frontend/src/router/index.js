import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import ArticleForm from '../components/ArticleForm.vue'
import XiaohongshuForm from '../components/XiaohongshuForm.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/article',
    name: 'article',
    component: ArticleForm
  },
  {
    path: '/xiaohongshu',
    name: 'xiaohongshu',
    component: XiaohongshuForm
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
