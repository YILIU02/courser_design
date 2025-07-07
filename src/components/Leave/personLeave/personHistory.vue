<template>

    <el-card class="ecard">
        <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;position: relative;">个人请假信息<span
                style="position: absolute; right: 1em;">
                <el-select placeholder="请假状态" style="width: 115px;" class="input-with-select" v-model="store.status" @change="change">
                    <el-option v-for="(v, i) in activeList" :label=v :value="i" />
                </el-select></span></p>

        <div class=" history">
            <el-table :data="store.showList" border style="width: 100%">
                <el-table-column prop="id" label="请假编号" />
                <el-table-column prop="empName" label="员工姓名" />
                <el-table-column prop="leaveType" label="请假类型" />
                <el-table-column prop="startDate" label="开始时间" />
                <el-table-column prop="days" label="请假天数" />
                <el-table-column prop="createTime" label="提交申请时间" />
                <el-table-column prop="approver" label="审批人" />
                <el-table-column prop="approveDate" label="审批日期" />
                <el-table-column prop="status" label="状态" />
            </el-table>
        </div>
    </el-card>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useLeaveDataStore, useMainDataStore } from "../../../stores";
import api from '../../../untils/api/leave'
import hapi from '../../../untils/api/human'
onMounted(() => {
    api.selectOne({ empId: dstore.uesrInfo.empId }).then(async ({ data }) => {
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
            })
        );



        store.leaveList = projectsWithManNames;
        store.showList = projectsWithManNames


    })
})
const dstore = useMainDataStore()
const store = useLeaveDataStore()
const activeList = ['待审批', '已拒绝', '已批准','全部']
const change=()=>{
    
    store.showList=store.leaveList
    if(store.status!=null&&store.status!=3){
        store.showList=computed(() => store.leaveList.filter(val => val.status==activeList[store.status])).value
    }
    
}
</script>

<style lang="less" scoped>
.ecard{
    margin: 1em;
    min-height:41em ;
    max-height: 41em;
    overflow-y:auto ;
}</style>