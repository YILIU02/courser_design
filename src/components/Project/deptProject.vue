<template>
    <el-card style="min-height: 89vh;">
        <div class="project">
            <el-card>
                <div class="header">
                    <div class="add">
                        <el-button type='primary' :icon="CirclePlus" plain @click="handleAdd">添加项目</el-button>
                    </div>
                    <div class="search">
                        <el-input style="max-width: 600px" placeholder="请输入编号/项目名/负责人" clearable v-model="store.dproName"
                            class="input-with-select">
                            <template #append>
                                <el-button :icon="Search" @click="search" />
                            </template>
                        </el-input>
                    </div>
                </div>
            </el-card>
            <div class="main" style="padding-top: 1em;">
                <el-row :gutter="60">
                    <!-- 表头行 -->
                    <div class="ecard header-row" style="border-bottom: 1px solid #cacaca;">
                        <div class="field-container">
                            <span style="color: #cacaca;">项目编号</span>
                        </div>
                        <div class="field-container">
                            <span style="color: #cacaca;">项目名</span>
                        </div>
                        <div class="field-container">
                            <span style="color: #cacaca;">负责人</span>
                        </div>
                        <div class="field-container">
                            <span style="color: #cacaca;">部门</span>
                        </div>
                        <div class="field-container">
                            <span style="color: #cacaca;">参与人数</span>
                        </div>
                        <div class="field-container">
                            <span style="color: #cacaca;">开始时间</span>
                        </div>
                        <div class="field-container">
                            <span style="color: #cacaca;">状态</span>
                        </div>
                    </div>

                    <!-- 内容行 - 使用当前页数据 -->
                    <div class="ecard content-row" v-for="(v, i) in currentPageProjects" :key="v.id"
                        :style="{ 'background': store.colorList[v.status == '进行中' ? 3 : v.status == '已暂停' ? 2 : 1] }" @click="showDetail(v)">
                          <div class="field-container">
                            <span>{{ v.id }}</span>
                        </div>
                        <div class="field-container">
                            <span>{{ v.projectName }}</span>
                        </div>
                        <div class="field-container">
                            <span>{{ v.manName }}</span>
                        </div>
                        <div class="field-container">
                            <span>{{ deptList[v.deptId - 1] }}</span>
                        </div>
                        <div class="field-container">
                            <span>{{ v.count }}</span>
                        </div>
                        <div class="field-container">
                            <span>{{v.startDate.map(v => {
                                return v = v < 10 ? '0' + v : v
                            }).join('-')}}</span>
                        </div>
                        <div class="field-container">
                            <span>{{ v.status }}</span>
                        </div>
                    </div>
                </el-row>

                <!-- 分页器 -->
                <div class="pagination-container" style="text-align: center; margin-top: 20px;">
                    <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
                        :current-page="currentPage" :page-size="pageSize" layout="total, prev, pager, next, jumper"
                        :total="total">
                    </el-pagination>
                </div>
            </div>
        </div>
    </el-card>
    <el-dialog v-model="add" title="添加项目" width="500" draggable>
    <!-- 使用el-form包裹添加表单 -->
    <el-form ref="addFormRef" :model="addForm" :rules="addFormRules">
      <!-- 项目名 -->
      <el-form-item label="项目名" prop="projectName" required>
        <el-input 
          type="input" 
          placeholder="请输入添加项目名" 
          class="dialog-input" 
          v-model="addForm.projectName" 
        />
      </el-form-item>
      
      <!-- 项目描述 -->
      <el-form-item label="项目描述" prop="projectDesc">
        <el-input 
          type="input" 
          placeholder="请输入项目描述" 
          class="dialog-input" 
          v-model="addForm.projectDesc" 
        />
      </el-form-item>
      
      <!-- 负责人 -->
      <el-form-item label="负责人" prop="projMan" required>
        <el-select 
          placeholder="部门员工" 
          class="dialog-input" 
          v-model="addForm.projMan"
        >
          <el-option 
            v-for="(v, i) in hstore.deptempList" 
            :label="v.empName" 
            :value="v.id" 
          />
        </el-select>
      </el-form-item>
    </el-form>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="add = false">取消</el-button>
        <el-button type="primary" @click="submitAddForm">确认</el-button>
      </div>
    </template>
    </el-dialog>
     <el-dialog v-model="detail" :title="`项目详情 - ${currentProject.projectName || ''}`" width="600" draggable>
  
 <el-descriptions :column="1" border>
                <el-descriptions-item label="编号">{{ currentProject.id }}</el-descriptions-item>
                <el-descriptions-item label="项目名">{{ currentProject.projectName }}</el-descriptions-item>
                <el-descriptions-item label="部门">{{ deptList[currentProject.deptId - 1] }}</el-descriptions-item>
                <el-descriptions-item label="负责人">{{ currentProject.manName }}
                </el-descriptions-item>
                <el-descriptions-item label="开始时间">{{ currentProject.startDate.join('-') || '暂无'
                    }}</el-descriptions-item>
                <el-descriptions-item label="参与人员">{{currentProject.empList.map(v => v.empName).toString() ||
                    '暂无'}}</el-descriptions-item>
                <el-descriptions-item label="参与人数">{{ currentProject.count || '暂无' }}</el-descriptions-item>
                <el-descriptions-item label="项目状态">{{ currentProject.status || '暂无' }}</el-descriptions-item>
                <el-descriptions-item label="项目描述">{{ currentProject.projectDesc || '暂无' }}</el-descriptions-item>
                <el-descriptions-item label="项目结束时间">{{ currentProject.endDate.map(v => {
                                return v = v < 10 ? '0' + v : v
                            }).join('-') || '暂无'
                    }}</el-descriptions-item>
            </el-descriptions>

        
   
    </el-dialog>
</template>

<script setup>
import { reactive, ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { useHumanDataStore, useMainDataStore, usePojectDataStore } from "../../stores";
import { Search, CirclePlus } from '@element-plus/icons-vue'
import { ElMessage,ElMessageBox } from "element-plus";
import hapi from '../../untils/api/human'
import api from '../../untils/api/project'
onMounted(()=>{

    
    api.getBydId(dstore.uesrInfo.deptId).then(async({data})=>{
        const projectsWithManNames = await Promise.all(
            data.map(async (v) => {
                // 获取负责人姓名
                const response = await hapi.getById(v.projMan);
                // 确保响应数据存在
                const manName = response?.data?.empName || "未知负责人";
                return { ...v, manName };
            })
        );
        // 更新存储
        store.dproList = projectsWithManNames;
        store.dShowList = projectsWithManNames;
    })
})

onBeforeUnmount(()=>{
    store.dproList=[]
    store.dShowList=[]
    store.dproName=''

}) 
const addId = ref('')
const detail=ref()
const store = usePojectDataStore()
const dstore = useMainDataStore()
const hstore=useHumanDataStore()
const add = ref(false)
const addForm=ref({})
const addFormRules = reactive({
  projectName: [
    { required: true, message: '项目名不能为空', trigger: 'blur' }
  ],
  projMan: [
    { required: true, message: '负责人不能为空', trigger: 'change' }
  ]
})
const addFormRef = ref(null)

// 修改添加方法
const submitAddForm = () => {
  addFormRef.value.validate(valid => {
    if (valid) {
      // 校验通过，执行添加操作
      addOption()
    } else {
      // 校验失败
      ElMessage.warning('请填写必填项')
      return false
    }
  })
}
const addOption = () => {
    api.addPro({ ...addForm.value, deptId: dstore.uesrInfo.deptId }).then((d) => {
 api.getBydId(dstore.uesrInfo.deptId).then(async({data})=>{
        const projectsWithManNames = await Promise.all(
            data.map(async (v) => {
                // 获取负责人姓名
                const response = await hapi.getById(v.projMan);
                // 确保响应数据存在
                const manName = response?.data?.empName || "未知负责人";
                return { ...v, manName };
            })
        );
        // 更新存储
        store.dproList = projectsWithManNames;
        store.dShowList = projectsWithManNames;
    })
    })
    ElMessage.success('添加项目成功')
    add.value = false
}
const handleAdd = () => {
    add.value = true

}
const currentPage = ref(1)        // 当前页码
const pageSize = ref(8)          // 每页显示数量
const total = ref(0)              // 总记录数

// 部门列表
const deptList = [...dstore.deptList, '全部']

watch(() => store.dShowList, (newList) => {
    total.value = newList.length
}, { immediate: true })



// 计算当前页要显示的数据
const currentPageProjects = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return store.dShowList.slice(start, end)
})

// 分页事件处理
const handleSizeChange = (newSize) => {
    pageSize.value = newSize
    // 调整每页数量后，确保当前页有数据
    if ((currentPage.value - 1) * newSize >= total.value) {
        currentPage.value = Math.ceil(total.value / newSize) || 1
    }
}

const handleCurrentChange = (newPage) => {
    currentPage.value = newPage
}
//下面搜索替换
const search = store.dsearch

const currentProject = ref({})

const showDetail = async (pro) => {
    // 1. 获取项目基础数据
    const { data: project } = await api.getById(pro.id);
    // 2. 检查并处理可能的空值
    if (!project || !project.empList) {
        console.error("项目数据不完整", project);
        currentProject.value = {
            ...pro,
            empList: []
        };
        detail.value = true;
        return;
    }
    const manName = await hapi.getById(pro.projMan).then(({ data }) => data.empName);
    // 3. 并行获取所有员工姓名（添加空值检查）
    const empFetchPromises = project.empList
        .filter(v => !v.leaveDate)
        .map(v =>
            hapi.getById(v.empId)
                .then(emp => {
                    // 添加空值检查

                    return {
                        empName: emp?.data?.empName || "未知员工",
                        id: emp.data.id
                    }
                })
                .catch(() => "获取失败") // 添加错误处理
        );

    // 4. 等待所有员工请求完成
    const empNames = await Promise.all(empFetchPromises);


    // 5. 更新当前项目数据
    currentProject.value = {
        ...project,
        empList: empNames.slice(1),
        manName,
        count: empNames.length,
        endDate:project.endDate?project.endDate:[]
    };


    // 6. 打开详情对话框
    detail.value = true;

}

</script>

<style lang="less" scoped>
.project {
    position: relative;

    .header {
        min-height: 3vh;

        .add {
            width: 40px;
            height: 30px;
            position: absolute;
            right: 5vw;
            top: 2vh;

            .icon {
                color: #636e72;
            }
        }

        .search {
            width: 30vw;
            min-height: 30px;
            position: absolute;
            left: 2vw;
            top: 2vh;
        }
    }

    .main {
       height: 70vh;
        overflow-y: auto;
        scrollbar-width: none;
        -ms-overflow-style: none;
    

        .header-row,
        .content-row {
            margin-bottom: 1em;
            margin-left: 3em;
            width: 90%;
            height: 2em;
            border-radius: 8px;
            position: relative;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: grid;
            grid-template-columns: 150px 250px 150px 150px 150px 180px 150px;
            align-items: center;
            padding: 0.3em;
            text-align: center;
        }

        .field-container {
            padding: 0 5px;
            box-sizing: border-box;
        }

        .header-row {
            background-color: transparent;

            span {
                color: #cacaca;
                font-weight: normal;
            }
        }

        .content-row {
            &:hover {
                transform: scale(1.02);
                z-index: 10;
            }

            span {
                color: #fff;
                font-weight: 600;
            }
        }

        .pagination-container {
            padding-bottom: 20px;
            position: absolute;
            right: 3em;
         bottom: 0.5em;
            z-index: 1;
        }
    }
}

.dialog-input {
    width: 100%;
    margin-top: 8px;
}

/* 并排布局 */
.row-flex {
    display: flex;
    gap: 16px;
    /* 元素间距 */
    margin-bottom: 15px;

    >div {
        flex: 1;
        /* 等分宽度 */
    }
}

/* 调整标签对齐 */
p>span[style*="color: red"] {
    margin-right: 4px;
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

/* 按钮样式 */

.el-form-item {
    margin-bottom: 18px;
}

.el-select,
.el-input {
    width: 100%;
}

/* 按钮样式 */
.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
</style>