<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import ArticlePreview from './ArticlePreview.vue'
import { useRouter } from 'vue-router'

// 表单数据
const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const loadingText = ref('正在生成文章')
const showPreview = ref(false)
const articleData = ref(null)
const errorMessage = ref('')

const formData = reactive({
  description: '',
  coreTopic: ''
})

const buttonText = computed(() => loading.value ? loadingText.value : '点击自动生成文章')

// 表单验证规则
const rules = reactive({
  description: [
    { required: true, message: '请输入内容描述', trigger: 'blur' },
    { min: 10, message: '描述内容至少10个字符', trigger: 'blur' },
    { max: 1000, message: '描述内容不能超过1000个字符', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value.trim().length < 10) {
          callback(new Error('描述内容不能全是空格'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  coreTopic: [
    { max: 100, message: '核心主题不能超过100个字符', trigger: 'blur' }
  ]
})

// 字数统计
const getWordCount = (text) => {
  return text.length
}

// 生成文章
const generateArticle = async () => {
  if (!formRef.value) return

  try {
    // 表单验证
    await formRef.value.validate()

    loading.value = true
    errorMessage.value = ''

    // 添加环境变量调试日志
    console.log('Environment variables:', {
      VITE_API_URL: import.meta.env.VITE_API_URL,
      MODE: import.meta.env.MODE,
      DEV: import.meta.env.DEV,
      PROD: import.meta.env.PROD,
    });

    console.log('Sending request to:', `${import.meta.env.VITE_API_URL}/article/generate`);
    console.log('Request data:', {
      description: formData.description,
      core_idea: formData.coreTopic,
    });

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 300000); // 5分钟超时
    let loadingInterval;

    try {
      // 更新加载状态文字
      loadingInterval = setInterval(() => {
        loadingText.value = loadingText.value + '.';
        if (loadingText.value.endsWith('....')) {
          loadingText.value = '正在生成文章';
        }
      }, 500);

      const response = await Promise.race([
        fetch(`${import.meta.env.VITE_API_URL}/article/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            description: formData.description,
            core_idea: formData.coreTopic,
          }),
          signal: controller.signal,
        }),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('请求超时，请重试')), 300000)
        )
      ]);

      if (!response) {
        throw new Error('未收到服务器响应');
      }

      console.log('Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text().catch(() => '未知错误');
        console.error('Error response:', errorText);
        throw new Error(`请求失败: ${response.status} ${errorText}`);
      }

      const data = await response.json();
      console.log('收到响应数据:', data);

      if (!data || !data.success) {
        throw new Error(data?.message || '生成失败，请重试');
      }

      // 保存文章数据并显示预览
      articleData.value = data;
      showPreview.value = true;

      // 导航到预览页面
      router.push({
        name: 'article-preview',
        params: { id: new Date().getTime() },
        query: { data: JSON.stringify(data) }
      });

    } catch (error) {
      console.error('Error:', error);
      throw error;
    } finally {
      clearTimeout(timeoutId);
      if (loadingInterval) {
        clearInterval(loadingInterval);
      }
    }
  } catch (error) {
    console.error('Error:', error);
    errorMessage.value = error.message || '生成失败，请重试';
    ElMessage.error({
      message: errorMessage.value,
      duration: 5000,
      showClose: true
    });
  } finally {
    loading.value = false;
    loadingText.value = '正在生成文章';
  }
}

const backToForm = () => {
  showPreview.value = false
  articleData.value = null
  errorMessage.value = ''
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
    errorMessage.value = ''
  }
}
</script>

<template>
  <div class="page-container">
    <!-- 文章生成表单 -->
    <div v-if="!showPreview" class="article-form">
      <div class="header">
        <router-link to="/" class="back-button">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M20 11H7.83L13.42 5.41L12 4L4 12L12 20L13.41 18.59L7.83 13H20V11Z" fill="currentColor"/>
          </svg>
          返回首页
        </router-link>
        <h1>灵感写手</h1>
      </div>
      <div class="form-container">
        <el-form
          ref="formRef"
          :model="formData"
          :rules="rules"
          label-position="top"
          @submit.prevent
        >
          <div class="input-group">
            <el-form-item
              label="内容描述"
              prop="description"
              :error="errorMessage"
            >
              <el-input
                v-model="formData.description"
                type="textarea"
                :rows="6"
                placeholder="请输入文章内容描述..."
                resize="none"
                maxlength="1000"
                show-word-limit
              />
              <div class="input-tips">
                <el-alert
                  v-if="formData.description.length < 10"
                  title="建议：描述越详细，生成的文章质量越高"
                  type="info"
                  :closable="false"
                  show-icon
                />
              </div>
            </el-form-item>
          </div>

          <div class="input-group">
            <el-form-item
              label="核心主题"
              prop="coreTopic"
            >
              <el-input
                v-model="formData.coreTopic"
                placeholder="请输入核心主题（选填）..."
                maxlength="100"
                show-word-limit
              />
              <div class="input-tips">
                <el-alert
                  title="提示：核心主题可以帮助AI更好地把握文章重点"
                  type="info"
                  :closable="false"
                  show-icon
                />
              </div>
            </el-form-item>
          </div>

          <div class="form-actions">
            <el-button
              type="primary"
              :loading="loading"
              @click="generateArticle"
              class="submit-button"
            >
              {{ buttonText }}
            </el-button>

            <el-button
              type="default"
              @click="resetForm"
              :disabled="loading"
              class="reset-button"
            >
              重置表单
            </el-button>
          </div>
        </el-form>
      </div>
    </div>

    <!-- 文章预览 -->
    <template v-else>
      <div class="preview-header">
        <el-button
          type="default"
          @click="backToForm"
          class="back-button"
        >
          返回编辑
        </el-button>
      </div>
      <article-preview
        :article-data="articleData"
      />
    </template>
  </div>
</template>

<style scoped>
.page-container {
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

.article-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px 40px;
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

.input-group :deep(.el-form-item__label) {
  font-size: 1rem;
  font-weight: 500;
  color: #1d1d1f;
  margin-bottom: 8px;
  line-height: 1.5;
}

.input-tips {
  margin-top: 8px;
}

.input-tips :deep(.el-alert) {
  background: transparent;
  padding: 0;
}

.input-tips :deep(.el-alert__title) {
  font-size: 0.9rem;
  color: #6e6e73;
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

:deep(.el-input__count) {
  background: transparent;
  font-size: 0.9rem;
  color: #6e6e73;
}

.form-actions {
  display: flex;
  gap: 16px;
  margin-top: 32px;
}

.submit-button {
  flex: 2;
  height: 50px;
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

.reset-button {
  flex: 1;
  height: 50px;
  font-size: 1.1rem;
  font-weight: 500;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.reset-button:hover {
  background: #f5f5f7;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .article-form {
    padding: 20px 10px;
  }

  .form-container {
    padding: 20px;
  }

  h1 {
    font-size: 2rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .submit-button,
  .reset-button {
    width: 100%;
  }
}
</style>
