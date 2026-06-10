<template>
  <div class="page-view">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">员工总数</div>
        <div class="stat-value">{{ overview.stats.employee_total }}</div>
        <div class="stat-footnote">按当前角色可见范围汇总</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">项目总数</div>
        <div class="stat-value">{{ overview.stats.project_total }}</div>
        <div class="stat-footnote">覆盖在途与计划项目</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">待处理请假</div>
        <div class="stat-value">{{ overview.stats.pending_leave_total }}</div>
        <div class="stat-footnote">待审批或待确认流程</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">今日打卡完成</div>
        <div class="stat-value">
          {{ overview.stats.attendance_completed }}/{{ overview.stats.attendance_total }}
        </div>
        <div class="stat-footnote">签到完成人数统计</div>
      </div>
    </div>

    <el-row :gutter="18">
      <el-col :lg="16" :xs="24">
        <el-card class="page-card">
          <template #header>
            <div class="page-header">
              <div>
                <h2 class="page-title">最近项目</h2>
                <p class="page-subtitle">展示最近更新的关键项目与人员结构</p>
              </div>
            </div>
          </template>
          <el-table :data="overview.recent_projects" class="table-compact">
            <el-table-column prop="project_code" label="项目编号" width="140" />
            <el-table-column prop="name" label="项目名称" min-width="200" />
            <el-table-column prop="department_name" label="部门" width="120" />
            <el-table-column prop="manager_name" label="负责人" width="120" />
            <el-table-column prop="member_count" label="成员数" width="100" />
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="resolveProjectTag(row.status)">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="进度" min-width="180">
              <template #default="{ row }">
                <el-progress :percentage="row.progress" :stroke-width="10" />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :lg="8" :xs="24">
        <el-card class="page-card dashboard-side-card">
          <template #header>
            <div class="page-header">
              <div>
                <h2 class="page-title">我的考勤</h2>
                <p class="page-subtitle">个人当日签到签退状态</p>
              </div>
            </div>
          </template>
          <div class="soft-panel">
            <div class="detail-row">
              <span>签到时间</span>
              <strong>{{ formatDateTime(overview.today_attendance?.check_in) }}</strong>
            </div>
            <div class="detail-row">
              <span>签退时间</span>
              <strong>{{ formatDateTime(overview.today_attendance?.check_out) }}</strong>
            </div>
            <div class="detail-row">
              <span>状态</span>
              <el-tag :type="attendanceTag">{{ overview.today_attendance?.status || '未打卡' }}</el-tag>
            </div>
            <div class="button-row" v-if="authStore.roleCode !== 'admin'">
              <el-button type="primary" plain :disabled="Boolean(overview.today_attendance?.check_in)" @click="checkIn">
                签到
              </el-button>
              <el-button type="primary" :disabled="!overview.today_attendance?.check_in || Boolean(overview.today_attendance?.check_out)" @click="checkOut">
                签退
              </el-button>
            </div>
          </div>

          <div class="status-list">
            <div v-for="item in overview.project_status" :key="item.status" class="status-item">
              <div>{{ item.status }}</div>
              <strong>{{ item.count }}</strong>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="page-card">
      <template #header>
        <div class="page-header">
          <div>
            <h2 class="page-title">绩效快照</h2>
            <p class="page-subtitle">基于最新年度结果的高分员工清单</p>
          </div>
        </div>
      </template>
      <el-table :data="overview.latest_performance" class="table-compact">
        <el-table-column prop="employee_name" label="姓名" width="120" />
        <el-table-column prop="department_name" label="部门" width="120" />
        <el-table-column prop="year" label="年度" width="100" />
        <el-table-column prop="reviewer_name" label="考核人" width="120" />
        <el-table-column prop="total_score" label="总分" width="100">
          <template #default="{ row }">
            <el-tag :type="resolveScoreTag(row.total_score)">{{ row.total_score }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="comment" label="评语" min-width="260" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'

import api from '../api'
import { useAuthStore } from '../stores/auth'
import { formatDateTime, resolveProjectTag, resolveScoreTag } from '../utils/formatters'

const authStore = useAuthStore()

const overview = reactive({
  stats: {
    employee_total: 0,
    project_total: 0,
    pending_leave_total: 0,
    attendance_total: 0,
    attendance_completed: 0,
  },
  project_status: [],
  recent_projects: [],
  latest_performance: [],
  today_attendance: null,
})

const attendanceTag = computed(() => {
  const status = overview.today_attendance?.status
  if (status === 'present') return 'success'
  if (status === 'checked_in') return 'warning'
  return 'info'
})

async function loadOverview() {
  Object.assign(overview, await api.dashboard.overview())
}

async function checkIn() {
  try {
    await api.attendance.checkIn()
    ElMessage.success('签到成功。')
    await loadOverview()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

async function checkOut() {
  try {
    await api.attendance.checkOut()
    ElMessage.success('签退成功。')
    await loadOverview()
  } catch (error) {
    ElMessage.error(error.message)
  }
}

onMounted(loadOverview)
</script>

<style scoped>
.dashboard-side-card {
  height: 100%;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px dashed rgba(15, 35, 70, 0.1);
}

.detail-row:last-child {
  border-bottom: none;
}

.button-row {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

.status-list {
  display: grid;
  gap: 12px;
  margin-top: 18px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-radius: 16px;
  background: #f5f8fc;
}
</style>
