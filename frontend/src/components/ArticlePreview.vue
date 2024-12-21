<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import 'highlight.js/styles/github.css'
import hljs from 'highlight.js'

const route = useRoute()
const title = ref('')
const directions = ref([])
const content = ref('')
const htmlContent = ref('')

onMounted(() => {
  title.value = route.params.title || ''
  directions.value = JSON.parse(route.params.directions || '[]')
  content.value = route.params.content || ''
  
  // 配置marked选项
  marked.setOptions({
    highlight: function(code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value
      }
      return hljs.highlightAuto(code).value
    },
    breaks: true
  })
  
  // 转换Markdown为HTML
  htmlContent.value = marked(content.value)
})
</script>

<template>
  <div class="article-preview">
    <div class="preview-container">
      <h1 class="article-title">{{ title }}</h1>
      
      <div v-if="directions.length" class="directions-section">
        <h2>写作方向</h2>
        <ul class="directions-list">
          <li v-for="(direction, index) in directions" :key="index">
            {{ direction }}
          </li>
        </ul>
      </div>
      
      <div class="content-section">
        <h2>文章内容</h2>
        <div class="markdown-content" v-html="htmlContent"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.article-preview {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.preview-container {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.article-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1d1d1f;
  text-align: center;
  margin-bottom: 40px;
  line-height: 1.2;
}

h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1d1d1f;
  margin: 30px 0 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f5f5f7;
}

.directions-section {
  margin: 30px 0;
}

.directions-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.directions-list li {
  position: relative;
  padding: 12px 0 12px 24px;
  color: #1d1d1f;
  font-size: 1.1rem;
  line-height: 1.4;
}

.directions-list li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #0071e3;
  font-weight: bold;
}

.content-section {
  margin-top: 40px;
}

.markdown-content {
  color: #1d1d1f;
  line-height: 1.6;
  font-size: 1.1rem;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin: 1.5em 0 0.8em;
  font-weight: 600;
  line-height: 1.3;
}

.markdown-content :deep(p) {
  margin: 1em 0;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 1.5em;
  margin: 1em 0;
}

.markdown-content :deep(li) {
  margin: 0.5em 0;
}

.markdown-content :deep(code) {
  background: #f5f5f7;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
  font-family: 'SF Mono', Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
}

.markdown-content :deep(pre) {
  background: #f5f5f7;
  padding: 1em;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1em 0;
}

.markdown-content :deep(blockquote) {
  margin: 1em 0;
  padding-left: 1em;
  border-left: 4px solid #0071e3;
  color: #6e6e73;
}

.markdown-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1em 0;
}

.markdown-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  padding: 0.5em;
  border: 1px solid #d2d2d7;
}

.markdown-content :deep(th) {
  background: #f5f5f7;
}
</style> 