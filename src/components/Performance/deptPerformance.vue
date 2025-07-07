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
        <el-card class="ecard" style="min-height: 36em;max-height: 36em;overflow: auto;">
            <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;position: relative;">绩效信息<span
                    style="position: absolute; right: 1em;"><el-button type='primary' @click="loadDept">下载部门绩效表</el-button></span></p>
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
    yearList.value = await api.getYear().then(({ data }) => data)
    historyList.value = await api.getDept({ deptId: dstore.uesrInfo.deptId, last: '0' }).then(({ data }) => data)
    historyList.value = historyList.value.sort((b, a) => a.year - b.year)
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
   const list=ref([])
   if(empId.value){
    list.value=[...empId.value]
}
   else{
   list.value=[]
}
   console.log(list.value,empId.value);
   
   
    if ((/^[+]{0,1}(\d+)$|^[+]{0,1}(\d+\.\d+)$/).test(empId.value) && !date.value&&list.value[0]==dstore.uesrInfo.deptId) {
       
        const history = await Promise.all(
            yearList.value.map(async (year) => {
                return await api.getOne({ empId: empId.value, last: '0', year }).then(({ data }) => data[0])
            })
        )
        historyList.value = history
        historyList.value = historyList.value.sort((b, a) => a.year - b.year)


    } else if (empId.value && !date.value) {

        ElMessage({
            type: 'warning',
            message: '请输入工号'
        })
    } else if (empId.value) {
        historyList.value = await api.getOne({ empId: empId.value, last: '0', year: date.value }).then(({ data }) => data)
        historyList.value = historyList.value.sort((b, a) => a.year - b.year)
    }
    else {

        historyList.value = await api.getDept({ deptId: dstore.uesrInfo.deptId, last: '0', year: date.value }).then(({ data }) => data)
        historyList.value = historyList.value.sort((b, a) => a.year - b.year)
    }


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
const loadDept=()=>{
      const url ="http://111.230.242.244:8081/ind/deptReport"
    //    'http://127.0.0.1:8082/ind/deptReport';
    const params = {
        deptId: dstore.uesrInfo.deptId,
        year: date.value,
        last: '0'
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(response => {
        return response.blob();
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = '部门考勤信息表'+date.value; // 可以使用动态文件名
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    })
}


</script>

<style lang="less" scoped>
.ecard {
    margin-top: 1em;
    margin-left: 1em;
    width: 98%;
}
</style>
