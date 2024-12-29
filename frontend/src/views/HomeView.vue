<template>
  <div class="home-container">
    <h1 class="title">KD Tools Hub</h1>
    <div class="cards-container">

    <!-- 小红书文案卡片 -->
      <router-link to="/xiaohongshu" class="card">
        <div class="card-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- 主标题框 -->
            <rect x="4" y="6" width="16" height="6" rx="1" fill="var(--background-color)" stroke="currentColor" stroke-width="1.5"/>
            <!-- 创意灯泡 -->
            <circle cx="7" cy="9" r="1.5" fill="currentColor"/>
            <!-- 标题文本线 -->
            <path d="M10 9H17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <!-- 副标题框 -->
            <path d="M6 15H14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M6 18H12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <!-- 创意星星 -->
            <path d="M17 14L18 15L17 16L16 15L17 14Z" fill="currentColor"/>
            <path d="M19 17L20 18L19 19L18 18L19 17Z" fill="currentColor"/>
            <path d="M16 18L17 19L16 20L15 19L16 18Z" fill="currentColor"/>
          </svg>
        </div>
        <h2>🏃‍♂️智能标题助手｜跑步博主专享⭐</h2>
        <p class="keynote">还在为写跑步标题发愁吗？</p>
        <p>只需输入想表达的内容，自动帮你生成10个不同风格的小红书标题！包含励志、干货、治愈等多种风格，智能匹配emoji，让跑步博主的创作之路不再有标题困扰～</p>
    </router-link>

      <!-- 文章生成器卡片 -->
      <router-link to="/article" class="card">
        <div class="card-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- 纸张背景 -->
            <path d="M19 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3Z" fill="var(--background-color)" stroke="currentColor" stroke-width="1.5"/>
            <!-- 纸张上的横线 -->
            <path d="M7 8H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M7 12H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M7 16H13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <!-- 钢笔 -->
            <path d="M16.5 15.5L19 13L20 14L17.5 16.5L16.5 15.5Z" fill="currentColor"/>
            <path d="M16.5 15.5L15.5 16.5L14 20L17.5 16.5L16.5 15.5Z" fill="currentColor"/>
          </svg>
        </div>
        <h2>📝一键写文章｜提升创作效率💫</h2>
        <p class="keynote">输入核心主题，自动帮你生成公众号文章！</p>
        <p>智能分析主题重点，自动构建文章框架。让创作者告别写作焦虑，轻松打造优质文章。支持多种写作风格，让你的公众号创作事半功倍～</p>
      </router-link>

    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  text-align: center;
}

.title {
  font-size: 56px;
  font-weight: 800;
  margin-bottom: 40px;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, var(--primary-color) 0%, #34c759 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  display: inline-block;
  padding: 0 20px;
}

.title::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 4px;
  background: var(--primary-color);
  border-radius: 2px;
}

.title::after {
  content: '';
  position: absolute;
  top: -10px;
  right: -10px;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, var(--primary-color) 0%, #34c759 100%);
  opacity: 0.2;
  border-radius: 50%;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  text-decoration: none;
  color: var(--text-color);
  transition: all 0.3s ease;
  border: 1px solid var(--border-color);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: var(--primary-color);
}

.card-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--background-color);
  border-radius: 20px;
  color: var(--primary-color);
}

.card h2 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 15px;
}

.card p {
  font-size: 16px;
  color: #86868b;
  line-height: 1.5;
}

.card .keynote {
  font-size: 18px;
  font-weight: 500;
  color: var(--primary-color);
  margin-bottom: 12px;
  position: relative;
  display: inline-block;
  padding: 0 4px;
}

.card .keynote::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 0;
  width: 100%;
  height: 6px;
  background: var(--primary-color);
  opacity: 0.1;
  border-radius: 3px;
  z-index: -1;
}

@media (max-width: 768px) {
  .home-container {
    padding: 20px 10px;
  }

  .title {
    font-size: 36px;
    margin-bottom: 30px;
  }

  .title::before {
    width: 40px;
    height: 3px;
  }

  .title::after {
    width: 15px;
    height: 15px;
    top: -8px;
    right: -8px;
  }

  .cards-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
