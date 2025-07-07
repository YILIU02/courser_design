<template>
    <div>
        <el-card class="ecard">
            <div class="search" style="padding: 0.1em;">
                <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;">绩效信息查询</p>
                <div class="choice" style=" display: flex;justify-content: space-between; padding-right: 2em;">
                    <div style="display: inline-block;">
                        <el-date-picker v-model="date" type="year" value-format="YYYY" placeholder="选择时间"
                            style="width: 20em;" />
                    </div>
                    <div style="display: inline-block;">
                        <el-input style="max-width: 600px;width: 30em;" placeholder="请输入工号" clearable
                            class="input-with-select" v-model="empId">
                            <template #append>
                                <el-button :icon="Search" @click="search()" />
                            </template>
                        </el-input>
                    </div>
                </div>

            </div>
        </el-card>
        <el-card class="ecard" style="max-height: 36em;overflow: auto;">
            <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;position: relative;">绩效信息<span
                    style="position: absolute; right: 1em;"><el-button type='primary'
                        @click="loadAll">下载历年绩效表</el-button></span></p>
            <div class=" history">
                <el-table :data="historyList" border style="width: 100%">
                    <el-table-column prop="year" label="年份" />
                    <el-table-column prop="empId" label="员工ID" />
                    <el-table-column prop="empName" label="姓名" />
                    <el-table-column prop="totalScore" label="总绩效分" />
                    <el-table-column label="操作" width="180" fixed="right" align="center">
                        <template #default="{ row }">
                            <div class="action-buttons">
                                <el-button type="success" @click="toshow(row.empId, row.year)">
                                    查看详情
                                </el-button>

                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </el-card>
    </div>
    <el-dialog v-model="show">
        <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;">详情信息</p>
        <el-table :data="newList" border style="width: 100%">
            <el-table-column prop="year" label="年份" />
            <el-table-column prop="empId" label="员工ID" />
            <el-table-column prop="empName" label="姓名" />
         <el-table-column prop="deptScore" label="业务分数（30%）" />
            <el-table-column prop="projScore" label="技能分数（50%）" />
            <el-table-column prop="attdScore" label="考勤分数(20%)" />
            <el-table-column prop="totalScore" label="总绩效分" />
        </el-table>
    </el-dialog>
</template>

<script setup>
import { Search, CirclePlus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus';
import { onMounted, ref } from "vue";
import { useMainDataStore } from "../../stores";
import api from '../../untils/api/performance'
onMounted(async () => {
    historyList.value = []
    yearList.value = await api.getYear().then(({ data }) => data)
    historyList.value = await api.getAll({ last: '0', year: '2025' }).then(({ data }) => data)

})
const show = ref(false)
const dstore = useMainDataStore()
const newList = ref([])
const historyList = ref([])
const date = ref(null)
const yearList = ref([])
const empId = ref(null)

const search = async () => {
    historyList.value = []
    const result = ref([])
    if ((/^[+]{0,1}(\d+)$|^[+]{0,1}(\d+\.\d+)$/).test(empId.value) && !date.value) {

        const history = await Promise.all(
            yearList.value.map(async (year) => {
                return await api.getOne({ empId: empId.value, last: '0', year }).then(({ data }) => data[0])
            })
        )
        console.log(history);
        
        result.value = history
        result.value = result.value.sort((b, a) => a.year - b.year)


    } else if (empId.value && !date.value) {

        ElMessage({
            type: 'warning',
            message: '请输入工号'
        })
    } else if (empId.value) {
        result.value = await api.getOne({ empId: empId.value, last: '0', year: date.value }).then(({ data }) => data)
        result.value = result.value.sort((b, a) => a.year - b.year)
    }
    else {
        result.value = await api.getAll({ last: '0', year: date.value }).then(({ data }) => data)
        result.value = result.value.sort((b, a) => a.year - b.year)
    }

    historyList.value=result.value
}

const toshow = async (empId, year) => {
    newList.value = await api.getOne({ empId, last: '0', year }).then(({ data }) => {
        show.value = true
        data.forEach((v) => {
            v.attdScore = v.attdScore || '0'
            v.deptScore = v.deptScore || '0'
            v.projScore = v.projScore || '0'
        })
        return data
    }).catch((err) => {
        ElMessage({
            type: 'warning',
            message: err
        })
    })
}
const loadAll = async () => {

   const url='http://127.0.0.1:8082/ind/report'
//    const url ="https://111.230.242.244:8081/ind/report"
    const link = document.createElement('a');
    link.href = url
    link.download = 'fileName'; // 使用动态文件名
    document.body.appendChild(link);
    link.click();
    URL.revokeObjectURL(url);
    document.body.removeChild(link);

}
</script>

<style lang="less" scoped>
.ecard {
    margin-top: 1em;
    margin-left: 1em;
    width: 98%;
}
</style>
