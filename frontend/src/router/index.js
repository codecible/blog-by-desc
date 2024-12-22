import { createRouter, createWebHistory } from 'vue-router'
import ArticleForm from '../components/ArticleForm.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: ArticleForm
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 