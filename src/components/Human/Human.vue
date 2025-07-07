<template>
    <el-card>
        <div class="human" style="height: 85vh;">
            <el-card>
                <div class="header">
                    <div class="add">
                        <el-button type='primary' :icon="CirclePlus" plain @click="add = true">添加员工</el-button>
                    </div>
                    <div class="search">
                        <el-input v-model="store.empName" style="max-width: 600px" placeholder="请输入工号或姓名" clearable
                            class="input-with-select">
                            <template #prepend>
                                <el-select v-model="store.deptId" placeholder="部门" style="width: 115px;"
                                    class="input-with-select">
                                    <el-option v-for="(v, i) in deptList" :label=v :value="i" />
                                </el-select>
                            </template>
                            <template #append>
                                <el-button :icon="Search" @click="search()" />
                            </template>
                        </el-input>
                    </div>
                </div>
            </el-card>
            <div class="main">
                <el-row :gutter="40">
                    <el-col :span="6" v-for="(v, i) in store.showList">
                        <el-card class="empcard">
                            <div class="empImg">
                                <img src="../../assets/img/user.svg" style="fill: #485460;height: 100px;">
                            </div>
                            <div class="userInfo">
                                <p>工号: <span>{{ v.id }}</span></p>
                                <p>姓名：<span>{{ v.empName }}</span></p>
                                <p>部门：<span>{{ deptList[v.deptId - 1] }}</span></p>
                                <p>职位：<span :style="{ color: colorList[v.roleId - 1] }">{{ roleList[v.roleId - 1]
                                        }}</span>
                                </p>
                            </div>
                            <div class="detail" @click="showDetail(v)">查看详情>></div>
                        </el-card>
                    </el-col>

                </el-row>
            </div>
        </div>
    </el-card>
    <el-dialog v-model="add" title="添加员工" width="500" draggable>
        <!-- 姓名 -->
        <p>
            姓名<span style="color: red;">*</span>：
            <el-input type="input" placeholder="请输入添加员工姓名" class="dialog-input" v-model="addForm.empName" />
        </p>

        <!-- 部门与职位（并排显示） -->
        <div class="row-flex">
            <div>
                所属部门<span style="color: red;">*</span>：
                <el-select placeholder="部门" class="dialog-input" v-model="addForm.deptId">
                    <el-option v-for="(v, i) in deptList" :label=v :value="i" />
                </el-select>
            </div>
            <div>
                职位<span style="color: red;">*</span>：
                <el-select placeholder="职位" class="dialog-input" v-model="addForm.roleId">
                    <el-option v-for="(v, i) in roleList" :label=v :value="i" />
                </el-select>
            </div>
        </div>

        <!-- 学历 -->
        <p>
            学历<span style="color: red;">*</span>：
            <el-select placeholder="学历" class="dialog-input" v-model="addForm.eduBac">
                <el-option v-for="(v, i) in eduBacList" :label=v :value="i" />
            </el-select>
        </p>

        <!-- 邮箱 -->
        <p>
            邮箱：
            <el-input type="input" placeholder="请输入添加员工邮箱" class="dialog-input" v-model="addForm.email" />
        </p>

        <!-- 电话 -->
        <p>
            电话：
            <el-input type="input" placeholder="请输入添加员工电话" class="dialog-input" v-model="addForm.phone" />
        </p>

        <template #footer>
            <div class="dialog-footer">
                <el-button @click="add = false">取消</el-button>
                <el-button type="primary" @click="addOption">确认</el-button>
            </div>
        </template>
    </el-dialog>
    <el-dialog v-model="detail" :title="`员工详情 - ${currentEmployee.empName || ''}`" width="600" draggable>
        <!-- 查看模式 -->
        <div v-if="!isEditing">
            <el-descriptions :column="1" border>
                <el-descriptions-item label="工号">{{ currentEmployee.id }}</el-descriptions-item>
                <el-descriptions-item label="姓名">{{ currentEmployee.empName }}</el-descriptions-item>
                <el-descriptions-item label="部门">{{ deptList[currentEmployee.deptId - 1] }}</el-descriptions-item>
                <el-descriptions-item label="职位">
                    <span :style="{ color: colorList[currentEmployee.roleId - 1] }">
                        {{ roleList[currentEmployee.roleId - 1] }}
                    </span>
                </el-descriptions-item>
                <el-descriptions-item label="学历">{{ eduBacList[currentEmployee.eduBac] || '暂无' }}</el-descriptions-item>
                <el-descriptions-item label="邮箱">{{ currentEmployee.email || '暂无' }}</el-descriptions-item>
                <el-descriptions-item label="电话">{{ currentEmployee.phone || '暂无' }}</el-descriptions-item>
                <el-descriptions-item label="入职日期">{{currentEmployee.createTime[0]+'-'+currentEmployee.createTime[1]+'-'+currentEmployee.createTime[2] +' '+currentEmployee.createTime[3]+': '+currentEmployee.createTime[4]+':'+currentEmployee.createTime[5]
                    ||
                    '暂无' }}</el-descriptions-item>
            </el-descriptions>
        </div>

        <!-- 编辑模式 -->
        <el-form v-else :model="editForm" label-width="100px">
            <el-form-item label="工号">
                <el-input v-model="editForm.id" disabled />
            </el-form-item>

            <el-form-item label="姓名" required>
                <el-input v-model="editForm.empName" />
            </el-form-item>

            <el-form-item label="部门" required>
                <el-select v-model="editForm.deptId" placeholder="选择部门">
                    <el-option v-for="(v, i) in deptList" :key="i" :label="v" :value="i" />
                </el-select>
            </el-form-item>

            <el-form-item label="职位" required>
                <el-select v-model="editForm.roleId" placeholder="选择职位">
                    <el-option v-for="(v, i) in roleList" :key="i" :label="v" :value="i + 1" />
                </el-select>
            </el-form-item>

            <el-form-item label="学历" required>
                <el-select v-model="editForm.eduBac" placeholder="选择学历">
                    <el-option v-for="(v, i) in eduBacList" :key="i" :label="v" :value="i" />
                </el-select>
            </el-form-item>

            <el-form-item label="邮箱">
                <el-input v-model="editForm.email" />
            </el-form-item>

            <el-form-item label="电话">
                <el-input v-model="editForm.phone" />
            </el-form-item>

            <el-form-item label="入职日期">
                <el-date-picker v-model="editForm.createTime" type="date" placeholder="选择日期" disabled />
            </el-form-item>
        </el-form>

        <template #footer>
            <div class="dialog-footer">
                <!-- 查看模式下的按钮 -->
                <template v-if="!isEditing">
                    <el-button type="danger" @click="deleteEmployee">删除</el-button>
                    <el-button type="primary" @click="startEditing">修改</el-button>
                </template>

                <!-- 编辑模式下的按钮 -->
                <template v-else>
                    <el-button @click="cancelEditing">取消</el-button>
                    <el-button type="primary" @click="saveEmployee">保存</el-button>
                </template>
            </div>
        </template>
    </el-dialog>
</template>

<script setup>
import { onBeforeMount, onBeforeUnmount, onMounted, reactive, ref } from "vue";
import { Search, CirclePlus } from '@element-plus/icons-vue'
import { useHumanDataStore, useMainDataStore, useRegDataStore } from "../../stores";
import { ElMessage, ElMessageBox } from "element-plus";
import api from '../../untils/api/human'
onMounted(() => {
    api.getAll().then(({ data }) => {
        store.empList = data
        store.showList = store.empList

    }).catch((err) => {
        ElMessage({
            message: err,
            type: 'warning',
        })
    })
})
onBeforeUnmount(()=>{
    store.deptId=null;
    store.empName=''
})
const addForm = reactive({
    empName: '',
    deptId: null,
    roleId: null,
    eduBac: '',
    email: '',
    phone: '',
    status: '在职'
})
const dstore = useMainDataStore()
const rstore = useRegDataStore()
const store = useHumanDataStore()

const deptList = [...dstore.deptList, '全部']
const roleList = rstore.roleList
const colorList = store.colorList
const eduBacList = store.eduBacList
const search = store.search
const add = ref(false)
const detail = ref(false)
const isEditing = ref(false) // 控制编辑状态

const addOption = () => {
    Object.assign(addForm, { ...addForm, eduBac: eduBacList[addForm.eduBac], deptId: addForm.deptId + 1, roleId: addForm.roleId + 1 })
    console.log(addForm)
    api.addEmp(addForm).then((data) => {
        ElMessage.success('添加员工成功')
        api.getAll().then(({ data }) => {
            store.empList = data
            store.showList = store.empList

        })
    })

    add.value = false
}
const currentEmployee = ref({})
const editForm = reactive({
    id: '',
    empName: '',
    deptId: null,
    roleId: null,
    eduBac: null,
    email: '',
    phone: '',
    createTime: ''
})

const showDetail = (employee) => {
    currentEmployee.value = { ...employee }
    isEditing.value = false // 初始为查看模式
    detail.value = true
}
const startEditing = () => {
    // 填充编辑表单
    Object.assign(editForm, {
        id: currentEmployee.value.id,
        empName: currentEmployee.value.empName,
        deptId: currentEmployee.value.deptId - 1, // 适配选择器索引
        roleId: currentEmployee.value.roleId,
        eduBac: eduBacList[currentEmployee.value.eduBac],
        email: currentEmployee.value.email || '',
        phone: currentEmployee.value.phone || '',
        createTime: currentEmployee.value.createTime || ''
    })
    isEditing.value = true // 切换到编辑模式
}

const deleteEmployee = () => {


    ElMessageBox.confirm(
        `确定要删除员工 ${currentEmployee.value.empName} 吗？此操作不可恢复。`,
        '警告',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    ).then(() => {
        api.upEmp({ id: currentEmployee.value.id, status: '离职' }).then((data) => {
            console.log(data)
            ElMessage.success('员工删除成功')
            api.getAll().then(({ data }) => {
                store.empList = data
                store.showList = store.empList
                
            })
        })
        detail.value = false
    }).catch(() => {
    })
}

const cancelEditing = () => {
    isEditing.value = false // 返回查看模式
}

// 保存修改
const saveEmployee = () => {
    // 表单验证
    console.log(editForm)
    if (!editForm.empName || !editForm.deptId == null || !editForm.roleId || !editForm.eduBac) {

        ElMessage.warning('请填写必填项')
        return
    }

    // 构建要保存的数据
    const updatedEmployee = {
        ...currentEmployee.value,
        empName: editForm.empName,
        deptId: editForm.deptId + 1, // 转换回存储格式
        roleId: editForm.roleId,
        eduBac: editForm.eduBac,
        email: editForm.email,
        phone: editForm.phone
    }


    // 更新当前显示的员工数据
    const index = store.showList.findIndex(emp => emp.id === updatedEmployee.id)
    if (index !== -1) {
        store.showList[index] = updatedEmployee
    }

    // 更新当前显示的员工信息
    currentEmployee.value = updatedEmployee
    console.log(currentEmployee.value)
    api.upEmp(currentEmployee.value).then((data) => {
        console.log(data)
        api.getAll().then(({ data }) => {
            store.empList = data
            store.showList = store.empList
        })
        ElMessage.success('员工信息更新成功')
    })

    isEditing.value = false // 返回查看模式
}

</script>

<style lang="less" scoped>
.human {
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
        max-height: 80vh;
        overflow-y: auto;
        scrollbar-width: none;
        /* Firefox */
        -ms-overflow-style: none;

        /* IE 10+ */
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