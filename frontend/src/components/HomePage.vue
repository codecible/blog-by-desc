<template>
  <div class="home-container">
    <h1 class="title">创意伙伴</h1>
    <div class="cards-container">
      <!-- 文章生成器卡片 -->
      <router-link to="/article" class="card">
        <div class="card-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 19H5C3.89543 19 3 18.1046 3 17V7C3 5.89543 3.89543 5 5 5H19C20.1046 5 21 5.89543 21 7V17C21 18.1046 20.1046 19 19 19H12ZM5 7V17H19V7H5Z" fill="currentColor"/>
            <path d="M6 9H18V11H6V9ZM6 13H14V15H6V13Z" fill="currentColor"/>
          </svg>
        </div>
        <h2>灵感写作家</h2>
        <p>让公众号文章创作更高效！</p>
        <p>生成专业的长文章内容，支持多种写作风格和主题方向。</p>
      </router-link>

      <!-- 小红书文案卡片 -->
      <router-link to="/xiaohongshu" class="card">
        <div class="card-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 6H3V18H21V6ZM19 16H5V8H19V16Z" fill="currentColor"/>
            <path d="M7 10H17V12H7V10ZM7 13H13V14H7V13Z" fill="currentColor"/>
          </svg>
        </div>
        <h2>跑文标题助手</h2>
        <p>还在为小红书跑步文案发愁？跑文助手是一款专为跑者打造的文案生成工具，只需输入跑步数据或关键词，即可轻松生成吸睛又走心的小红书文案！</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
// HomePage.vue
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  text-align: center;
}

.title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 40px;
  background: linear-gradient(135deg, #1a1a1a 0%, #4a4a4a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
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

@media (max-width: 768px) {
  .home-container {
    padding: 20px 10px;
  }

  .title {
    font-size: 36px;
    margin-bottom: 30px;
  }

  .cards-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
