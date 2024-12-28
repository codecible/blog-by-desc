<template>
  <div class="xiaohongshu-container">
    <div class="header">
      <router-link to="/" class="back-button">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M20 11H7.83L13.42 5.41L12 4L4 12L12 20L13.41 18.59L7.83 13H20V11Z" fill="currentColor"/>
        </svg>
        返回
      </router-link>
      <h1>小红书文案生成器</h1>
    </div>

    <div class="form-container">
      <div class="form-group">
        <label>主题描述</label>
        <textarea
          v-model="formData.description"
          placeholder="描述你想要生成的文案主题，例如：分享一款新买的化妆品使用体验"
          rows="4"
        ></textarea>
      </div>

      <div class="form-group">
        <label>文案风格</label>
        <select v-model="formData.style">
          <option value="casual">轻松日常风</option>
          <option value="professional">专业测评风</option>
          <option value="emotional">感性治愈风</option>
          <option value="humor">幽默搞笑风</option>
        </select>
      </div>

      <div class="form-group">
        <label>关键词</label>
        <input
          type="text"
          v-model="formData.keywords"
          placeholder="输入关键词，用逗号分隔，例如：好用,性价比高,安全"
        />
      </div>

      <div class="form-group">
        <label>标签数量</label>
        <input
          type="number"
          v-model="formData.tagCount"
          min="3"
          max="20"
          placeholder="建议3-20个标签"
        />
      </div>

      <button class="submit-button" @click="generateContent" :disabled="isGenerating">
        {{ isGenerating ? '生成中...' : '开始生成' }}
      </button>
    </div>

    <div v-if="generatedContent" class="preview-container">
      <div class="preview-header">
        <h2>生成结果</h2>
        <div class="preview-actions">
          <button @click="copyContent" class="action-button">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M16 1H4C2.9 1 2 1.9 2 3V17H4V3H16V1ZM19 5H8C6.9 5 6 5.9 6 7V21C6 22.1 6.9 23 8 23H19C20.1 23 21 22.1 21 21V7C21 5.9 20.1 5 19 5ZM19 21H8V7H19V21Z" fill="currentColor"/>
            </svg>
            复制文案
          </button>
          <button @click="regenerateContent" class="action-button">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4C7.58 4 4.01 7.58 4.01 12C4.01 16.42 7.58 20 12 20C15.73 20 18.84 17.45 19.73 14H17.65C16.83 16.33 14.61 18 12 18C8.69 18 6 15.31 6 12C6 8.69 8.69 6 12 6C13.66 6 15.14 6.69 16.22 7.78L13 11H20V4L17.65 6.35Z" fill="currentColor"/>
            </svg>
            重新生成
          </button>
        </div>
      </div>

      <div class="content-preview">
        <div class="title">{{ generatedContent.title }}</div>
        <div class="content">{{ generatedContent.content }}</div>
        <div class="tags">
          <span v-for="(tag, index) in generatedContent.tags" :key="index" class="tag">
            #{{ tag }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const formData = reactive({
  description: '',
  style: 'casual',
  keywords: '',
  tagCount: 5
})

const isGenerating = ref(false)
const generatedContent = ref(null)

const generateContent = async () => {
  isGenerating.value = true
  try {
    // TODO: 调用后端API生成内容
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))
    generatedContent.value = {
      title: '测试标题',
      content: '测试内容',
      tags: ['测试标签1', '测试标签2', '测试标签3']
    }
  } catch (error) {
    console.error('生成失败:', error)
  } finally {
    isGenerating.value = false
  }
}

const regenerateContent = () => {
  generateContent()
}

const copyContent = () => {
  if (!generatedContent.value) return

  const text = `${generatedContent.value.title}\n\n${generatedContent.value.content}\n\n${generatedContent.value.tags.map(tag => '#' + tag).join(' ')}`
  navigator.clipboard.writeText(text)
}
</script>

<style scoped>
.xiaohongshu-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 40px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text-color);
  margin-right: 20px;
}

.form-container {
  background: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

input, textarea, select {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s ease;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(0, 113, 227, 0.2);
}

.submit-button {
  width: 100%;
  padding: 14px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.preview-container {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.preview-actions {
  display: flex;
  gap: 10px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button:hover {
  background: #e5e5e7;
}

.content-preview {
  padding: 20px;
  background: var(--background-color);
  border-radius: 10px;
}

.title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
}

.content {
  margin-bottom: 20px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 4px 12px;
  background: #e5e5e7;
  border-radius: 16px;
  font-size: 14px;
}

@media (max-width: 768px) {
  .xiaohongshu-container {
    padding: 10px;
  }

  .form-container,
  .preview-container {
    padding: 20px;
  }

  .preview-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .preview-actions {
    width: 100%;
  }

  .action-button {
    flex: 1;
    justify-content: center;
  }
}
</style>
