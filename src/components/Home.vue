<template>
    <!-- 首页 -->
    <!-- 首页左侧设计 -->
    <div class="main_left">
        <!-- 首页左侧头部设计 -->
        <div class="main_left_heard">

            <div class="img">
                <img src="../assets/img/user1.png">
            </div>

            <div class="user_info">
                <p>工号：{{store.uesrInfo.empId}}</p>
                <p>权限：{{ rstore.roleList[store.uesrInfo.roleId-1] }}</p>
                
            </div>
        </div>
        <!-- 首页菜单左侧栏设计 -->
        <div class="main_menu">
            <!-- 无子菜单建立 -->
            <el-menu class="el-menu" background-color="#485460" text-color="#fff" :default-active="activeMenu">
                <el-menu-item v-for="item in notChildren" :index="item.path" :key="item.path" @click="handleMenu(item)">
                    <component :is="item.icon" class="icons"></component>
                    <span>{{ item.label }}</span>
                </el-menu-item>
                <!-- 有子菜单建立 -->
                <el-sub-menu v-for="item in hasChildren" :index="item.path" :key="item.path">
                    <template #title>
                        <component :is="item.icon" class="icons"></component>
                        <span>{{ item.label }}</span>
                    </template>
                    <el-menu-item-group>
                        <el-menu-item v-for="(subItem, subIndex) in item.children" :index="subItem.path"
                            @click="handleMenu(subItem)" :key="subItem.path">
                            <component :is="subItem.icon" class="icons"></component>
                            <span>{{ subItem.label }}</span>
                        </el-menu-item>
                    </el-menu-item-group>
                </el-sub-menu>

            </el-menu>

        </div>
    </div>

    <div class="main_right">
        <div class="main_right_heard">
            <el-menu mode="horizontal" style="max-width: 3em;" background-color="#485460" text-color="#fff"
                class="menu">
                <el-menu-item style="background-color: #fff;color: black;" @click="handOut">退出登录</el-menu-item>
            </el-menu>
        </div>
        <div class="main_content">
            <router-view></router-view>
        </div>
    </div>

</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useMainDataStore, useRegDataStore } from '../stores/index'
import { useRoute, useRouter } from "vue-router";
import api from '../untils/api/human'
onMounted(() => {
    api.getNowInfo().then((data)=>{
        Object.assign(store.uesrInfo,data.data)
           store.updateMenuList(store.uesrInfo.roleId-1)
           router.push('/Frist')
    })
 
})
const rstore=useRegDataStore()
const store = useMainDataStore()
const router = useRouter()
const list = computed(() => store.menuList)//获取菜单-路由列表
const notChildren = computed(() => list.value.filter(item => !item.children))//获取无子菜单列表
const hasChildren = computed(() => list.value.filter(item => item.children))//获取有子菜单列表
const route = useRoute()
const activeMenu = computed(() => route.path)//获取当前展示路由
const handleMenu = (item) => {//建立跳转逻辑
    router.push(item.path)
}
const handOut=()=>{
    localStorage.setItem('token','')
    localStorage.setItem('userInfo','')
    store.token=''
    router.push('/')
}
</script>

<style lang="less" scoped>
.main_left,
.main_right {
    vertical-align: top; //设置顶部对齐
}

.main_left {
    max-height: 100vh;
    display: inline-block;
    min-height: 100vh;
    overflow: auto;
    width: 20vw;
    background: #485460;

    .main_left_heard {
        height: 13vh;


        .img {
            margin-top: 2vh;
            display: inline-block;
            height: 11vh;
            width: 11vh;
            border-radius: 50%;
            background-color: #fff;
            text-align: center;
            margin-left: 2vh;
            margin-right: 2vh;

            img {
                height: 10vh;

            }
        }

        .user_info {
            display: inline-block;
            font-size: 10px;
            font-weight: 600;
            margin: 0.3vw;
            color: #fff;
            p{
                font-size: 1.4em;
            }
        }

        .img,
        .user_info {
            vertical-align: middle;
        }
    }

    .el-submenu__title:hover,
    .el-menu-item:focus,
    .el-menu-item:hover {
        background-color: #45465e
    }

    .main_menu {
        .el-menu {
            align-items: center;
            /* 垂直居中 */
            justify-content: center;
            /* 水平居中 */
            width: 100%;
            background: #485460;

            .icons {
                width: 50px;
                height: 30px;
            }
        }
    }
}

.main_right {

    display: inline-block;
    min-height: 100vh;
    width: 79vw;

    .main_right_heard {
        position: relative;
        background: #485460;
        height: 10vh;
        align-items: center;
        /* 垂直居中 */
        justify-content: center;

        .menu {
            border: none;
            position: absolute;
            right: 3vw;
            top: 0.5vw;

        }


    }


}
</style>