<template>
    <div class="main">
        <el-card class="ecard">
            <div class="search" style="padding: 0.1em;">
                <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;">考勤信息查询</p>
                <div class="choice" style=" display: flex;justify-content: space-between; padding-right: 2em;">
                    <div style="display: inline-block;">
                        <el-date-picker v-model="date" type="date" value-format="YYYY-MM-DD" placeholder="选择时间"
                            style="width: 20em;" />
                    </div>
                    <div style="display: inline-block;">
                        <el-input style="max-width: 600px;width: 30em;" placeholder="请输入工号或姓名" clearable
                            class="input-with-select" v-model="empName">
                            <template #prepend>
                                <el-select placeholder="部门" style="width: 115px;" class="input-with-select"
                                    v-model="deptId">
                                    <el-option v-for="(v, i) in deptList" :label=v :value="i" :key="i"/>
                                </el-select>
                            </template>
                            <template #append>
                                <el-button :icon="Search" @click="search()" />
                            </template>
                        </el-input>
                    </div>
                </div>

            </div>
        </el-card>
        <el-card class="ecard">
            <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;position: relative;">历史考勤信息<span
                    style="position: absolute; right: 1em;"></span></p>
            <div class=" history">
                <el-table :data="store.allAttendList" border style="width: 100%">
                    <el-table-column prop="attDate" label="考勤日期" width="180" />
                    <el-table-column prop="empName" label="姓名" width="180" />
                    <el-table-column prop="status" label="考勤状态" />
                    <el-table-column prop="checkIn" label="签到时间" />
                    <el-table-column prop="checkOut" label="签退时间" />
                    <el-table-column prop="remark" label="备注" />
                </el-table>
            </div>
        </el-card>

    </div>
</template>

<script setup>
import { Search, CirclePlus, Check } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useAttendDataStore, useMainDataStore } from '../../stores'
import api from '../../untils/api/attend'
import hapi from '../../untils/api/human'
onMounted(async () => {
    api.getHistory().then(({ data }) => {
        data.forEach((v) => {
            v.checkIn = v.checkIn?.map((v, i) => {
                v = v < 10 ? '0' + v : v
                v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                return v
            }).join(''),
                v.checkOut = v.checkOut?.map((v, i) => {
                    v = v < 10 ? '0' + v : v
                    v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                    return v
                }).join('')
            v.attDate = v.attDate.map((v, i) => {
                v = v < 10 ? '0' + v : v
                return v
            }).join('-')
        });
        store.allAttendList = data;
    //      store.allTheMList = store.allAttendList.map((data) => {
    //     const list = ref(data.attDate.split('-'))
    //     let date = new Date()
    //     if (list.value[1] < 10) {
    //         list.value[1] = list.value[1][1]


    //     }
    //     if (list.value[0] == date.getFullYear() && list.value[1] == date.getMonth()+1) {
    //         return data
    //     }
    // }).filter((data)=>data!=null);


    }).catch((err) => ElMessage({
        type: 'warning',
        message: err
    }))
   






})
onBeforeUnmount(() => {
    store.allAttendList = []
    deptId.value = null
    empName.value = null
    date.value = null
})
const store = useAttendDataStore()
const dstore = useMainDataStore()
const empName = ref('')
const empId = ref('')
const deptList = [...dstore.deptList, '全部']
const deptId = ref(null)
const date = ref(null)

const search = () => {
    let dept = deptId.value == 4 ? null : deptId.value + 1
    let empId = (/^[+]{0,1}(\d+)$|^[+]{0,1}(\d+\.\d+)$/).test(empName.value) ? empName.value : null
    empName.value = (/^[+]{0,1}(\d+)$|^[+]{0,1}(\d+\.\d+)$/).test(empName.value) ? null : empName.value;
    api.getHistory(dept, empId, empName.value, date.value).then(({ data }) => {
        data.forEach((v) => {
            v.checkIn = v.checkIn?.map((v, i) => {
                v = v < 10 ? '0' + v : v
                v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                return v
            }).join(''),
                v.checkOut = v.checkOut?.map((v, i) => {
                    v = v < 10 ? '0' + v : v
                    v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                    return v
                }).join('')
            v.attDate = v.attDate.map((v, i) => {
                v = v < 10 ? '0' + v : v
                return v
            }).join('-')
        });
        store.allAttendList = data;

    }).catch((err) => ElMessage({
        type: 'warning',
        message: err
    }))

}
</script>

<style lang="less" scoped>
.main {
    padding: 1em;

    .ecard {
        margin-top: 1em;
        margin-left: 1em;
        width: 98%;
    }

    .history {
        min-height: 28.5em;
        max-height: 28.5em;
        overflow-y: auto;
    }

}

:deep(.el-descriptions__body) {
    background-color: #f9f9f9;
}

:deep(.el-descriptions__label) {
    width: 100px;
    font-weight: bold;
}

:deep(.el-descriptions__content) {
    padding-left: 20px;
}
</style>