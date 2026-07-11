import { defineStore } from 'pinia'

import api from '../api'
import { navigationItems } from '../utils/navigation'

function normalizeMeta(meta = {}) {
  return {
    departments: meta.departments || [],
    roles: meta.roles || [],
    employees: meta.employees || [],
    leaveTypes: meta.leaveTypes || meta.leave_types || [],
    projectStatuses: meta.projectStatuses || meta.project_statuses || [],
  }
}

export const useAuthStore = defineStore(
  'auth',
  {
    state: () => ({
      token: '',
      user: null,
      meta: {
        departments: [],
        roles: [],
        employees: [],
        leaveTypes: [],
        projectStatuses: [],
      },
      metaLoaded: false,
    }),
    getters: {
      isAuthenticated: (state) => Boolean(state.token),
      roleCode: (state) => state.user?.role_code || '',
      visibleNavigation(state) {
        return navigationItems.filter((item) => !item.roles || item.roles.includes(state.user?.role_code))
      },
      employeeOptions: (state) => state.meta.employees || [],
      dataScopeText: (state) => {
        if (state.user?.role_code === 'admin') {
          return '当前账号可查看系统全部数据。'
        }
        if (state.user?.role_code === 'manager') {
          return '当前账号仅可查看本部门数据。'
        }
        return '当前账号仅可查看本人数据，以及本人参与的项目。'
      },
    },
    actions: {
      async login(payload) {
        const { token, user } = await api.auth.login(payload)
        this.token = token
        this.user = user
        await this.loadBootstrap(true)
      },
      async restoreSession() {
        if (!this.token) {
          return
        }
        this.user = await api.auth.me()
        await this.loadBootstrap(true)
      },
      async loadBootstrap(force = false) {
        if (this.metaLoaded && !force) {
          return this.meta
        }
        this.meta = normalizeMeta(await api.meta.options())
        this.metaLoaded = true
        return this.meta
      },
      logout() {
        this.token = ''
        this.user = null
        this.metaLoaded = false
        this.meta = {
          departments: [],
          roles: [],
          employees: [],
          leaveTypes: [],
          projectStatuses: [],
        }
      },
    },
    persist: {
      paths: ['token', 'user'],
      storage: sessionStorage,
    },
  },
)
