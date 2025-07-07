<template>
    <div>

        <el-card class="ecard">
            <div class="header">
                <div class="search">
                    <el-input style="max-width: 600px" placeholder="请输入编号/员工姓名" clearable class="input-with-select" v-model="store.rName">
                        <template #prepend>
                            <el-select placeholder="类型" style="width: 115px;" class="input-with-select" v-model="type">
                                <el-option v-for="(v,i) in activeList" :label="v" :value="i"/>
                            </el-select>
                        </template>
                        <template #append>
                            <el-button :icon="Search" @click="search"/>
                        </template>
                    </el-input>
                </div>
            </div>
        </el-card>
        <el-card class="ecard">
            <div class=" history">
                <el-table :data="store.rshowList" border style="width: 100%" height="500">
                    <el-table-column prop="id" label="请假编号" width="100" align="center" />
                    <el-table-column prop="empName" label="员工姓名" width="120" align="center" />
                    <el-table-column prop="leaveType" label="请假类型" width="120" align="center" />
                    <el-table-column prop="startDate" label="开始时间" width="140" align="center" />
                    <el-table-column prop="endDate" label="结束时间" width="140" align="center" />
                    <el-table-column prop="days" label="请假天数" width="100" align="center" />
                    <el-table-column prop="createTime" label="提交申请时间" width="170" align="center" />
                    <el-table-column prop="approver" label="审批人" width="120" align="center" />
                    <el-table-column prop="approveDate" label="审批日期" width="140" align="center" />
                    <el-table-column prop="status" label="状态" width="120" align="center">
                        <template #default="{ row }">
                            <span :class="['status-badge', `status-${row.status}`]">
                                {{ row.status }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="180" fixed="right" align="center">
                        <template #default="{ row }">
                            <div class="action-buttons">
                                <el-button v-if="row.status === '待审批'" type="success" size="small"
                                    @click="approve(row,'已批准')" :icon="CircleCheck">
                                    批准
                                </el-button>
                                <el-button v-if="row.status === '待审批'" type="danger" size="small"
                                    @click="approve(row,'已拒绝')" :icon="CircleClose">
                                    拒绝
                                </el-button>
                                <span v-if="row.status !== '待审批'">
                                    {{ row.status }}
                                </span>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </el-card>
    </div>

</template>

<script setup>
import { Search } from '@element-plus/icons-vue'
import { computed, onMounted, ref } from 'vue'
import { useLeaveDataStore, useMainDataStore } from '../../stores'
import api from '../../untils/api/leave'
import hapi from '../../untils/api/human'

onMounted(() => {
    api.selectDept({ deptId: dstore.uesrInfo.deptId }).then(async ({ data }) => {
        const projectsWithManNames = await Promise.all(
            data.map(async (v) => {
                // 获取负责人姓名
                const response = await hapi.getById(v.approver);
                // 确保响应数据存在
                const approver = response?.data?.empName || "未知负责人";
                return {
                    ...v, approver, startDate: v.startDate.map(v => {
                        return v = v < 10 ? '0' + v : v
                    }).join('-') || '暂无',
                    endDate: v.endDate.map(v => {
                        return v = v < 10 ? '0' + v : v
                    }).join('-') || '暂无',
                    createTime: v.createTime.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                        return v
                    }).join('') || '暂无',
                    approveDate: v.approveDate?.map(v => {
                        return v = v < 10 ? '0' + v : v
                    }).join('-') || '暂无',
                    empName: dstore.uesrInfo.empName,
                };
            }))
        console.log(data);

        store.leavereList = projectsWithManNames
        store.rshowList = projectsWithManNames
    })
})
const type=ref(null)
const activeList = ['待审批', '已拒绝', '已批准','全部']
const store = useLeaveDataStore()
const dstore = useMainDataStore()
const approve=(r,status)=>{
    console.log(r.id,r.empId);
    api.permit({id:r.id,empId:r.empId,status}).then((data)=>{
          api.selectDept({ deptId: dstore.uesrInfo.deptId }).then(async ({ data }) => {
        const projectsWithManNames = await Promise.all(
            data.map(async (v) => {
                // 获取负责人姓名
                const response = await hapi.getById(v.approver);
                // 确保响应数据存在
                const approver = response?.data?.empName || "未知负责人";
                return {
                    ...v, approver, startDate: v.startDate.map(v => {
                        return v = v < 10 ? '0' + v : v
                    }).join('-') || '暂无',
                     endDate: v.endDate.map(v => {
                        return v = v < 10 ? '0' + v : v
                    }).join('-') || '暂无',
                    createTime: v.createTime.map((v, i) => {
                        v = v < 10 ? '0' + v : v
                        v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v
                        return v
                    }).join('') || '暂无',
                    approveDate: v.approveDate?.map(v => {
                        return v = v < 10 ? '0' + v : v
                    }).join('-') || '暂无',
                    empName: dstore.uesrInfo.empName,
                };
            }))

        store.leavereList = projectsWithManNames
        store.rshowList = projectsWithManNames
    })
    })

}
const search=()=>{
    store.rshowList=store.leavereList
     if(type.value!=null&&type.value!=3){
        store.rshowList=computed(() => store.leavereList.filter(val => val.status==activeList[type.value])).value
    }
    if(store.rName){
         const searchTerm = store.rName.trim().toLowerCase();
             store.rshowList = store.leavereList.filter(val =>
                val.empName.toLowerCase().includes(searchTerm) ||  val.id.toString().includes(searchTerm)
            );
    }
}
</script>

<style lang="less" scoped>
.ecard {
    margin: 1em;

    .history {
        min-height: 36.7em;
        max-height: 36.7em;
        overflow: auto;
    }
}
</style>