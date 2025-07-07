<template>
    <!-- 登录表单 -->
    <div>
        <el-form :model="loginForm" class="login-container">
            <h1>欢迎登录</h1>
            <h1> 员工管理系统 </h1>
            <el-form-item>
                <el-input type="input" placeholder="请输入账号" v-model="loginForm.username"></el-input>
                <el-input type="password" placeholder="请输入密码" show-password v-model="loginForm.password"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type='primary' @click="handLogin()">登录</el-button>
            </el-form-item>
        </el-form>
        <div class="reg">
        <p >暂无账号？<span @click="handReg">前往注册...</span></p>
        </div>
    </div>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import { useLoginDataStore } from "../../stores";
import api from '../../untils/api/login'
const router = useRouter()
const store = useLoginDataStore ()
const loginForm = store.loginForm//设置表单内容
const updateloginForm=store.updateloginForm //登录后清除表单数据
const handLogin = () => { //登陆后路由跳转
 if(loginForm.username&&loginForm.password){
        api.Login({username:loginForm.username,
            password:loginForm.password
        }).then(({data}) => {
           store.token=data.token
           localStorage.setItem('token',store.token)
        ElMessage({
            message: '成功登录',
            type: 'success',
        })
        
          router.push('/home')
        }).catch((err) => {
            ElMessage({
            message: err,
            type: 'warning',
            })
        })
    
  
    }else{
        ElMessage({
            message: '账户密码不能为空',
            type: 'warning',
        })
    }
    updateloginForm()
   
}
const handReg=()=>{//选择注册路由跳转
    router.push("/registerContent")
}
</script>

<style lang="less" scoped>
.login-container {
    margin-top: 20vh;
    .el-input {
    width: 25vw;
    height: 5vh;
    font-size: 2vh;
    margin: 2vh;
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
.reg{
    width: 100%;
   p {
    font-size: 2vh;
   color: #fff;
    text-align: center;
    span{
        color: #00a8ff;
         cursor: pointer;
    }
}
}


</style>