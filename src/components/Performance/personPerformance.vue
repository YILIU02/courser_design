<template>
    <div>
        <el-card class="ecard">
            <div class="search" style="padding: 0.1em;">
                <div>
                    <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;">个人绩效信息查询</p>
                    <el-date-picker v-model="date" type="year" value-format="YYYY" placeholder="选择时间"
                        @change="change" />
                </div>

            </div>
        </el-card>
    </div>
    <div>
        <el-card class="ecard">
            <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;position: relative;">最新绩效信息</p>

            <div class=" history">
                <el-table :data="newList" border style="width: 100%">
                    <el-table-column prop="year" label="年份" />
                    <el-table-column prop="empId" label="员工ID" />
                    <el-table-column prop="empName" label="姓名" />
                    <el-table-column prop="deptScore" label="业务分数" />
                    <el-table-column prop="projScore" label="技能分数" />
                    <el-table-column prop="attdScore" label="考勤分数" />
                    <el-table-column prop="totalScore" label="总绩效分" />
                </el-table>
            </div>
        </el-card>
    </div>
    <div>
        <el-card class="ecard" style="min-height: 24em;max-height: 24em;overflow: auto;">
            <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;position: relative;">绩效信息<span
                    style="position: absolute; right: 1em;"></span></p>
            <div class=" history">
                <el-table :data="historyList" border style="width: 100%">
                    <el-table-column prop="year" label="年份" />
                    <el-table-column prop="empId" label="员工ID" />
                    <el-table-column prop="empName" label="姓名" />
        <el-table-column prop="deptScore" label="业务分数（30%）" />
            <el-table-column prop="projScore" label="技能分数（50%）" />
            <el-table-column prop="attdScore" label="考勤分数(20%)" />
                    <el-table-column prop="totalScore" label="总绩效分" />
                </el-table>
            </div>
        </el-card>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useMainDataStore } from "../../stores";
import api from '../../untils/api/performance'
onMounted(async () => {
    newList.value = await api.getOne({ empId: dstore.uesrInfo.empId, last: '1' }).then(({ data }) => {
        data.forEach((v) => {
            v.attdScore = v.attdScore || '0'
            v.deptScore = v.deptScore || '0'
            v.projScore = v.projScore || '0'
        })
        return data
    })
    yearList.value = await api.getYear().then(({ data }) => data)
    const history = await Promise.all(
        yearList.value.map(async (year) => {
            return await api.getOne({ empId: dstore.uesrInfo.empId, last: '0', year }).then(({ data }) => {
                data.forEach((v) => {
                    v.attdScore = v.attdScore || '0'
                    v.deptScore = v.deptScore || '0'
                    v.projScore = v.projScore || '0'
                })
                return data[0]
            })
        })
    )
    historyList.value = history
      historyList.value=historyList.value.sort((b, a) => a.year - b.year)


})
const dstore = useMainDataStore()
const newList = ref([])
const historyList = ref([])
const date = ref(null)
const yearList = ref([])
const change = async () => {
    historyList.value = await api.getOne({ empId: dstore.uesrInfo.empId, last: '0', year: date.value }).then(({ data }) => {
        data.forEach((v) => {
            v.attdScore = v.attdScore || '0'
            v.deptScore = v.deptScore || '0'
            v.projScore = v.projScore || '0'
        })
        return data
    })
      historyList.value=historyList.value.sort((b, a) => a.year - b.year)

}
</script>

<style lang="less" scoped>
.ecard {
    margin-top: 1em;
    margin-left: 1em;
    width: 98%;
}
</style>
