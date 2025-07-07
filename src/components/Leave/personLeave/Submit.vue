<template>
  <div class="leave-application-container">
  

    <el-card class="form-card">
          <div class="header">
            <h1>请假申请表</h1>
    </div>
      
      <el-form ref="leaveForm" :model="form" :rules="rules" label-width="120px" label-position="top">
        <div class="form-row">
          <el-form-item label="工号" prop="empId" class="form-item half-width">
           <el-input placeholder="请输入工号" clearable v-model="form.empId"></el-input>
          </el-form-item>
          
          <el-form-item label="姓名" prop="empName" class="form-item half-width">
            <el-input placeholder="请输入姓名" clearable v-model="form.empName"></el-input>
          </el-form-item>
        </div>
        <!-- 请假类型 -->
        <el-form-item label="请假类型" prop="type" class="form-item">
          <el-select v-model="form.leaveType" placeholder="请选择请假类型" style="width: 100%">
            <el-option v-for="type in leaveTypes" :key="type.value" :label="type.label" :value="type.value" />
          </el-select>
        </el-form-item>

        <!-- 时间范围 -->
        <div class="form-row">
          <el-form-item label="开始时间" prop="startDate" class="form-item half-width">
            <el-date-picker
              v-model="form.startDate"
              type="date"
              placeholder="选择开始日期和时间"
              value-format="YYYY-MM-DD"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="结束时间" prop="endDate" class="form-item half-width">
            <el-date-picker
              v-model="form.endDate"
              type="date"
              placeholder="选择结束日期和时间"
              value-format="YYYY-MM-DD"
              style="width: 100%"
            />
          </el-form-item>
        </div>

        <!-- 时长计算 -->
        <el-form-item label="请假时长" class="form-item">
          <div class="duration-display">
            <span>{{ calculatedDuration }}</span>

          </div>
        </el-form-item>


        <!-- 审批人 -->
        <el-form-item label="审批人" prop="approver" class="form-item">
          <el-select v-model="form.approver" placeholder="请选择审批人" style="width: 100%">
            <el-option
              v-for="person in approvers"
              :key="person.id"
              :label="person.name + ' (部长)'"
              :value="person.id"
            />
          </el-select>
        </el-form-item>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button type="primary" @click="submitForm" :loading="submitting">提交申请</el-button>
          <el-button @click="resetForm">重置</el-button>
  
        </div>
      </el-form>
    </el-card>

    <!-- 提交成功对话框 -->
    <el-dialog v-model="dialogVisible" title="提交成功" width="30%" center>
      <div class="success-dialog">
        <el-icon class="success-icon"><CircleCheck /></el-icon>
        <p>您的请假申请已成功提交！</p>
      </div>
      <template #footer>
        <el-button type="primary" @click="dialogVisible = false">确定</el-button>
        <el-button @click="printApplication">打印申请</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { CircleCheck, Message, Upload } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'
import api from '../../../untils/api/leave'
import hapi from '../../../untils/api/human'
import { useMainDataStore } from '../../../stores'
onMounted(async()=>{

approvers.value=[ await hapi.getBoss(dstore.uesrInfo.deptId).then(({data})=>{
  return {
  id:data[0].id,
  name:data[0].empName
 }}
 )]
 
})
const days=ref('')
// 表单数据
const dstore=useMainDataStore()
const form = ref({
 
  empId: null,
  empName:'',
  deptId: dstore.uesrInfo.deptId,
  leaveType: '',
  startDate: '',
endDate:'',
  days: '',
  approver: ''

})


// 表单验证规则
const rules = {
     empId: [
    { required: true, message: '请输入工号', trigger: 'change' }
  ],
     empName: [
    { required: true, message: '请输入姓名', trigger: 'change' }
  ],
  leaveType: [
    { required: true, message: '请选择请假类型', trigger: 'change' }
  ],
  startDate: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  endDate: [
    { required: true, message: '请选择结束时间', trigger: 'change' },
    { validator: validateEndTime, trigger: 'change' }
  ],
  approver: [
    { required: true, message: '请选择审批人', trigger: 'change' }
  ]
}

// 验证结束时间
function validateEndTime(rule, value, callback) {
  if (!form.value.startDate) {
    callback(new Error('请先选择开始时间'))
  } else if (dayjs(value).isBefore(dayjs(form.value.startDate))) {
    callback(new Error('结束时间不能早于开始时间'))
  } else {
    callback()
  }
}

// 请假类型选项
const leaveTypes = [
  { value: 'sick', label: '病假' },
  { value: 'annual', label: '年假' },
  { value: 'personal', label: '事假' },
  { value: 'marriage', label: '婚假' },
  { value: 'maternity', label: '产假' },
  { value: 'paternity', label: '陪产假' },
  { value: 'bereavement', label: '丧假' },
  { value: 'other', label: '其他' }
]

// 审批人选项
const approvers = ref([])

const calculatedDuration = computed(() => {
  if (!form.value.startDate || !form.value.endDate) return '0天'
  
  const start = dayjs(form.value.startDate)
  const end = dayjs(form.value.endDate)
  
  if (end.isBefore(start)) return '结束时间不能早于开始时间'
  
  // 计算小时差
  const hours = end.diff(start, 'hour', true)
  
  // 转换为天和小时
  const days = Math.floor(hours / 8)
  const remainingHours = hours % 8
  
  let result = ''
  if (days > 0) result += `${days}天`
  
  if (remainingHours > 0) result += `${remainingHours.toFixed(1)}小时`
  
  form.value.days = days

  
  return result || '0小时'
})



// 提交状态
const submitting = ref(false)
const dialogVisible = ref(false)


// 提交表单
function submitForm() {

 
 api.submit({
   empId: form.value.empId,
  deptId: dstore.uesrInfo.deptId,
  leaveType: form.value.leaveType,
  startDate: form.value.startDate,
  days: form.value.days,
  approver: form.value.approver
 }).then((data)=>{
  console.log(data);
  ElMessage({
    type:'success',
    message:'申请提交成功'
  })
  
 }
).catch((err)=>{
  ElMessage({
    type:'warning',
    message:err
  })
})
 
}

// 重置表单
function resetForm() {
  leaveForm.value.resetFields()
  fileList.value = []
  ElMessage.info('表单已重置')
}

// 保存草稿

  
 


// 表单引用

</script>

<style scoped>
.leave-application-container {
  max-width: 40%;
  margin: 0 auto;
  padding: 20px;
  max-height: 43em;
  overflow-y: auto;
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.header {
  text-align: center;

}

.header h1 {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 10px;
}

.header p {
  color: #7f8c8d;
  font-size: 16px;
}

.required {
  color: #f56c6c;
  margin-right: 4px;
}

.form-card {
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
 
}



.form-row {
  display: flex;
  gap: 20px;
}

.half-width {
  flex: 1;
}

.duration-display {
  display: flex;
  align-items: center;
  gap: 15px;
}

.duration-display span {
  font-size: 18px;
  color: #409eff;
  font-weight: 500;
}

.upload-tip {
  font-size: 13px;
  color: #909399;
  margin-top: 8px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
}

.success-dialog {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  font-size: 60px;
  color: #67c23a;
  margin-bottom: 20px;
}

.success-dialog p {
  margin: 10px 0;
  font-size: 16px;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .half-width {
    width: 100%;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 10px;
  }
  
  .form-actions .el-button {
    width: 100%;
    margin-left: 0 !important;
  }
}
</style>