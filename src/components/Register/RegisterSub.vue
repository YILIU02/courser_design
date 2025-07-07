<template>
    <!-- 注册的表单 -->
    <div>
        <el-form :model="RegForm" class="login-container">
            <h1> 员工管理系统 </h1>
            <h1>用户信息填写</h1>
            <el-form-item>
                <el-input type="input" placeholder="请输入工号" v-model="RegForm.empId"></el-input>
                <el-input type="input" placeholder="请输入账号" v-model="RegForm.username"></el-input>
                <el-input type="password" show-password placeholder="请输入密码" v-model="RegForm.password"></el-input>
                <el-input type="password" show-password placeholder="请再次输入密码" v-model="store.check"></el-input>
                <el-radio-group v-model="RegForm.roleId">
                    <el-radio v-for="(v, i) in roleList" :value="i" @change="store.roleId=i">{{ v }}</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item>
                <el-button type='primary' @click="handReg()">注册</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import { useRegDataStore } from "../../stores";
import api from '../../untils/api/register'
const store = useRegDataStore()
const roleList = store.roleList
const router = useRouter()
const RegForm = store.RegForm //注册表单
const updateReg = store.updateRegForm //表单清除
const handReg = () => {//注册后跳转
    if(store.check!=RegForm.password){
        ElMessage({
            type:'warning',
            message:'两次密码不一致'
        })
    }else{
    api.register2({...store.RegForm,roleId:store.RegForm.roleId+1}).then((data) => {    
        ElMessage({type:'success',
            message:'注册成功'
        })
          updateReg()
        router.push('/loginMain')
    }).catch((err) => {
    ElMessage({
            message: err,
            type: 'warning',
            })
  })}
}

</script>

<style lang="less" scoped>
.login-container {
    margin-top: 10vh;

    .el-input {
        width: 25vw;
        height: 5vh;
        font-size: 2vh;
        margin: 2vh;

        .el-input__inner {
            color: #333;
            /* 设置字体颜色为深灰色 */
        }
    }

    .el-button {
        height: 5vh;
        width: 10vh;
        font-size: 2vh;
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

}
</style>