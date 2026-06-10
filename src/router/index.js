import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '../stores/auth'
import { pinia } from '../stores/pinia'

const routes = [
  {
    path: '/',
    redirect: '/app/dashboard',
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
    meta: { public: true },
  },
  {
    path: '/app',
    component: () => import('../components/layout/AppShell.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('../views/DashboardView.vue'),
        meta: { title: '工作台' },
      },
      {
        path: 'employees',
        name: 'employees',
        component: () => import('../views/EmployeesView.vue'),
        meta: { title: '员工管理', roles: ['admin', 'manager'] },
      },
      {
        path: 'projects',
        name: 'projects',
        component: () => import('../views/ProjectsView.vue'),
        meta: { title: '项目管理' },
      },
      {
        path: 'attendance',
        name: 'attendance',
        component: () => import('../views/AttendanceView.vue'),
        meta: { title: '考勤管理' },
      },
      {
        path: 'performance',
        name: 'performance',
        component: () => import('../views/PerformanceView.vue'),
        meta: { title: '绩效管理' },
      },
      {
        path: 'leaves',
        name: 'leaves',
        component: () => import('../views/LeavesView.vue'),
        meta: { title: '请假管理' },
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFoundView.vue'),
    meta: { public: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore(pinia)
  const isPublic = Boolean(to.meta.public)

  if (authStore.token && !authStore.user) {
    try {
      await authStore.restoreSession()
    } catch (_error) {
      authStore.logout()
    }
  }

  if (isPublic) {
    if (to.path === '/login' && authStore.isAuthenticated) {
      return { name: 'dashboard' }
    }
    return true
  }

  if (!authStore.isAuthenticated) {
    return { name: 'login' }
  }

  const allowedRoles = to.meta.roles
  if (allowedRoles && !allowedRoles.includes(authStore.roleCode)) {
    return { name: 'dashboard' }
  }

  if (!authStore.metaLoaded) {
    await authStore.loadBootstrap()
  }

  return true
})

export default router
