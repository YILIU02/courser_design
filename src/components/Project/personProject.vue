<template>
    <el-card style="min-height: 89vh;">
        <div class="project">
            <el-card>
                <div class="header">
                    <div class="search">
                        <el-input style="max-width: 600px" placeholder="请输入编号/项目名/负责人" clearable
                            v-model="store.pproName" class="input-with-select">
                            <template #prepend>
                                <el-select v-model="store.type" placeholder="类型" style="width: 115px;"
                                    class="input-with-select">
                                    <el-option v-for="(v, i) in store.typeList" :label="v" :value="i" />
                                </el-select>
                            </template>
                            <template #append>
                                <el-button :icon="Search" @click="tsearch" />
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
                        :style="{ 'background': store.colorList[v.status == '进行中' ? 3 : v.status == '已暂停' ? 2 : 1] }"
                        @click="showDetail(v)">
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
                            <span>{{v.startDate?.map(v => {
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

    <el-dialog v-model="detail" :title="`项目详情 - ${currentProject.projectName || ''}`" width="600" draggable>
        <!-- 查看模式 -->
        <div v-if="!isEditing">
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
        </div>

        <!-- 编辑模式 -->
        <el-form v-else :model="editForm" label-width="100px">
            <el-form-item label="编号">
                <el-input v-model="editForm.id" disabled />
            </el-form-item>

            <el-form-item label="项目名" required>
                <el-input v-model="editForm.projectName" />
            </el-form-item>

            <el-form-item label="项目描述">
                <el-input v-model="editForm.projectDesc" />
            </el-form-item>


            <el-form-item label="项目状态">
                <el-select placeholder="项目状态" class="dialog-input" v-model="editForm.status">
                    <el-option v-for="(v, i) in store.activeList" :label=v :value="v" />
                </el-select>
            </el-form-item>
            <el-form-item label="结束日期" required>
                <el-date-picker v-model="editForm.endDate" type="date" value-format="YYYY-MM-DD" placeholder="选择时间" />
            </el-form-item>

        </el-form>

        <template #footer>
            <div class="dialog-footer">
                <!-- 查看模式下的按钮 -->
                <template v-if="!isEditing && !currentProject.responsibility">
                    <el-button type="danger" @click="deleteEmployee">暂停</el-button>
                    <el-button type="primary" @click="startEditing">修改项目信息</el-button>
                    <el-button type='primary' @click="editEmp">修改项目成员信息</el-button>
                </template>

                <!-- 编辑模式下的按钮 -->
                <template v-else>
                    <el-button @click="cancelEditing">取消</el-button>
                    <el-button type="primary" @click="saveEmployee">保存</el-button>
                </template>
            </div>
        </template>
    </el-dialog>
    <el-dialog v-model="editE" title="修改项目成员" width="600" draggable>
        <p>增加项目成员</p>
        <el-select placeholder="项目成员" class="dialog-input" v-model="addId"
            @change="updateEmp(currentProject.id, addId)">
            <el-option v-for="(v, i) in hstore.empList" :label="v.empName" :value="v.id">
            </el-option>
        </el-select>
        <p>删除项目成员信息</p>
        <el-table :data="currentProject.empList" style="width: 100%">
            <el-table-column prop="id" label="工号" width="120" />
            <el-table-column prop="empName" label="姓名" width="120" />
            <el-table-column prop="deptId" label="部门" width="120" />
            <el-table-column fixed="right" label="操作" min-width="120">
                <template #default="scope">
                    <el-button link type="danger" size="small"
                        @click="deleteEmp(scope.row, currentProject.id)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <template #footer>
            <div class="dialog-footer">
                <el-button type="primary" @click="editE = false">退出</el-button>

            </div>
        </template>
    </el-dialog>
</template>

<script setup>
import { reactive, ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { useHumanDataStore, useMainDataStore, usePojectDataStore } from "../../stores";
import { Search, CirclePlus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from "element-plus";
import api from '../../untils/api/project'
import hapi from '../../untils/api/human'
onMounted(async () => {
    api.getByempID(dstore.uesrInfo.empId).then(async ({ data }) => {
        
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
        store.pproList = projectsWithManNames;
        store.pshowList = projectsWithManNames;

            

    }).catch((err) => ElMessage({
        type: 'warning',
        message: err
    }))
})
onBeforeUnmount(() => {
    store.pproList = []
    store.pshowList = []

    store.pproName = ''

})
const detail = ref()
const store = usePojectDataStore()
const dstore = useMainDataStore()
const hstore = useHumanDataStore()

const currentPage = ref(1)        // 当前页码
const pageSize = ref(8)          // 每页显示数量
const total = ref(0)              // 总记录数

// 部门列表
const deptList = [...dstore.deptList, '全部']
const typeList = ref(['负责', '全部'])
watch(() => store.pshowList, (newList) => {
    total.value = newList.length

}, { immediate: true })



// 计算当前页要显示的数据
const currentPageProjects = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return store.pshowList.slice(start, end)
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
const tsearch = store.tsearch
const isEditing = ref(false)
const currentProject = ref({})
const editForm = reactive(
    {
        projId: '',
        projectName: '',
        projectDesc: '',
        endDate: '',
        status: '',
        manName: '',
        projectDesc: ''
    }
)


const showDetail =async (pro) => {
    
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
                        id: emp.data.id,
                        deptId: deptList[emp.data.deptId - 1]
                    }
                })
                .catch(() => "获取失败") // 添加错误处理
        );

    // 4. 等待所有员工请求完成
    const empNames = await Promise.all(empFetchPromises);



    // 5. 更新当前项目数据
    currentProject.value = {
        responsibility:pro.responsibility,
        ...project,
        empList: empNames.slice(1),
        manName,
        count: empNames.length,
        endDate: project.endDate ? project.endDate : []
    };


    console.log(currentProject.value);

    // 6. 打开详情对话框
    detail.value = true;
    isEditing.value = false;
}
const startEditing = () => {
     // 填充编辑表单
    Object.assign(editForm, {
        id: currentProject.value.id,
        projectName: currentProject.value.projectName,
        startDate: currentProject.value.startDate, // 适配选择器索引
        status: currentProject.value.status,
        deptId: currentProject.value.deptId - 1,
        projMan: currentProject.value.projMan,
        count: currentProject.value.count,
        manName: currentProject.value.manName,
        projectDesc: currentProject.value.projectDesc,
        endDate: currentProject.value.endDate.map(v => {
                                return v = v < 10 ? '0' + v : v
                            }).join('-')

    })
    console.log(editForm);
    
    isEditing.value = true // 切换到编辑模式
}

const deleteEmployee = () => {
     ElMessageBox.confirm(
        `确定要暂停项目 ${currentProject.value.projectName} 吗？此操作不可恢复。`,
        '警告',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    ).then(() => {
        api.editPro({ projId: currentProject.value.id, status: '已暂停' }).then((data) => {
            api.getByempID(dstore.uesrInfo.empId).then(async ({ data }) => {
        
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
        store.pproList = projectsWithManNames;
        store.pshowList = projectsWithManNames;

            

    }).catch((err) => ElMessage({
        type: 'warning',
        message: err
    }))
            ElMessage.success('项目暂停成功')
            detail.value = false
        })
            .catch((err) => {
                ElMessage.warning(err)
            })
    }).catch(() => {
    })
}

const cancelEditing = () => {
    isEditing.value = false // 返回查看模式
}

// 保存修改
const saveEmployee = () => {
   // 表单验证

    if (!editForm.projectName || !editForm.deptId == null || !editForm.projMan) {
        ElMessage.warning('请填写必填项')
        return
    }
    hstore.empList.map(val => {
        if (val.id == editForm.manName) {
            editForm.manName = val.empName
        }
    })
    editForm.projMan = (/^[+]{0,1}(\d+)$|^[+]{0,1}(\d+\.\d+)$/).test(editForm.manName) ? editForm.manName : editForm.projMan
    console.log(editForm);
    api.editPro({
        projId: editForm.id,
        projectName: editForm.projectName,
        projectDesc: editForm.projectDesc,
        endDate: editForm.endDate,
        status: editForm.status
    }).then((data) => {
        console.log(data);
        // 构建要保存的数据
        const updatedProject = {
            ...currentProject.value,
            id: editForm.id,
            projectName: editForm.projectName,
            startDate: editForm.startDate, // 适配选择器索引
            status: editForm.status,
            deptId: editForm.deptId + 1,
            projMan: editForm.projMan,
            count: editForm.count,
            manName: editForm.manName,
            projectDesc: editForm.projectDesc,
            endDate: editForm.endDate.split('-')
        }



        // 更新当前显示的项目数据
        const index = store.pshowList.findIndex(v => v.id === updatedProject.id)
        if (index !== -1) {
            store.pshowList[index] = updatedProject
        }

        // 更新当前显示的员工信息
        currentProject.value = updatedProject

        ElMessage.success('项目信息更新成功')
        isEditing.value = false // 返回查看模式
    })
}
const editE = ref(false)
const editEmp = () => {
    editE.value = true
}
const deleteEmp = async (row, pro) => {
    await api.deleteEmp(pro, row.id).then(async (data) => {
        currentProject.value.empList = currentProject.value.empList.filter(v => v.id !== row.id);

        // 更新参与人数
        currentProject.value.count = currentProject.value.empList.length;

        ElMessage.success("员工已从项目中移除");
    })
}
const updateEmp = (pro, emp) => {

    
    api.addEmp(pro, emp).then(async (data) => {
    
        
        const response = await hapi.getById(emp);
        const newEmp = {
            id: emp,
            empName: response?.data?.empName || "新成员",
            deptId:deptList[response?.data?.deptId-1]
            
        };

        // 更新当前项目的员工列表
        currentProject.value.empList = [...currentProject.value.empList, newEmp];
        console.log(   currentProject.value.empList );
        
        // 更新参与人数
        currentProject.value.count = currentProject.value.empList.length;

        // 清空选择框

        addId=null
        ElMessage.success("成员添加成功");

    })
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