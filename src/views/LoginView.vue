<template>
  <div class="login-page">
    <div class="login-orb login-orb-left" />
    <div class="login-orb login-orb-right" />

    <section class="login-shell">
      <div class="login-copy">
        <div class="login-chip">企业管理平台</div>
        <h1>员工协同管理系统</h1>
        <p>统一处理员工、项目、考勤、绩效与请假审批。</p>
      </div>

      <section class="login-panel page-card">
        <div class="login-panel-top">
          <div class="login-panel-mark">CD</div>
          <div>
            <h2 class="page-title">登录系统</h2>
            <p class="page-subtitle">使用企业账号进入工作台</p>
          </div>
        </div>

        <el-form :model="form" label-position="top" autocomplete="off" @submit.prevent="handleSubmit">
          <el-form-item label="用户名">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              autocomplete="off"
              size="large"
            />
          </el-form-item>
          <el-form-item label="密码">
            <el-input
              v-model="form.password"
              type="password"
              show-password
              placeholder="请输入密码"
              autocomplete="new-password"
              size="large"
            />
          </el-form-item>
          <el-button :loading="loading" type="primary" size="large" class="login-button" @click="handleSubmit">
            进入系统
          </el-button>
        </el-form>
      </section>
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
  username: '',
  password: '',
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
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background:
    radial-gradient(circle at top, rgba(33, 95, 166, 0.08), transparent 30%),
    linear-gradient(180deg, #f3f6fb 0%, #eaf0f7 100%);
}

.login-orb {
  position: absolute;
  border-radius: 999px;
  filter: blur(80px);
  opacity: 0.55;
}

.login-orb-left {
  top: 8%;
  left: -6%;
  width: 280px;
  height: 280px;
  background: rgba(34, 97, 168, 0.18);
}

.login-orb-right {
  right: -4%;
  bottom: 8%;
  width: 240px;
  height: 240px;
  background: rgba(217, 137, 61, 0.16);
}

.login-shell {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  max-width: 1120px;
  margin: 0 auto;
  padding: 40px 24px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 430px;
  gap: 40px;
  align-items: center;
}

.login-copy {
  padding: 12px 8px;
}

.login-chip {
  display: inline-flex;
  align-items: center;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(15, 62, 115, 0.08);
  color: var(--brand-strong);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.login-copy h1 {
  margin: 18px 0 14px;
  font-size: 54px;
  line-height: 1.06;
  color: var(--text-main);
}

.login-copy p {
  margin: 0;
  max-width: 420px;
  color: var(--text-subtle);
  font-size: 17px;
  line-height: 1.8;
}

.login-panel {
  padding: 10px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(16px);
  box-shadow:
    0 24px 60px rgba(15, 35, 70, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
}

.login-panel-top {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 12px;
}

.login-panel-mark {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  background: linear-gradient(135deg, #11447c 0%, #3f8fe2 100%);
  color: white;
  font-size: 18px;
  font-weight: 800;
  letter-spacing: 0.08em;
  box-shadow: 0 12px 24px rgba(33, 95, 166, 0.22);
}

.login-button {
  width: 100%;
  margin-top: 10px;
  height: 48px;
  border-radius: 14px;
  font-weight: 700;
}

:deep(.el-input__wrapper) {
  min-height: 48px;
  border-radius: 14px;
  box-shadow: 0 0 0 1px rgba(15, 35, 70, 0.08) inset;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: var(--text-main);
}

@media (max-width: 980px) {
  .login-shell {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 24px 18px;
  }

  .login-copy {
    padding: 0;
  }

  .login-copy h1 {
    font-size: 38px;
  }

  .login-copy p {
    max-width: none;
  }
}
</style>
