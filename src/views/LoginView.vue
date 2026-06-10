<template>
  <div class="login-page">
    <section class="hero">
      <div class="hero-content">
        <div class="eyebrow">正式系统改造版</div>
        <h1>企业人事与协同运营平台</h1>
        <p>
          前端采用统一企业后台风格，后端基于 Flask 服务分层与 MySQL 数据模型，
          覆盖员工、项目、考勤、绩效与请假审批场景。
        </p>
        <div class="hero-grid">
          <div class="hero-card">
            <div class="hero-card-title">数据一致性</div>
            <div class="hero-card-text">统一接口响应、统一权限校验、统一聚合统计口径。</div>
          </div>
          <div class="hero-card">
            <div class="hero-card-title">角色权限</div>
            <div class="hero-card-text">管理员、部门负责人、员工三类角色按范围隔离数据。</div>
          </div>
        </div>
      </div>
    </section>

    <section class="login-panel page-card">
      <div class="page-header">
        <div>
          <h2 class="page-title">系统登录</h2>
          <p class="page-subtitle">使用企业账号进入工作台</p>
        </div>
      </div>

      <el-form :model="form" label-position="top" @submit.prevent="handleSubmit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" size="large" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="请输入密码" size="large" />
        </el-form-item>
        <el-button :loading="loading" type="primary" size="large" class="login-button" @click="handleSubmit">
          进入系统
        </el-button>
      </el-form>

      <div class="demo-box">
        <div class="demo-title">演示账号</div>
        <div class="demo-row"><span>管理员</span><code>admin / Admin@123</code></div>
        <div class="demo-row"><span>研发负责人</span><code>rd_manager / Manager@123</code></div>
        <div class="demo-row"><span>普通员工</span><code>rd_user / Staff@123</code></div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const form = reactive({
  username: 'admin',
  password: 'Admin@123',
})

async function handleSubmit() {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码。')
    return
  }

  loading.value = true
  try {
    await authStore.login(form)
    ElMessage.success('登录成功。')
    router.push('/app/dashboard')
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  background:
    linear-gradient(135deg, rgba(15, 62, 115, 0.96), rgba(22, 77, 142, 0.84)),
    url('/cowhourse.svg') center/cover;
  color: white;
}

.hero {
  position: relative;
  padding: 72px;
  display: grid;
  align-items: center;
}

.hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 12% 18%, rgba(217, 137, 61, 0.26), transparent 18%),
    radial-gradient(circle at 74% 80%, rgba(255, 255, 255, 0.12), transparent 22%);
}

.hero-content {
  position: relative;
  max-width: 660px;
}

.eyebrow {
  display: inline-flex;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  font-size: 13px;
  letter-spacing: 0.1em;
}

h1 {
  margin: 20px 0 16px;
  font-size: 56px;
  line-height: 1.08;
}

p {
  margin: 0;
  max-width: 560px;
  color: rgba(241, 247, 255, 0.86);
  font-size: 17px;
  line-height: 1.8;
}

.hero-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-top: 34px;
}

.hero-card {
  padding: 18px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
}

.hero-card-title {
  font-weight: 700;
  margin-bottom: 8px;
}

.hero-card-text {
  color: rgba(241, 247, 255, 0.82);
  line-height: 1.6;
  font-size: 14px;
}

.login-panel {
  margin: 32px;
  align-self: center;
  color: var(--text-main);
}

.login-button {
  width: 100%;
  margin-top: 8px;
}

.demo-box {
  margin-top: 28px;
  padding: 18px;
  border-radius: 18px;
  background: #f5f8fc;
}

.demo-title {
  font-weight: 700;
  margin-bottom: 12px;
}

.demo-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px dashed rgba(15, 35, 70, 0.08);
  font-size: 14px;
}

.demo-row:last-child {
  border-bottom: none;
}

code {
  color: var(--brand-strong);
}

@media (max-width: 1100px) {
  .login-page {
    grid-template-columns: 1fr;
  }

  .hero {
    padding: 40px 24px 16px;
  }

  .login-panel {
    margin: 0 24px 24px;
  }

  h1 {
    font-size: 40px;
  }

  .hero-grid {
    grid-template-columns: 1fr;
  }
}
</style>
