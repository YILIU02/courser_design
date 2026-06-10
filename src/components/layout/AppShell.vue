<template>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">CD</div>
        <div>
          <div class="brand-title">Course Design</div>
          <div class="brand-subtitle">Enterprise Console</div>
        </div>
      </div>

      <div class="profile">
        <div class="profile-avatar">{{ initials }}</div>
        <div>
          <div class="profile-name">{{ authStore.user?.full_name }}</div>
          <div class="profile-role">
            {{ authStore.user?.department_name }} / {{ authStore.user?.role_name }}
          </div>
        </div>
      </div>

      <el-menu
        class="menu"
        :default-active="route.path"
        background-color="transparent"
        text-color="#dce8f7"
        active-text-color="#ffffff"
      >
        <el-menu-item
          v-for="item in authStore.visibleNavigation"
          :key="item.path"
          :index="item.path"
          @click="router.push(item.path)"
        >
          <component :is="item.icon" class="menu-icon" />
          <span>{{ item.label }}</span>
        </el-menu-item>
      </el-menu>
    </aside>

    <main class="main">
      <header class="header page-card">
        <div>
          <div class="header-title">{{ currentTitle }}</div>
          <div class="header-subtitle">统一员工、项目、考勤、绩效与审批流程</div>
        </div>
        <div class="header-actions">
          <el-tag type="info" effect="plain">{{ authStore.user?.employee_no }}</el-tag>
          <el-button type="primary" plain @click="logout">退出登录</el-button>
        </div>
      </header>

      <section class="content">
        <router-view />
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const currentTitle = computed(() => route.meta.title || '工作台')
const initials = computed(() => authStore.user?.full_name?.slice(0, 1) || 'U')

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 280px 1fr;
  background:
    radial-gradient(circle at top left, rgba(33, 95, 166, 0.18), transparent 26%),
    radial-gradient(circle at right center, rgba(217, 137, 61, 0.14), transparent 24%),
    var(--page-bg);
}

.sidebar {
  padding: 24px 20px;
  background: var(--sidebar-bg);
  color: white;
  display: flex;
  flex-direction: column;
  gap: 24px;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-mark {
  width: 54px;
  height: 54px;
  display: grid;
  place-items: center;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.24), rgba(255, 255, 255, 0.06));
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 1px;
}

.brand-title {
  font-size: 18px;
  font-weight: 700;
}

.brand-subtitle {
  margin-top: 4px;
  color: rgba(220, 232, 247, 0.82);
  font-size: 12px;
}

.profile {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.08);
}

.profile-avatar {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  background: linear-gradient(135deg, #d9893d, #f0b26a);
  font-size: 20px;
  font-weight: 700;
}

.profile-name {
  font-size: 16px;
  font-weight: 700;
}

.profile-role {
  margin-top: 4px;
  font-size: 12px;
  color: rgba(220, 232, 247, 0.82);
}

.menu {
  border-right: none;
}

.menu :deep(.el-menu-item) {
  height: 48px;
  border-radius: 14px;
  margin-bottom: 8px;
}

.menu :deep(.el-menu-item.is-active) {
  background: rgba(255, 255, 255, 0.14);
}

.menu-icon {
  width: 18px;
  margin-right: 10px;
}

.main {
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 22px;
  margin-bottom: 18px;
}

.header-title {
  font-size: 24px;
  font-weight: 700;
}

.header-subtitle {
  margin-top: 6px;
  color: var(--text-subtle);
  font-size: 13px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.content {
  min-height: calc(100vh - 126px);
}

@media (max-width: 1080px) {
  .shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    padding-bottom: 8px;
  }

  .main {
    padding-top: 0;
  }
}
</style>
