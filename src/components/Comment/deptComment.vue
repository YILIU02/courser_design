<template>
    <div>
        <el-card class="ecard" style="min-height: 9em;">
            <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;">部门成员查询</p>
            <el-select v-model="empId" filterable placeholder="选择您的成员" style="width: 440px" @change="change">
                <el-option v-for="item in HumanList" :key="item.id" :label="item.empName" :value="item.id" />
            </el-select>
        </el-card>
        <el-card class="ecard" style="min-height: 35em;max-height: 30em;overflow-y:auto ;">
            <p style="margin: 0;margin-bottom: 1em;font-size: 1.4em;">部门 成员</p>
            <el-row :gutter="40">
                 <el-col :span="6" v-for="(v, i) in showList" >
                    <el-card class="empcard">
                        <div class="empImg">
                            <img src="../../assets/img/user.svg" style="fill: #485460;height: 100px;">
                        </div>
                        <div class="userInfo">
                            <p>工号: <span>{{ v.id }}</span></p>
                            <p>姓名：<span>{{ v.empName }}</span></p>
                            <p>部门：<span>{{ dstore.deptList[v.deptId - 1] }}</span></p>
                            <p>职位：<span :style="{ color:colorList[v.roleId - 1] }">{{ roleList[v.roleId - 1]
                            }}</span>
                            </p>
                        </div>
                        <div class="detail" @click="showCom(v)">前往打分>></div>
                    </el-card>
                </el-col>

            </el-row>
        </el-card>
    </div>
    <el-dialog v-model="comment" title="输入评分" width="400" align-center style="position: relative;height: 10em;">
        <el-form v-model="sorce">
                    <el-input-number 
                v-model="sorce" 
                :min="0" 
                :max="100" 
                :precision="0"
                controls-position="right"
                placeholder="请输入0-100的整数"
                style="width: 100%"
            />
            <el-button type='primary'
                style="margin-top:1em;  position: absolute; right: 1.2em;bottom: 1em;" @click="submit">提交</el-button>
        </el-form>
    </el-dialog>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { computed, onMounted, ref } from "vue";
import { useHumanDataStore, useMainDataStore, useRegDataStore } from "../../stores";
import hapi from '../../untils/api/human'
import api from '../../untils/api/comment'
onMounted(async () => {
   HumanList.value= await hapi.getDeptHuman({deptId:dstore.uesrInfo.deptId}).then(({data}) =>data )

   showList.value=HumanList.value
   
})
const hstore = useHumanDataStore()
const colorList=hstore.colorList
const rstore=useRegDataStore()
const roleList=rstore.roleList
const HumanList=ref([])
const showList=ref([])
const dstore = useMainDataStore()
const comment = ref(false)
const sorce = ref(null)
const empId=ref('')
const showCom = (v) => {
    empId.value=v.id
    comment.value = true
}
const change=async()=>{
    if(empId.value){
          showList.value= [await hapi.getById(empId.value).then(({data}) =>data)]
    }
    
}
const submit=()=>{
     if (sorce.value === null || sorce.value === undefined) {
        ElMessage.error('分数不能为空')
        return
    }
    
    // 这里添加实际提交逻辑
    api.business(empId.value,sorce.value).then(()=>{
        sorce.value=null
        comment.value=false
        ElMessage({
            type:'success',
            message:'提交成功'
        })
    }).catch((err)=>{
        ElMessage({
            type:'warning',
            message:err
        })
    })
}
</script>

<style lang="less" scoped>
.ecard {
    margin: 1em 0 0 1em;

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
</style>