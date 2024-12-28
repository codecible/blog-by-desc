import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ArticleForm from '@/components/ArticleForm.vue'
import XiaohongshuForm from '@/components/XiaohongshuForm.vue'
import XiaohongshuPreviewView from '@/views/XiaohongshuPreviewView.vue'
import ArticlePreviewView from '@/views/ArticlePreviewView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/article',
    name: 'article',
    component: ArticleForm
  },
  {
    path: '/article/preview/:id',
    name: 'article-preview',
    component: ArticlePreviewView
  },
  {
    path: '/xiaohongshu',
    name: 'xiaohongshu',
    component: XiaohongshuForm
  },
  {
    path: '/xiaohongshu/preview/:id',
    name: 'xiaohongshu-preview',
    component: XiaohongshuPreviewView
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes
})

export default router
