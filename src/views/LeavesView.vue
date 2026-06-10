<template>
  <div class="page-view">
    <el-row :gutter="18">
      <el-col :lg="9" :xs="24">
        <el-card class="page-card">
          <template #header>
            <div class="page-header">
              <div>
                <h2 class="page-title">发起请假</h2>
                <p class="page-subtitle">申请单将自动流转到当前可用审批人</p>
              </div>
            </div>
          </template>

          <el-form label-position="top">
            <el-form-item label="请假类型">
              <el-select v-model="form.leave_type" style="width: 100%">
                <el-option v-for="item in authStore.meta.leaveTypes" :key="item" :label="item" :value="item" />
              </el-select>
            </el-form-item>
            <el-form-item label="开始日期">
              <el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
            <el-form-item label="结束日期">
              <el-date-picker v-model="form.end_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
            <el-form-item label="请假原因">
              <el-input v-model="form.reason" type="textarea" :rows="4" />
            </el-form-item>
            <el-button type="primary" :loading="submitting" @click="submitLeave">提交申请</el-button>
          </el-form>
        </el-card>
      </el-col>

      <el-col :lg="15" :xs="24">
        <el-card class="page-card">
          <template #header>
            <div class="page-header">
              <div>
                <h2 class="page-title">请假列表</h2>
                <p class="page-subtitle">个人申请和审批任务统一查看</p>
              </div>
            </div>
          </template>

          <el-tabs v-model="activeTab">
            <el-tab-pane label="我的申请" name="mine">
              <el-table :data="mineRows" class="table-compact">
                <el-table-column prop="leave_type" label="类型" width="100" />
                <el-table-column prop="start_date" label="开始日期" width="120">
                  <template #default="{ row }">{{ formatDate(row.start_date) }}</template>
                </el-table-column>
                <el-table-column prop="end_date" label="结束日期" width="120">
                  <template #default="{ row }">{{ formatDate(row.end_date) }}</template>
                </el-table-column>
                <el-table-column prop="days" label="天数" width="80" />
                <el-table-column prop="approver_name" label="审批人" width="120" />
                <el-table-column label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="resolveLeaveTag(row.status)">{{ row.status }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="reason" label="原因" min-width="180" show-overflow-tooltip />
                <el-table-column prop="decision_comment" label="审批意见" min-width="180" show-overflow-tooltip />
              </el-table>
            </el-tab-pane>

            <el-tab-pane v-if="authStore.roleCode !== 'employee'" label="待我审批" name="approvals">
              <el-table :data="approvalRows" class="table-compact">
                <el-table-column prop="employee_name" label="申请人" width="110" />
                <el-table-column prop="department_name" label="部门" width="110" />
                <el-table-column prop="leave_type" label="类型" width="90" />
                <el-table-column prop="days" label="天数" width="80" />
                <el-table-column label="开始日期" width="120">
                  <template #default="{ row }">{{ formatDate(row.start_date) }}</template>
                </el-table-column>
                <el-table-column label="结束日期" width="120">
                  <template #default="{ row }">{{ formatDate(row.end_date) }}</template>
                </el-table-column>
                <el-table-column prop="reason" label="原因" min-width="180" show-overflow-tooltip />
                <el-table-column label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="resolveLeaveTag(row.status)">{{ row.status }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="160" fixed="right">
                  <template #default="{ row }">
                    <template v-if="row.status === 'pending'">
                      <el-button type="success" link @click="openDecisionDialog(row, 'approved')">批准</el-button>
                      <el-button type="danger" link @click="openDecisionDialog(row, 'rejected')">驳回</el-button>
                    </template>
                    <span v-else>-</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="decisionVisible" :title="decisionForm.status === 'approved' ? '批准请假' : '驳回请假'" width="520">
      <el-form label-position="top">
        <el-form-item label="审批意见">
          <el-input v-model="decisionForm.decision_comment" type="textarea" :rows="4" placeholder="请输入审批意见" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="decisionVisible = false">取消</el-button>
        <el-button type="primary" :loading="decisionSubmitting" @click="submitDecision">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

import api from '../api'
import { useAuthStore } from '../stores/auth'
import { formatDate, resolveLeaveTag } from '../utils/formatters'

const authStore = useAuthStore()

const activeTab = ref('mine')
const mineRows = ref([])
const approvalRows = ref([])
const submitting = ref(false)
const decisionVisible = ref(false)
const decisionSubmitting = ref(false)
const currentLeaveId = ref(null)

const form = reactive({
  leave_type: '',
  start_date: '',
  end_date: '',
  reason: '',
})

const decisionForm = reactive({
  status: 'approved',
  decision_comment: '',
})

function resetForm() {
  Object.assign(form, {
    leave_type: authStore.meta.leaveTypes[0] || '',
    start_date: '',
    end_date: '',
    reason: '',
  })
}

async function loadData() {
  mineRows.value = await api.leaves.list({ scope: 'mine' })
  if (authStore.roleCode !== 'employee') {
    approvalRows.value = await api.leaves.list({ scope: 'approvals' })
  }
}

async function submitLeave() {
  if (!form.leave_type || !form.start_date || !form.end_date || !form.reason) {
    ElMessage.warning('请补齐请假信息。')
    return
  }
  submitting.value = true
  try {
    await api.leaves.create(form)
    ElMessage.success('请假申请已提交。')
    resetForm()
    await loadData()
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    submitting.value = false
  }
}

function openDecisionDialog(row, status) {
  currentLeaveId.value = row.id
  decisionForm.status = status
  decisionForm.decision_comment = ''
  decisionVisible.value = true
}

async function submitDecision() {
  decisionSubmitting.value = true
  try {
    await api.leaves.decide(currentLeaveId.value, decisionForm)
    ElMessage.success('审批结果已提交。')
    decisionVisible.value = false
    await loadData()
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    decisionSubmitting.value = false
  }
}

onMounted(async () => {
  resetForm()
  await loadData()
})
</script>
