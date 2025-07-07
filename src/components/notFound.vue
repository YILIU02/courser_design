<template>
    <div class="body-not">
        <div class="notfound">
            <el-row class="big">
                <b>无法访问该网站</b>
            </el-row>
            <el-row class="big">
                <b class="eng">DON'T HAVE ACCESS TO WEB SITES</b>
            </el-row>
            <div class="big">
                <el-row>
                    <span>HI!真不巧，没有找到该网页。</span>
                </el-row>
                <el-row>
                    <span>试试修改网址重新搜索，或者点击下方按钮返回首页吧。</span>
                </el-row>
            </div>
            <el-row>
                <el-button @click="handleBack">返回首页</el-button>
            </el-row>
        </div>
    </div>

</template>

<script setup>
import { useRouter } from 'vue-router';
import {  useMainDataStore } from '../stores'
const router = useRouter()
const store = useMainDataStore()
const handleBack = () => {
    if (localStorage.getItem('token')) return router.push('/home')
    router.push('/loginMain')
}
</script>

<style lang="less" scoped>
.body-not{
    width: 100%;
    height: 99.2vh;
    background-image: url('../assets/img/404.jpg');
    background-size: 100% 100%;
    overflow: hidden;
    color: #fff;
    .notfound {
    margin-top: 20vh;

    .big {
        margin-bottom: 2vw;
    }

    .el-row {
        margin-left: 10vw;

        b {
            font-size: 5vw;
        }

        .eng {
            font-size: 1.9vw;
        }


        span {
            font-size: 1vw;
        }

        .el-button {
            font-size: 1vw;
            height: 100px;
            width: 10vw;
            border-radius: 5vw;
        }
    }
}
}

</style>