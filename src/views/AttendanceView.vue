<template>
  <div class="page-view">
    <el-card class="page-card">
      <template #header>
        <div class="page-header">
          <div>
            <h2 class="page-title">考勤管理</h2>
            <p class="page-subtitle">个人打卡与团队考勤记录统一查询</p>
          </div>
        </div>
      </template>

      <div class="soft-panel" style="margin-bottom: 18px">
        <div class="page-header">
          <div>
            <strong>今日状态</strong>
            <div class="page-subtitle">签到 {{ formatDateTime(data.today?.check_in) }}，签退 {{ formatDateTime(data.today?.check_out) }}</div>
          </div>
          <div v-if="authStore.roleCode !== 'admin'" style="display: flex; gap: 10px">
            <el-button type="primary" plain :disabled="Boolean(data.today?.check_in)" @click="checkIn">签到</el-button>
            <el-button type="primary" :disabled="!data.today?.check_in || Boolean(data.today?.check_out)" @click="checkOut">签退</el-button>
          </div>
        </div>
      </div>

      <div class="filter-row">
        <el-input v-model="query.keyword" placeholder="搜索工号或姓名" clearable style="max-width: 280px" />
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
        />
        <el-button type="primary" plain @click="loadAttendance">查询</el-button>
      </div>

      <el-table :data="data.items" style="margin-top: 18px" class="table-compact">
        <el-table-column prop="work_date" label="日期" width="120">
          <template #default="{ row }">{{ formatDate(row.work_date) }}</template>
        </el-table-column>
        <el-table-column prop="employee_no" label="工号" width="110" />
        <el-table-column prop="employee_name" label="姓名" width="120" />
        <el-table-column prop="department_name" label="部门" width="120" />
        <el-table-column label="签到时间" width="180">
          <template #default="{ row }">{{ formatDateTime(row.check_in) }}</template>
        </el-table-column>
        <el-table-column label="签退时间" width="180">
          <template #default="{ row }">{{ formatDateTime(row.check_out) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="row.status === 'present' ? 'success' : row.status === 'checked_in' ? 'warning' : 'info'">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="160" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

import api from '../api'
import { useAuthStore } from '../stores/auth'
import { formatDate, formatDateTime } from '../utils/formatters'

const authStore = useAuthStore()
const dateRange = ref([])
const query = reactive({
  keyword: '',
})
const data = reactive({
  today: null,
  items: [],
})

async function loadAttendance() {
  const params = {
    keyword: query.keyword,
    start_date: dateRange.value?.[0],
    end_date: dateRange.value?.[1],
  }
  Object.assign(data, await api.attendance.list(params))
}

async function checkIn() {
  try {
    await api.attendance.checkIn()
    ElMessage.success('签到成功。')
    await loadAttendance()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

async function checkOut() {
  try {
    await api.attendance.checkOut()
    ElMessage.success('签退成功。')
    await loadAttendance()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

onMounted(loadAttendance)
</script>
