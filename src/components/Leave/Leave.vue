<template>
    <div>
        <div class="menu">
            <el-menu :default-active="activeMenu" class="el-menu-demo" mode="horizontal" >
                <!-- 无子菜单建立 -->
                <el-menu-item v-for="item in leaveList" :index="item.path" :key="item.path" @click="handleMenu(item)">
                    <component :is="item.icon" class="icons"></component>
                    <span>{{ item.label }}</span>
                </el-menu-item>
            </el-menu>
        </div>
        <div class="main">
            <router-view></router-view>
        </div>
    </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
onMounted(() => {
    router.push('/submit')
})
const router = useRouter()
const leaveList = ref([{
    path: '/submit',
    label: '请假申请',
    icon: 'HomeFilled',
},
{ path: '/personhistory',
        label: '请假信息',
        icon: 'HomeFilled',}
])

const route = useRoute()
const activeMenu = computed(() => route.path)//获取当前展示路由
const handleMenu = (item) => {//建立跳转逻辑
    router.push(item.path)

}

</script>

<style lang="scss" scoped></style>