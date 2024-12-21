import { createRouter, createWebHistory } from 'vue-router'
import ArticleForm from '../components/ArticleForm.vue'
import ArticlePreview from '../components/ArticlePreview.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: ArticleForm
  },
  {
    path: '/preview',
    name: 'preview',
    component: ArticlePreview
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 