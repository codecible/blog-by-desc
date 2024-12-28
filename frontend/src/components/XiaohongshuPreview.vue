<template>
  <div class="preview-container">
    <div class="quote-block">
      <p class="quote-text">"跑步让平凡的日子也能亮起来。"</p>
      <p class="quote-author">—— 村上春树《当我谈跑步时我谈些什么》</p>
    </div>

    <el-skeleton :loading="loading" animated>
      <template #template>
        <div class="skeleton-content">
          <el-skeleton-item variant="text" style="margin-bottom: 10px;" v-for="i in 3" :key="i" />
        </div>
      </template>

      <template #default>
        <div class="content" v-if="content">
          <div class="markdown-content" v-html="htmlContent"></div>
        </div>
        <el-empty v-else description="暂无内容" />
      </template>
    </el-skeleton>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, watch } from 'vue'
import { marked } from 'marked'
import 'highlight.js/styles/github.css'
import hljs from 'highlight.js'
import { ElMessage } from 'element-plus'

const props = defineProps({
  titleData: {
    type: Object,
    required: true
  }
})

const content = ref('')
const htmlContent = ref('')
const loading = ref(true)
const copySuccess = ref(false)

const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(content.value)
    showCopySuccess()
  } catch (err) {
    try {
      const textarea = document.createElement('textarea')
      textarea.value = content.value
      textarea.style.position = 'fixed'
      textarea.style.opacity = '0'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      showCopySuccess()
    } catch (fallbackErr) {
      ElMessage.error('复制失败，请手动复制')
    }
  }
}

const showCopySuccess = () => {
  ElMessage({
    message: '已复制到剪贴板',
    type: 'success',
    duration: 2000,
  })
  copySuccess.value = true
  setTimeout(() => {
    copySuccess.value = false
  }, 2000)
}

const downloadTitle = () => {
  const element = document.createElement('a')
  const file = new Blob([content.value], {type: 'text/plain'})
  element.href = URL.createObjectURL(file)
  element.download = `xiaohongshu_title_${new Date().toISOString().slice(0,10)}.txt`
  document.body.appendChild(element)
  element.click()
  document.body.removeChild(element)
}

const processContent = () => {
  if (props.titleData && props.titleData.data) {
    content.value = props.titleData.data.content || ''

    marked.setOptions({
      highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          return hljs.highlight(code, { language: lang }).value
        }
        return hljs.highlightAuto(code).value
      },
      breaks: true,
      gfm: true
    })

    htmlContent.value = marked(content.value)
  }
}

watch(() => props.titleData, (newVal) => {
  if (newVal) {
    loading.value = true
    try {
      processContent()
    } catch (error) {
      ElMessage.error('处理内容失败')
    } finally {
      loading.value = false
    }
  }
}, { immediate: true, deep: true })
</script>

<style scoped>
.preview-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.toolbar {
  position: sticky;
  top: 0;
  z-index: 100;
  margin-bottom: 30px;
  padding: 20px;
  background: #f0f7ff;
  border-radius: 12px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  border: none;
}

.toolbar :deep(.el-button) {
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 100px;
  height: 40px;
}

.toolbar :deep(.el-button.success) {
  background-color: #34c759;
  border-color: #34c759;
}

.content {
  animation: fadeIn 0.5s ease-out;
}

.markdown-content {
  color: #1d1d1f;
  line-height: 1.6;
  font-size: 1.1rem;
  white-space: pre-wrap;
  animation: fadeIn 0.7s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .preview-container {
    padding: 20px;
    margin: 10px;
  }
}

.quote-block {
  background: #f0f7ff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid rgba(0, 113, 227, 0.1);
}

.quote-text {
  font-size: 1.2rem;
  color: #1d1d1f;
  margin: 0 0 10px 0;
  font-weight: 500;
  text-align: center;
}

.quote-author {
  font-size: 0.9rem;
  color: #6e6e73;
  margin: 0;
  font-style: italic;
  text-align: right;
}
</style>
