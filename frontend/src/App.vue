<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 根据路由更新标题
watch(() => route.path, (to) => {
  // 可以根据不同的路由设置不同的标题后缀
  const baseTitle = import.meta.env.VITE_APP_TITLE
  switch(to) {
    case '/article':
      document.title = `文章生成 | ${baseTitle}`
      break
    case '/xiaohongshu':
      document.title = `小红书标题生成 | ${baseTitle}`
      break
    default:
      document.title = baseTitle
  }
})
</script>

<template>
  <div class="app">
    <router-view></router-view>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700&display=swap');

:root {
  --primary-color: #0071e3;
  --text-color: #1d1d1f;
  --background-color: #f5f5f7;
  --border-color: #d2d2d7;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background: var(--background-color);
  color: var(--text-color);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  min-height: 100vh;
  padding: 20px;
}

@media (max-width: 768px) {
  .app {
    padding: 10px;
  }
}
</style>
