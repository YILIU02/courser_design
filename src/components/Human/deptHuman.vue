<template>
    <el-card>
        <div class="human" style="height: 85vh;">
            <el-card class="main">
                <div class="header">
                    <div class="search">
                        <el-input v-model="store.deptEmpName" style="max-width: 600px" placeholder="请输入工号或姓名" clearable
                            class="input-with-select">
                            <template #append>
                                <el-button :icon="Search" @click="dsearch()" />
                            </template>
                        </el-input>
                    </div>
                </div>
            </el-card>
            <div class="main">
                <el-row :gutter="40">
                    <el-col :span="6" v-for="(v, i) in store.deptShowList">
                        <el-card class="empcard">
                            <div class="empImg">
                                <img src="../../assets/img/user.svg" style="fill: #485460;height: 100px;">
                            </div>
                            <div class="userInfo">
                                <p>工号: <span>{{ v.id }}</span></p>
                                <p>姓名：<span>{{ v.empName }}</span></p>
                                <p>部门：<span>{{ deptList[v.deptId - 1] }}</span></p>
                                <p>职位：<span :style="{ color: colorList[v.roleId - 1] }">{{ roleList[v.roleId - 1]
                                }}</span>
                                </p>
                            </div>
                            <div class="detail" @click="showDetail(v)">查看详情>></div>
                        </el-card>
                    </el-col>

                </el-row>
            </div>
        </div>
    </el-card>
    <el-dialog v-model="detail" :title="`员工详情 - ${currentEmployee.empName || ''}`" width="600" draggable>
        <el-descriptions :column="1" border>
            <el-descriptions-item label="工号">{{ currentEmployee.id }}</el-descriptions-item>
            <el-descriptions-item label="姓名">{{ currentEmployee.empName }}</el-descriptions-item>
            <el-descriptions-item label="部门">{{ deptList[currentEmployee.deptId - 1] }}</el-descriptions-item>
            <el-descriptions-item label="职位">
                <span :style="{ color: colorList[currentEmployee.roleId - 1] }">
                    {{ roleList[currentEmployee.roleId - 1] }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="学历">{{ currentEmployee.eduBac || '暂无' }}</el-descriptions-item>
            <el-descriptions-item label="邮箱">{{ currentEmployee.email || '暂无' }}</el-descriptions-item>
            <el-descriptions-item label="电话">{{ currentEmployee.phone || '暂无' }}</el-descriptions-item>
            <el-descriptions-item
                label="入职日期">{{ currentEmployee.createTime[0] + '-' + currentEmployee.createTime[1] + '-' + currentEmployee.createTime[2]
                    + ' ' + currentEmployee.createTime[3] + ': ' + currentEmployee.createTime[4] + ':' + currentEmployee.createTime[5]
                    ||
                '暂无' }}</el-descriptions-item>
        </el-descriptions>
    </el-dialog>
</template>

<script setup>
import { useHumanDataStore, useMainDataStore, useRegDataStore } from "../../stores"
import { Search, CirclePlus } from '@element-plus/icons-vue'
import { onBeforeUnmount, onMounted, ref } from "vue"
import api from '../../untils/api/human'
const dstore = useMainDataStore()
const rstore = useRegDataStore()
const store = useHumanDataStore()
onMounted(() => {
   
    api.getDeptHuman({deptId:dstore.uesrInfo.deptId}).then(({data}) => {
       store.deptempList=data;
       store.deptShowList=data

    })

})


const deptList = [...dstore.deptList, '全部']
const roleList = rstore.roleList
const colorList = store.colorList
const eduBacList = store.eduBacList
const dsearch = store.dsearch
const currentEmployee = ref({})
const detail = ref(false)
const showDetail = (employee) => {
    currentEmployee.value = { ...employee }
    detail.value = true
}
</script>

<style lang="less" scoped>
.human {
    position: relative;


    .main {
        max-height: 42.1em;
        overflow-y: auto;
    }

    .header {
        min-height: 3vh;



        .search {
            width: 30vw;
            min-height: 30px;
            position: absolute;
            left: 2vw;
            top: 2vh;

        }
    }

    .main {
        .el-row {
            margin-bottom: 20px;
        }

        .el-row:last-child {
            margin-bottom: 0;
        }

        .el-col {
            border-radius: 0.4em;

            .empcard {
                position: relative;
                margin-top: 1em;
                min-height: 10.2em;

                .empImg,
                .userInfo {
                    vertical-align: middle;
                    display: inline-block;
                    font-size: 1em;
                }

                .userInfo {
                    p {
                        margin: 0.2em;

                        span {
                            font-weight: 600;
                        }
                    }

                    margin-left: 0.2em;
                }
            }

            .detail {
                position: absolute;
                right: 1.2em;
                bottom: 0.4em;
                color: #1e90ff;
            }
        }

    }

}
</style>