<template>
  <div class="preview-page">
    <div class="header">
      <div class="header-left">
        <router-link to="/xiaohongshu" class="back-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M20 11H7.83L13.42 5.41L12 4L4 12L12 20L13.41 18.59L7.83 13H20V11Z" fill="currentColor"/>
          </svg>
          返回编辑
        </router-link>
        <h1>跑者专属</h1>
      </div>
      <div class="header-right" v-if="titleData">
        <el-button-group>
          <el-button
            type="primary"
            :icon="copySuccess ? 'Check' : 'DocumentCopy'"
            @click="copyContent"
            :class="{ 'success': copySuccess }"
          >
            {{ copySuccess ? '已复制' : '复制' }}
          </el-button>
          <el-button
            type="primary"
            icon="Download"
            @click="downloadTitle"
          >
            下载
          </el-button>
        </el-button-group>
      </div>
    </div>

    <xiaohongshu-preview
      v-if="titleData"
      :title-data="titleData"
      ref="previewRef"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import XiaohongshuPreview from '../components/XiaohongshuPreview.vue'

const router = useRouter()
const route = useRoute()
const titleData = ref(null)
const previewRef = ref(null)
const copySuccess = ref(false)

const copyContent = async () => {
  if (previewRef.value) {
    await previewRef.value.copyContent()
  }
}

const downloadTitle = () => {
  if (previewRef.value) {
    previewRef.value.downloadTitle()
  }
}

onMounted(() => {
  // 从 URL query 参数中获取数据
  const queryData = route.query.data
  if (queryData) {
    try {
      titleData.value = JSON.parse(queryData)
    } catch (error) {
      console.error('解析数据失败:', error)
      router.replace('/xiaohongshu')
    }
  } else {
    // 如果没有数据，返回表单页面
    router.replace('/xiaohongshu')
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
  justify-content: space-between;
  gap: 20px;
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--background-color);
  padding: 20px;
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-right :deep(.el-button) {
  transition: all 0.3s ease;
}

.header-right :deep(.el-button.success) {
  background-color: #34c759;
  border-color: #34c759;
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
    flex-direction: column;
    align-items: flex-start;
  }

  .header-right {
    width: 100%;
    justify-content: flex-end;
  }

  h1 {
    font-size: 1.2rem;
  }
}
</style>
