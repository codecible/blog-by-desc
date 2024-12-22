<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const description = ref('')
const coreTopic = ref('')
const loading = ref(false)

const generateArticle = async () => {
  if (!description.value.trim()) {
    ElMessage.warning('请输入内容描述')
    return
  }

  loading.value = true
  try {
    console.log('发送请求数据:', {
      description: description.value,
      core_idea: coreTopic.value,
    })

    const response = await fetch('/blog/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        description: description.value,
        core_idea: coreTopic.value,
      }),
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('请求失败:', {
        status: response.status,
        statusText: response.statusText,
        errorText
      })
      throw new Error(`请求失败: ${response.status} ${response.statusText}\n${errorText}`)
    }

    const data = await response.json()
    console.log('收到响应数据:', data)
    
    router.push({
      name: 'preview',
      params: { 
        title: data.title,
        directions: JSON.stringify(data.directions),
        content: data.content
      }
    })
  } catch (error) {
    console.error('发生错误:', error)
    ElMessage.error(error.message || '生成失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="article-form">
    <h1>AI文章生成器</h1>
    <div class="form-container">
      <div class="input-group">
        <label>内容描述</label>
        <el-input
          v-model="description"
          type="textarea"
          :rows="6"
          placeholder="请输入文章内容描述..."
          resize="none"
        />
      </div>
      
      <div class="input-group">
        <label>核心主题</label>
        <el-input
          v-model="coreTopic"
          placeholder="请输入核心主题（选填）..."
        />
      </div>

      <el-button
        type="primary"
        :loading="loading"
        @click="generateArticle"
        class="submit-button"
      >
        点击自动生成文章
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.article-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1d1d1f;
  text-align: center;
  margin-bottom: 40px;
}

.form-container {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.input-group {
  margin-bottom: 24px;
}

.input-group label {
  display: block;
  font-size: 1rem;
  font-weight: 500;
  color: #1d1d1f;
  margin-bottom: 8px;
}

:deep(.el-input__wrapper) {
  border-radius: 12px;
  box-shadow: none;
  border: 1px solid #d2d2d7;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  border-color: #86b7fe;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #0071e3;
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
}

:deep(.el-textarea__inner) {
  border-radius: 12px;
  padding: 12px;
  font-size: 1rem;
  line-height: 1.5;
}

.submit-button {
  width: 100%;
  height: 50px;
  margin-top: 20px;
  font-size: 1.1rem;
  font-weight: 500;
  border-radius: 12px;
  background: #0071e3;
  border: none;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background: #0077ed;
  transform: translateY(-1px);
}

.submit-button:active {
  transform: translateY(0);
}
</style> 