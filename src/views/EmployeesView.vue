<template>
  <div class="page-view">
    <el-card class="page-card">
      <template #header>
        <div class="page-header">
          <div>
            <h2 class="page-title">员工管理</h2>
            <p class="page-subtitle">统一维护员工账号、组织归属与基础档案</p>
          </div>
          <el-button type="primary" @click="openCreateDialog">新增员工</el-button>
        </div>
      </template>

      <div class="filter-row">
        <el-input v-model="query.keyword" placeholder="搜索工号、姓名或用户名" clearable style="max-width: 280px" />
        <el-select v-model="query.dept_id" clearable placeholder="部门" style="width: 180px" :disabled="authStore.roleCode !== 'admin'">
          <el-option v-for="item in authStore.meta.departments" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-select v-model="query.role_id" clearable placeholder="角色" style="width: 180px">
          <el-option v-for="item in roleChoices" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="primary" plain @click="loadEmployees">查询</el-button>
      </div>

      <el-table :data="rows" class="table-compact" style="margin-top: 18px">
        <el-table-column prop="employee_no" label="工号" width="110" />
        <el-table-column prop="full_name" label="姓名" width="110" />
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column prop="department_name" label="部门" width="120" />
        <el-table-column prop="role_name" label="角色" width="120" />
        <el-table-column prop="title" label="岗位" width="140" />
        <el-table-column prop="email" label="邮箱" min-width="220" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="110" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="openEditDialog(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="display: flex; justify-content: flex-end; margin-top: 16px">
        <el-pagination
          v-model:current-page="query.page"
          v-model:page-size="query.page_size"
          layout="prev, pager, next, total"
          :total="total"
          @current-change="loadEmployees"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑员工' : '新增员工'" width="760">
      <el-form label-position="top">
        <div class="dialog-grid">
          <el-form-item label="工号">
            <el-input v-model="form.employee_no" :disabled="Boolean(editingId)" />
          </el-form-item>
          <el-form-item label="用户名">
            <el-input v-model="form.username" :disabled="Boolean(editingId)" />
          </el-form-item>
          <el-form-item label="姓名">
            <el-input v-model="form.full_name" />
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="form.email" />
          </el-form-item>
          <el-form-item label="手机">
            <el-input v-model="form.phone" />
          </el-form-item>
          <el-form-item label="岗位">
            <el-input v-model="form.title" />
          </el-form-item>
          <el-form-item label="学历">
            <el-select v-model="form.education">
              <el-option label="本科" value="本科" />
              <el-option label="硕士" value="硕士" />
              <el-option label="博士" value="博士" />
            </el-select>
          </el-form-item>
          <el-form-item label="部门">
            <el-select v-model="form.department_id" :disabled="authStore.roleCode !== 'admin'">
              <el-option v-for="item in authStore.meta.departments" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="form.role_id" :disabled="authStore.roleCode !== 'admin' && Boolean(editingId)">
              <el-option v-for="item in roleChoices" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="form.status">
              <el-option label="active" value="active" />
              <el-option label="inactive" value="inactive" />
            </el-select>
          </el-form-item>
          <el-form-item :label="editingId ? '重置密码（可选）' : '初始密码'">
            <el-input v-model="form.password" type="password" show-password />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="submitForm">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

import api from '../api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const query = reactive({
  keyword: '',
  dept_id: null,
  role_id: null,
  page: 1,
  page_size: 10,
})

const rows = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const saving = ref(false)
const editingId = ref(null)

const roleChoices = computed(() =>
  authStore.roleCode === 'admin'
    ? authStore.meta.roles
    : authStore.meta.roles.filter((item) => item.code === 'employee'),
)

const form = reactive({
  employee_no: '',
  username: '',
  full_name: '',
  email: '',
  phone: '',
  title: '',
  education: '本科',
  department_id: null,
  role_id: null,
  status: 'active',
  password: '',
})

function resetForm() {
  Object.assign(form, {
    employee_no: '',
    username: '',
    full_name: '',
    email: '',
    phone: '',
    title: '',
    education: '本科',
    department_id: authStore.roleCode === 'manager' ? authStore.user.department_id : null,
    role_id: roleChoices.value[0]?.id || null,
    status: 'active',
    password: '',
  })
}

async function loadEmployees() {
  const result = await api.employees.list(query)
  rows.value = result.items
  total.value = result.total
}

function openCreateDialog() {
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(row) {
  editingId.value = row.id
  Object.assign(form, {
    employee_no: row.employee_no,
    username: row.username,
    full_name: row.full_name,
    email: row.email,
    phone: row.phone,
    title: row.title,
    education: row.education,
    department_id: row.department_id,
    role_id: row.role_id,
    status: row.status,
    password: '',
  })
  dialogVisible.value = true
}

async function submitForm() {
  if (!form.full_name || !form.email || !form.department_id || !form.role_id) {
    ElMessage.warning('请补齐员工基础信息。')
    return
  }
  if (!editingId.value && (!form.employee_no || !form.username || !form.password)) {
    ElMessage.warning('新增员工时需填写工号、用户名和初始密码。')
    return
  }

  saving.value = true
  try {
    const payload = { ...form }
    if (editingId.value && !payload.password) {
      delete payload.password
    }
    if (editingId.value) {
      await api.employees.update(editingId.value, payload)
      ElMessage.success('员工信息已更新。')
    } else {
      await api.employees.create(payload)
      ElMessage.success('员工已创建。')
    }
    dialogVisible.value = false
    await loadEmployees()
    await authStore.loadBootstrap(true)
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  resetForm()
  await loadEmployees()
})
</script>
