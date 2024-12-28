<template>
  <div class="xiaohongshu-container">
    <div class="header">
      <router-link to="/" class="back-button">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M20 11H7.83L13.42 5.41L12 4L4 12L12 20L13.41 18.59L7.83 13H20V11Z" fill="currentColor"/>
        </svg>
        返回首页
      </router-link>
      <h1>小红书标题生成（跑者专享）</h1>
    </div>

    <div class="form-container">
      <div class="form-group">
        <label><span class="required">*</span>内容描述</label>
        <textarea
          v-model="formData.description"
          placeholder="描述你想要生成的文案主题，例如：分享一次跑步体验"
          rows="4"
          @input="validateDescription"
          :disabled="isGenerating"
        ></textarea>
        <div class="info-container">
          <div class="input-tips">
            *描述越清晰，生成内容才更合适哦
          </div>
          <div class="input-info" :class="{ 'error': !isDescriptionValid && formData.description.length > 0 }">
            {{ formData.description.length }}/500字
            <span v-if="!isDescriptionValid && formData.description.length > 0">
              (需要在3-500字之间)
            </span>
          </div>
        </div>
      </div>

      <div class="button-group">
        <button
          class="submit-button"
          @click="generateContent"
          :disabled="isGenerating || !isDescriptionValid || formData.description.length === 0"
        >
          <span v-if="isGenerating" class="loading-spinner"></span>
          {{ isGenerating ? '生成中...' : '开始生成' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const formData = reactive({
  description: '',
})

const isGenerating = ref(false)
const isDescriptionValid = ref(false)
const loadingText = ref('正在生成')

const validateDescription = () => {
  const length = formData.description.length
  isDescriptionValid.value = length >= 3 && length <= 500
}

const generateContent = async () => {
  if (!isDescriptionValid.value) return

  isGenerating.value = true
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), 300000) // 5分钟超时
  let loadingInterval

  try {
    // 更新加载状态文字
    loadingInterval = setInterval(() => {
      loadingText.value = loadingText.value + '.'
      if (loadingText.value.endsWith('....')) {
        loadingText.value = '正在生成'
      }
    }, 500)

    const response = await Promise.race([
      fetch(`${import.meta.env.VITE_API_URL}/article/generatetitle`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description: formData.description,
          platform: 'xiaohongshu'
        }),
        signal: controller.signal,
      }),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('请求超时，请重试')), 300000)
      )
    ])

    if (!response) {
      throw new Error('未收到服务器响应')
    }

    if (!response.ok) {
      const errorText = await response.text().catch(() => '未知错误')
      throw new Error(`请求失败: ${response.status} ${errorText}`)
    }

    const data = await response.json()
    if (!data || !data.data || !data.data.content) {
      throw new Error('生成内容为空')
    }

    // 导航到预览页面
    router.push({
      name: 'xiaohongshu-preview',
      params: { id: new Date().getTime() },
      query: { data: JSON.stringify(data) }
    })

  } catch (error) {
    console.error('生成失败:', error)
    ElMessage.error(error.message || '生成失败，请重试')
  } finally {
    clearTimeout(timeoutId)
    if (loadingInterval) {
      clearInterval(loadingInterval)
    }
    isGenerating.value = false
    loadingText.value = '正在生成'
  }
}
</script>

<style scoped>
.xiaohongshu-container {
  max-width: 800px;
  margin: 0 auto;
  min-height: 100vh;
  background: var(--background-color);
}

.header {
  max-width: 800px;
  margin: 0 auto 40px;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
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

.header h1 {
  margin: 0;
  font-size: 2rem;
  background: linear-gradient(135deg, #1d1d1f 0%, #434343 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.form-container {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
  margin: 0 20px 30px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s ease;
}

textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(0, 113, 227, 0.2);
}

textarea:disabled {
  background-color: #f5f5f7;
  cursor: not-allowed;
}

.button-group {
  display: flex;
  gap: 12px;
}

.submit-button, .regenerate-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button {
  flex: 2;
  background: var(--primary-color);
  color: white;
}

.regenerate-button {
  flex: 1;
  background: var(--background-color);
  border: 1px solid var(--border-color);
  color: var(--text-color);
}

.submit-button:disabled,
.regenerate-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background: #ccc;
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #ffffff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.info-container {
  margin-top: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-tips {
  font-size: 14px;
  color: #6e6e73;
  font-style: italic;
}

.input-info {
  font-size: 14px;
  color: #666;
}

.input-info.error {
  color: #ff4d4f;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .xiaohongshu-container {
    padding: 10px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .submit-button,
  .regenerate-button {
    width: 100%;
  }
}

.required {
  color: #ff4d4f;
  margin-right: 4px;
}
</style>
