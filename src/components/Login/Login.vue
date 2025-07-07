<!-- 以下是对登录-注册页的设计 -->
<template>
    <!-- 登录-注册页总体 -->
    <div class="login_bgi">
        <h1 id="name">员工管理系统</h1>
        <h1 id="tech1" class="tech">MySQL</h1>
        <h1 id="tech2" class="tech">Vue</h1>
        <h1 id="tech3" class="tech">SpringBoot</h1>
        <h1 id="tech4" class="tech">MyBatis-Plus</h1>
        <h1 id="tech5" class="tech">VsCode</h1>
        <h1 id="tech6" class="tech">IDE</h1>
        <!-- 登录-注册内容 -->
        <div class="login_content">
            <!-- 路由展示 -->
           <router-view></router-view>
            <div class="author">
            <span>2300330216 刘懿辉 2300330210 高宏泽</span>
            <span>2300330133 卓慧明 2300330211 方焱 </span>
            </div>
        </div>

    </div>
</template>

<script setup>
import {   getCurrentInstance, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
const { proxy } = getCurrentInstance();
const router = useRouter()
// 设置初始跳转至登录页
onMounted(()=>{
    router.push('/loginMain')
})




</script>

<style lang="less" scoped>
.login_bgi {

    position: relative;
    height: 100vh;
    width: 100vw;
    background-image: url('../../assets/img/company.svg'); //设置图片背景
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: fixed;

    #name,
    .tech {
        display: inline;
        position: absolute;
    }

    #name {
        left: 17vw;
    }

    .tech {
        color: #cacaca
    }

    #tech1 {
        top: 10vh;
        left: 10vw
    }

    #tech2 {
        top: 22vh;
        left: 9vw
    }

    #tech3 {
        top: 34vh;
        left: 2vw
    }

    #tech4 {
        top: 47vh;
        left: 1vw
    }

    #tech5 {
        top: 60vh;
        left: 9vw
    }

    #tech6 {
        top: 72vh;
        left: 15vw
    }

    .login_content {
        display: inline;
        position: absolute;
        background-color: #45465e;
        border: 0.1vw solid #eaeaea;
        height: 100vh;
        width: 30.8vw;
        right: 1px;
        box-shadow: 0 0 2vh hsla(0, 0%, 79%, 0.849);
        opacity: 0.9;
        border-radius: 0.5vw;
        z-index: 0;
.el-menu-demo{
    width: 15vw;
    font-size: 2px;
    position: absolute;
    top:10vh;
    right: 5vw;
}
        .login-container {
            margin-top: 20vh;
        }

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
        .author{
            position: absolute;
            left: -6vw;
            bottom: 5vh;
         }

        :deep(.el-form-item__content) {
            justify-content: center;
        }

    }
}
</style>