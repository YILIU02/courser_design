<template>
  <div class="not-found">
    <div class="page-card not-found-card">
      <div class="not-found-code">404</div>
      <h1>页面不存在</h1>
      <p>请求的页面未找到，可能已迁移或当前账号无权访问。</p>
      <el-button type="primary" @click="router.push('/app/dashboard')">返回工作台</el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
}

.not-found-card {
  width: min(540px, 100%);
  padding: 48px 32px;
  text-align: center;
}

.not-found-code {
  font-size: 84px;
  font-weight: 800;
  color: var(--brand);
}

h1 {
  margin: 0 0 12px;
}

p {
  margin: 0 0 24px;
  color: var(--text-subtle);
}
</style>
