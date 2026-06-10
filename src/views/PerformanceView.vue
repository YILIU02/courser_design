<template>
  <div class="page-view">
    <div class="stats-grid">
      <div class="page-card soft-panel">
        <div class="stat-label">当前筛选年度</div>
        <div class="stat-value" style="color: var(--brand-strong)">{{ result.current_year || '-' }}</div>
      </div>
      <div class="page-card soft-panel">
        <div class="stat-label">平均绩效分</div>
        <div class="stat-value" style="color: var(--brand-strong)">{{ result.average_score }}</div>
      </div>
    </div>

    <el-card class="page-card">
      <template #header>
        <div class="page-header">
          <div>
            <h2 class="page-title">绩效管理</h2>
            <p class="page-subtitle">年度绩效结果与考核评语集中查看</p>
          </div>
        </div>
      </template>

      <div class="filter-row">
        <el-select v-model="query.year" clearable placeholder="年度" style="width: 180px">
          <el-option v-for="year in result.years" :key="year" :label="`${year}`" :value="year" />
        </el-select>
        <el-select v-if="authStore.roleCode !== 'employee'" v-model="query.employee_id" clearable filterable placeholder="员工" style="width: 220px">
          <el-option v-for="item in authStore.employeeOptions" :key="item.id" :label="`${item.full_name} / ${item.employee_no}`" :value="item.id" />
        </el-select>
        <el-switch v-model="latestOnly" active-text="仅看最新" inactive-text="按条件查询" />
        <el-button type="primary" plain @click="loadPerformance">查询</el-button>
      </div>

      <el-table :data="result.items" style="margin-top: 18px" class="table-compact">
        <el-table-column prop="employee_name" label="姓名" width="120" />
        <el-table-column prop="department_name" label="部门" width="120" />
        <el-table-column prop="year" label="年度" width="90" />
        <el-table-column prop="business_score" label="业务" width="90" />
        <el-table-column prop="skill_score" label="技能" width="90" />
        <el-table-column prop="collaboration_score" label="协作" width="90" />
        <el-table-column prop="attendance_score" label="考勤" width="90" />
        <el-table-column label="总分" width="100">
          <template #default="{ row }">
            <el-tag :type="resolveScoreTag(row.total_score)">{{ row.total_score }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="grade" label="等级" width="90" />
        <el-table-column prop="reviewer_name" label="考核人" width="120" />
        <el-table-column prop="comment" label="评语" min-width="280" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'

import api from '../api'
import { useAuthStore } from '../stores/auth'
import { resolveScoreTag } from '../utils/formatters'

const authStore = useAuthStore()

const latestOnly = ref(true)
const query = reactive({
  year: null,
  employee_id: null,
})

const result = reactive({
  items: [],
  years: [],
  current_year: null,
  average_score: 0,
})

async function loadPerformance() {
  Object.assign(
    result,
    await api.performance.list({
      year: query.year,
      employee_id: query.employee_id,
      latest_only: latestOnly.value && !query.year ? 1 : 0,
    }),
  )
}

onMounted(loadPerformance)
</script>
