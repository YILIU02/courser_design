<template>
  <!-- 注册前的信息收集 -->
  <div>
    <el-form :model="SubmitForm" class="login-container">
      <h1> 员工管理系统 </h1>
      <h1>注册信息填写</h1>
      <el-form-item>
        <el-input type="input" placeholder="请输入工号" v-model="SubmitForm.empId"></el-input>
        <el-input type="input" placeholder="请输入姓名" v-model="SubmitForm.empName"></el-input>
        <el-select v-model="SubmitForm.deptId" :value-on-clear="null" clearable placeholder="选择部门" style="width: 240px">
          <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type='primary' @click="handNext">下一步</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { useRegDataStore } from '../../stores'
import api from '../../untils/api/register'
const router = useRouter()
const routNexter = useRouter()
const store = useRegDataStore()
const SubmitForm = store.SubmitForm //员工信息表单
const updateSubmit = store.updateSubmit //下一步后清除表单
const options = store.options //选项框内容

const handNext = () => {//下一步路由跳转
  api.register1(store.SubmitForm).then((data) => {
    console.log(data);
    updateSubmit()
    router.push('/registerSub')
  }).catch((err)=>{
    ElMessage({
            message: err,
            type: 'warning',
            })
  })

}
</script>

<style lang="less" scoped>
.login-container {
  margin-top: 20vh;
}


.el-input,
.el-select {
  width: 18vw;
  height: 5vh;
  font-size: 2vh;
  margin: 1vh;
}

.el-button {
  height: 5vh;
  width: 10vh;
  font-size: 2vh;
}

span {
  font-size: 2vh;
  color: #fff;
  margin-left: 40%;
}

h1 {
  text-align: center;
  margin-bottom: 1vh;
  color: #fff;
}

.author {
  position: absolute;
  left: -6vw;
  bottom: 5vh;
}

:deep(.el-form-item__content) {
  justify-content: center;
}
</style>