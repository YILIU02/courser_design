<template>
    <div class="main">
        <el-card class="ecard">
            <div class="search" style="padding: 0.1em;">
                <div>
                    <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;">个人考勤信息查询</p>
                    <el-date-picker v-model="date" type="date" value-format="YYYY-MM-DD" placeholder="选择时间" @change="submit" />
                </div>

            </div>
        </el-card>
        <el-card style="position: relative;" class="ecard">
            <p style="display: inline-block;margin: 0;margin-bottom: 1em;font-size: 1.4em;">今日考勤</p>
            <div style="display: inline-block;position: absolute;top:2em;right: 3em;"><el-button type='primary'
                    :disabled="checkIn" @click="clickCheckIn">{{ !checkIn ? '签到' : '签到成功' }}</el-button>
                <el-button type='primary' :disabled="checkOut" @click="clickCheckOut">{{ !checkOut ? '签退' : '签退成功'
                }}</el-button>
            </div>
            <div class="personInfo">
                <el-descriptions :column="2" border>
                    <el-descriptions-item label="考勤状态">{{ store.pmsg.status || '暂无' }}</el-descriptions-item>
                    <el-descriptions-item label="备注">{{ store.pmsg.remark|| '暂无' }}</el-descriptions-item>
                    <el-descriptions-item label="签到时间">{{store.pmsg.checkIn? store.pmsg.checkIn.map((v, i) => {
                        v = v < 10 ? '0' + v : v;
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v;
                        return v
                    }).join('') : '暂无'}}</el-descriptions-item>
                    <el-descriptions-item label="签退时间">{{ store.pmsg.checkOut?store.pmsg.checkOut.map((v, i) => {
                        v = v < 10 ? '0' + v : v;
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v;
                        return v
                    }).join(''):'暂无'}}</el-descriptions-item>
                </el-descriptions>
            </div>
        </el-card>
        <el-card class="ecard">
            <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;position: relative;">历史考勤信息<span
                    style="position: absolute; right: 1em;"></span></p>
            <div class=" history">
                <el-table :data="store.pAttendList" border style="width: 100%">
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
import { onMounted, onUnmounted, ref } from 'vue'
import { useAttendDataStore, useMainDataStore } from '../../stores'
import api from '../../untils/api/attend'
import hapi from '../../untils/api/human'
onMounted(async () => {
    api.getpHistory(dstore.uesrInfo.empId).then(({data}) => {
        data.forEach(async(v)  => {
            v.empName=dstore.uesrInfo.empName
           v.checkIn=v.checkIn?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                        return v
                    }).join(''),
            v.checkOut=v.checkOut?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                        return v
                    }).join('') || '暂无',
             v.attDate=v.attDate?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        return v
                    }).join('-') 
        });
        store.pAttendList = data;
        api.getToday(dstore.uesrInfo.empId).then(({data}) => {
            Object.assign(store.pmsg,data)
            checkIn.value = store.pmsg.checkIn ? true : false
            checkOut.value = store.pmsg.checkOut ? true : false
        })
        
    })


})
onUnmounted(()=>{
    store.pmsg={}
})
const checkIn = ref(false)
const checkOut = ref(false)
const date = ref(null)
const store = useAttendDataStore()
const dstore = useMainDataStore()
const clickCheckIn = () => {
    api.checkIn(dstore.uesrInfo.empId).then((data) => {
        api.getpHistory(dstore.uesrInfo.empId).then(({ data }) => {
                    data.forEach(async(v)  => {
            v.empName=dstore.uesrInfo.empName
           v.checkIn=v.checkIn?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                        return v
                    }).join(''),
            v.checkOut=v.checkOut?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                        return v
                    }).join('') || '暂无',
             v.attDate=v.attDate?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        return v
                    }).join('-') 
        });
            store.pAttendList = data;
            api.getToday(dstore.uesrInfo.empId).then(({data}) => {
                Object.assign(store.pmsg,data)
                
                checkIn.value = true
                ElMessage({
                    message: '签到成功',
                    type: 'success',
                })
            })
        })


    })
}
const clickCheckOut=()=>{
     api.checkOut(dstore.uesrInfo.empId).then((data) => {
        api.getpHistory(dstore.uesrInfo.empId).then(({ data }) => {
                    data.forEach(async(v)  => {
            v.empName=dstore.uesrInfo.empName
           v.checkIn=v.checkIn?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                        return v
                    }).join(''),
            v.checkOut=v.checkOut?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                        return v
                    }).join('') || '暂无',
             v.attDate=v.attDate?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        return v
                    }).join('-') 
        });
            store.pAttendList = data;
            api.getToday(dstore.uesrInfo.empId).then(({data}) => {
                 Object.assign(store.pmsg,data)
                console.log(data);
                checkOut.value = true
                ElMessage({
                    message: '签到成功',
                    type: 'success',
                })
            })
        })


    })
}
const submit=()=>{
      api.getpHistory(dstore.uesrInfo.empId,date.value).then(({ data }) => {
          data.forEach(async(v)  => {
            v.checkIn=v.checkIn?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                        return v
                    }).join(''),
            v.checkOut=v.checkOut?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                        return v
                    }).join('') || '暂无',
             v.attDate=v.attDate?.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        return v}).join('-')
                         v.empName=dstore.uesrInfo.empName
        });
       
            store.pAttendList = data;
          
        })
    
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
        max-height: 17em;
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