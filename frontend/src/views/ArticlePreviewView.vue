<template>
  <div class="preview-page">
    <div class="header">
      <router-link to="/article" class="back-button">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M20 11H7.83L13.42 5.41L12 4L4 12L12 20L13.41 18.59L7.83 13H20V11Z" fill="currentColor"/>
        </svg>
        返回编辑
      </router-link>
      <h1>生成结果</h1>
    </div>

    <article-preview
      v-if="articleData"
      :article-data="articleData"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import ArticlePreview from '../components/ArticlePreview.vue'

const router = useRouter()
const route = useRoute()
const articleData = ref(null)

onMounted(() => {
  // 从 URL query 参数中获取数据
  const queryData = route.query.data
  if (queryData) {
    try {
      articleData.value = JSON.parse(queryData)
    } catch (error) {
      console.error('解析数据失败:', error)
      router.replace('/article')
    }
  } else {
    // 如果没有数据，返回表单页面
    router.replace('/article')
  }
})
</script>

<style scoped>
.preview-page {
  min-height: 100vh;
  padding: 20px;
  background: var(--background-color);
}

.header {
  max-width: 900px;
  margin: 0 auto 40px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text-color);
  font-weight: 500;
  transition: all 0.3s ease;
}

.back-button:hover {
  transform: translateX(-2px);
}

h1 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-color);
}

@media (max-width: 768px) {
  .preview-page {
    padding: 10px;
  }

  .header {
    margin-bottom: 20px;
  }

  h1 {
    font-size: 1.2rem;
  }
}
</style>
