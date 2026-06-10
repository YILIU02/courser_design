<template>
  <div class="page-view">
    <el-card class="page-card">
      <template #header>
        <div class="page-header">
          <div>
            <h2 class="page-title">项目管理</h2>
            <p class="page-subtitle">按部门、负责人和成员视角维护项目全生命周期</p>
          </div>
          <el-button v-if="authStore.roleCode !== 'employee'" type="primary" @click="openCreateDialog">新增项目</el-button>
        </div>
      </template>

      <div class="filter-row">
        <el-input v-model="query.keyword" placeholder="搜索项目编号或名称" clearable style="max-width: 280px" />
        <el-select v-model="query.status" clearable placeholder="状态" style="width: 180px">
          <el-option v-for="item in authStore.meta.projectStatuses" :key="item" :label="item" :value="item" />
        </el-select>
        <el-select v-model="query.dept_id" clearable placeholder="部门" style="width: 180px" :disabled="authStore.roleCode !== 'admin'">
          <el-option v-for="item in authStore.meta.departments" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="primary" plain @click="loadProjects">查询</el-button>
      </div>

      <el-table :data="rows" style="margin-top: 18px" class="table-compact">
        <el-table-column prop="project_code" label="项目编号" width="130" />
        <el-table-column prop="name" label="项目名称" min-width="180" />
        <el-table-column prop="department_name" label="部门" width="120" />
        <el-table-column prop="manager_name" label="负责人" width="120" />
        <el-table-column prop="member_count" label="成员数" width="90" />
        <el-table-column label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="resolveProjectTag(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="100" />
        <el-table-column label="预算" width="120">
          <template #default="{ row }">{{ formatCurrency(row.budget) }}</template>
        </el-table-column>
        <el-table-column label="进度" min-width="180">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" :stroke-width="10" />
          </template>
        </el-table-column>
        <el-table-column label="成员" min-width="220" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.members.map((member) => member.full_name).join('、') }}
          </template>
        </el-table-column>
        <el-table-column v-if="authStore.roleCode !== 'employee'" label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="openEditDialog(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑项目' : '新增项目'" width="860">
      <el-form label-position="top">
        <div class="dialog-grid">
          <el-form-item label="项目编号">
            <el-input v-model="form.project_code" :disabled="Boolean(editingId)" />
          </el-form-item>
          <el-form-item label="项目名称">
            <el-input v-model="form.name" />
          </el-form-item>
          <el-form-item label="部门">
            <el-select v-model="form.department_id" :disabled="authStore.roleCode !== 'admin'">
              <el-option v-for="item in authStore.meta.departments" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="负责人">
            <el-select v-model="form.manager_id" filterable>
              <el-option v-for="item in scopedEmployees" :key="item.id" :label="`${item.full_name} / ${item.employee_no}`" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="项目状态">
            <el-select v-model="form.status">
              <el-option v-for="item in authStore.meta.projectStatuses" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="优先级">
            <el-select v-model="form.priority">
              <el-option label="high" value="high" />
              <el-option label="medium" value="medium" />
              <el-option label="low" value="low" />
            </el-select>
          </el-form-item>
          <el-form-item label="开始日期">
            <el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
          </el-form-item>
          <el-form-item label="结束日期">
            <el-date-picker v-model="form.end_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
          </el-form-item>
          <el-form-item label="项目预算">
            <el-input-number v-model="form.budget" :min="0" :step="10000" style="width: 100%" />
          </el-form-item>
          <el-form-item label="当前进度">
            <el-slider v-model="form.progress" show-input />
          </el-form-item>
          <el-form-item label="项目成员" class="full-span">
            <el-select v-model="form.member_ids" multiple filterable collapse-tags style="width: 100%">
              <el-option v-for="item in scopedEmployees" :key="item.id" :label="`${item.full_name} / ${item.department_name}`" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="项目说明" class="full-span">
            <el-input v-model="form.summary" type="textarea" :rows="4" />
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
import { formatCurrency, resolveProjectTag } from '../utils/formatters'

const authStore = useAuthStore()

const query = reactive({
  keyword: '',
  status: '',
  dept_id: null,
})

const rows = ref([])
const dialogVisible = ref(false)
const saving = ref(false)
const editingId = ref(null)

const form = reactive({
  project_code: '',
  name: '',
  department_id: null,
  manager_id: null,
  status: 'planned',
  priority: 'medium',
  progress: 0,
  budget: 0,
  start_date: '',
  end_date: '',
  member_ids: [],
  summary: '',
})

const scopedEmployees = computed(() => {
  const targetDeptId = form.department_id || authStore.user.department_id
  return authStore.employeeOptions.filter(
    (item) => authStore.roleCode === 'admin' ? item.department_id === targetDeptId : item.department_id === authStore.user.department_id,
  )
})

function resetForm() {
  Object.assign(form, {
    project_code: '',
    name: '',
    department_id: authStore.roleCode === 'manager' ? authStore.user.department_id : null,
    manager_id: null,
    status: 'planned',
    priority: 'medium',
    progress: 0,
    budget: 0,
    start_date: '',
    end_date: '',
    member_ids: [],
    summary: '',
  })
}

async function loadProjects() {
  rows.value = await api.projects.list(query)
}

function openCreateDialog() {
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(row) {
  editingId.value = row.id
  Object.assign(form, {
    project_code: row.project_code,
    name: row.name,
    department_id: row.department_id,
    manager_id: row.manager_id,
    status: row.status,
    priority: row.priority,
    progress: row.progress,
    budget: row.budget,
    start_date: row.start_date,
    end_date: row.end_date,
    member_ids: row.members.map((member) => member.id),
    summary: row.summary,
  })
  dialogVisible.value = true
}

async function submitForm() {
  if (!form.project_code || !form.name || !form.department_id || !form.manager_id || !form.start_date) {
    ElMessage.warning('请补齐项目核心信息。')
    return
  }
  saving.value = true
  try {
    if (editingId.value) {
      await api.projects.update(editingId.value, form)
      ElMessage.success('项目已更新。')
    } else {
      await api.projects.create(form)
      ElMessage.success('项目已创建。')
    }
    dialogVisible.value = false
    await loadProjects()
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  resetForm()
  await loadProjects()
})
</script>
