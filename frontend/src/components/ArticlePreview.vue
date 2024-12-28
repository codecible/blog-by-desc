<script setup>
import { ref, onMounted, defineProps, watch } from 'vue'
import { marked } from 'marked'
import 'highlight.js/styles/github.css'
import hljs from 'highlight.js'
import { ElMessage } from 'element-plus'

// 定义props接收文章数据
const props = defineProps({
  articleData: {
    type: Object,
    required: true
  }
})

// 初始化所有ref变量
const content = ref('')
const htmlContent = ref('')
const loading = ref(true)
const copySuccess = ref(false)

// 复制文章内容到剪贴板
const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(content.value)
    ElMessage({
      message: '文章内容已复制到剪贴板',
      type: 'success',
      duration: 2000
    })
    copySuccess.value = true
    setTimeout(() => {
      copySuccess.value = false
    }, 2000)
  } catch (err) {
    ElMessage.error('复制失败，请手动复制')
  }
}

// 下载文章为Markdown文件
const downloadMarkdown = () => {
  const element = document.createElement('a')
  const file = new Blob([content.value], {type: 'text/markdown'})
  element.href = URL.createObjectURL(file)
  element.download = `article_${new Date().toISOString().slice(0,10).replace(/-/g,'')}_${new Date().toTimeString().slice(0,5).replace(/:/g,'')}${Math.floor(Math.random() * 100)}.md`
  document.body.appendChild(element)
  element.click()
  document.body.removeChild(element)
}

// 处理文章数据
const processArticleData = () => {
  if (props.articleData && props.articleData.data) {
    const { data } = props.articleData
    content.value = data.content || ''

    // 配置marked选项
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

    // 转换Markdown为HTML
    htmlContent.value = marked(content.value)
  }
}

// 监听文章数据变化
watch(() => props.articleData, (newVal) => {
  if (newVal) {
    loading.value = true
    try {
      processArticleData()
    } catch (error) {
      ElMessage.error('处理文章内容失败')
    } finally {
      loading.value = false
    }
  }
}, { immediate: true, deep: true })
</script>

<template>
  <div class="article-preview">
    <div class="preview-container">
      <!-- 顶部工具栏 -->
      <div class="toolbar">
        <el-button-group>
          <el-button
            type="primary"
            :icon="copySuccess ? 'Check' : 'DocumentCopy'"
            @click="copyContent"
            :class="{ 'success': copySuccess }"
          >
            {{ copySuccess ? '已复制' : '复制全文' }}
          </el-button>
          <el-button
            type="primary"
            icon="Download"
            @click="downloadMarkdown"
          >
            下载文章
          </el-button>
        </el-button-group>
      </div>

      <!-- 加载状态 -->
      <el-skeleton :loading="loading" animated>
        <template #template>
          <div class="skeleton-content">
            <el-skeleton-item variant="text" style="margin-bottom: 10px;" v-for="i in 8" :key="i" />
          </div>
        </template>

        <template #default>
          <div class="article-content" v-if="content">
            <!-- 文章内容 -->
            <div class="content-section">
              <div class="markdown-content" v-html="htmlContent"></div>
            </div>
          </div>

          <el-empty v-else description="暂无文章内容" />
        </template>
      </el-skeleton>
    </div>
  </div>
</template>

<style scoped>
.article-preview {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 100vh;
}

.preview-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.1);
  min-height: calc(100vh - 80px);
}

.skeleton-content {
  padding: 20px;
}

.toolbar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  justify-content: flex-end;
  margin-bottom: 30px;
  padding: 10px 0;
  background: inherit;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.toolbar :deep(.el-button) {
  font-weight: 500;
  transition: all 0.3s ease;
}

.toolbar :deep(.el-button.success) {
  background-color: #34c759;
  border-color: #34c759;
}

.article-content {
  animation: fadeIn 0.5s ease-out;
}

.content-section {
  margin-top: 20px;
  animation: slideUp 0.6s ease-out;
}

.markdown-content {
  color: #1d1d1f;
  line-height: 1.6;
  font-size: 1.1rem;
  animation: fadeIn 0.7s ease-out;
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

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .article-preview {
    padding: 20px 10px;
  }

  .preview-container {
    padding: 20px;
  }
}
</style>
