import { defineStore } from "pinia";
import { reactive, ref, computed, watch } from 'vue';

// 设置主首页数据库
export const useMainDataStore = defineStore('allData', () => {
    const token = ref('')//保存token
    const menuList = ref([]
    );
    const topMenu = [

        {
            path: '/human',
            name: 'Human',
            label: '员工管理',
            icon: 'Avatar',
            children: [
                {
                    path: '/allHuman',
                    name: 'allhuman',
                    label: '员工总览',
                    icon: 'User',
                    url: 'Human/Human.vue'
                },
                {
                    path: 'deptHuman',
                    name: 'depthuman',
                    label: '部门员工',
                    icon: 'User',
                    url: 'Human/deptHuman.vue'
                },

            ]
        },
        {
            path: '/project',
            name: 'Project',
            label: '项目管理',
            icon: 'Files',
            children: [
                {
                    path: '/allProject',
                    name: 'allproject',
                    label: '项目总览',
                    icon: 'FolderOpened',
                    url: 'Project/Project.vue'
                },
                {
                    path: '/deptProject',
                    name: 'deptproject',
                    label: '部门项目',
                    icon: 'FolderOpened',
                    url: 'Project/deptProject.vue',

                },
                {
                    path: '/personProject',
                    name: 'personproject',
                    label: '个人项目',
                    icon: 'FolderOpened',
                    url: 'Project/personProject.vue',

                },
            ]
        },
        {
            path: '/attend',
            name: 'Attend',
            label: '考勤管理',
            icon: 'DocumentChecked',
            children: [
                {
                    path: '/allAttend',
                    name: 'allattend',
                    label: '考勤总览',
                    icon: 'FolderChecked',
                    url: 'Attendance/Attendance.vue'
                },
                {
                    path: '/deptAttend',
                    name: 'deptattend',
                    label: '部门考勤',
                    icon: 'FolderChecked',
                    url: 'Attendance/deptAttend.vue'

                },
                {
                    path: '/personAttend',
                    name: 'personattend',
                    label: '个人考勤',
                    icon: 'FolderChecked',
                    url: 'Attendance/personAttend.vue'
                },
            ]
        },
        {
            path: '/performance',
            name: 'Performance',
            label: '绩效管理',
            icon: 'DataAnalysis',
            children: [
                {
                    path: '/allPerformance',
                    name: 'allperformance',
                    label: '绩效总览',
                    icon: 'DataLine',
                    url: 'Performance/Performance.vue'
                },
                {
                    path: '/deptPerformance',
                    name: 'deptperformance',
                    label: '部门绩效',
                    icon: 'DataLine',
                    url: 'Performance/deptPerformance.vue'
                },
                {
                    path: '/personPerformance',
                    name: 'personperformance',
                    label: '个人绩效',
                    icon: 'DataLine',
                    url: 'Performance/personPerformance.vue'
                },
            ]
        },
        {
            path: '/comment',
            name: 'Comment',
            label: '评价管理',
            icon: 'EditPen',
            children: [
                {
                    path: '/teamComment',
                    name: 'teamcomment',
                    label: '项目负责人评价',
                    icon: 'Edit',
                    url: 'Comment/teamComment.vue'
                },
                {
                    path: '/deptComment',
                    name: 'deptcomment',
                    label: '部长评价',
                    icon: 'Edit',
                    url: 'Comment/deptComment.vue'
                },

            ]
        },
        {
            path: '/leave',
            name: 'Leave',
            label: '请假',
            icon: 'DocumentCopy',
            children: [
                {
                    path: '/submitLeave',
                    name: 'submitLeave',
                    label: '请假申请',
                    icon: 'Tickets',
                    url: 'Leave/Leave.vue',

                    children: [
                        {
                            path: '/submit',
                            name: 'submit',
                            label: '请假申请',
                            url: 'Leave/personLeave/Submit.vue'
                        }, {
                            path: '/personhistory',
                            name: 'personhistory',
                            label: '请假信息',
                            url: 'Leave/personLeave/personHistory.vue'
                        }
                    ]
                },
                {
                    path: '/leaveReview',
                    name: 'leavereview',
                    label: '申请审批',
                    icon: 'Checked',
                    url: 'Leave/leaveReview.vue'
                }
            ]
        }
    ]
    const minMenu = [

        {
            path: '/human',
            name: 'Human',
            label: '员工管理',
            icon: 'Avatar',
            children: [
                {
                    path: 'deptHuman',
                    name: 'depthuman',
                    label: '部门员工',
                    icon: 'User',
                    url: 'Human/deptHuman.vue'
                },

            ]
        },
        {
            path: '/project',
            name: 'project',
            label: '项目管理',
            icon: 'Files',
            children: [
                {
                    path: '/deptProject',
                    name: 'deptproject',
                    label: '部门项目',
                    icon: 'FolderOpened',
                    url: 'Project/deptProject.vue',
                },

            ]
        },
        {
            path: '/attend',
            name: 'Attend',
            label: '考勤总览',
            icon: 'DocumentChecked',
            children: [

                {
                    path: '/deptAttend',
                    name: 'deptattend',
                    label: '部门考勤',
                    icon: 'FolderChecked',
                    url: 'Attendance/deptAttend.vue'

                },

            ]
        },
        {
            path: '/performance',
            name: 'Performance',
            label: '绩效管理',
            icon: 'DataAnalysis',
            children: [

                {
                    path: '/deptPerformance',
                    name: 'deptperformance',
                    label: '部门绩效',
                    icon: 'DataLine',
                    url: 'Performance/deptPerformance.vue'
                },

            ]
        },
        {
            path: '/comment',
            name: 'Comment',
            label: '评价管理',
            icon: 'EditPen',
            children: [

                {
                    path: '/deptComment',
                    name: 'deptcomment',
                    label: '部长评价',
                    icon: 'Edit',
                    url: 'Comment/deptComment.vue'
                },

            ]
        },
        {
            path: '/leave',
            name: 'Leave',
            label: '请假',
            icon: 'DocumentCopy',
            children: [
                {
                    path: '/leaveReview',
                    name: 'leavereview',
                    label: '申请审批',
                    icon: 'Checked',
                    url: 'Leave/leaveReview.vue'
                }
            ]
        }
    ]
    const nomMenu = [
        {
            path: '/project',
            name: 'Project',
            label: '项目管理',
            icon: 'Files',
            children: [
                {
                    path: '/personProject',
                    name: 'personproject',
                    label: '个人项目',
                    icon: 'FolderOpened',
                    url: 'Project/personProject.vue',
                    url: 'Project/personProject.vue'
                },
            ]
        },
        {
            path: '/attend',
            name: 'Attend',
            label: '考勤管理',
            icon: 'DocumentChecked',
            children: [
                {
                    path: '/personAttend',
                    name: 'personattend',
                    label: '个人考勤',
                    icon: 'FolderChecked',
                    url: 'Attendance/personAttend.vue'
                },
            ]
        },
        {
            path: '/performance',
            name: 'Performance',
            label: '绩效管理',
            icon: 'DataAnalysis',
            children: [
                {
                    path: '/personPerformance',
                    name: 'personperformance',
                    label: '个人绩效',
                    icon: 'DataLine',
                    url: 'Performance/personPerformance.vue'
                },
            ]
        },
        {
            path: '/comment',
            name: 'Comment',
            label: '评价管理',
            icon: 'EditPen',
            children: [
                {
                    path: '/teamComment',
                    name: 'teamcomment',
                    label: '项目负责人评价',
                    icon: 'Edit',
                    url: 'Comment/teamComment.vue'
                }
            ]
        },
        {
            path: '/leave',
            name: 'Leave',
            label: '请假',
            icon: 'DocumentCopy',
            children: [
                {
                    path: '/submitLeave',
                    name: 'submitLeave',
                    label: '请假申请',
                    icon: 'Tickets',
                    url: 'Leave/Leave.vue',

                    children: [
                        {
                            path: '/submit',
                            name: 'submit',
                            label: '请假申请',
                            url: 'Leave/personLeave/Submit.vue'
                        }, {
                            path: '/personhistory',
                            name: 'personhistory',
                            label: '请假信息',
                            url: 'Leave/personLeave/personHistory.vue'
                        }
                    ]
                },
            ]
        }
    ]
    const roleMenus = [topMenu,    // 管理员
        minMenu,    // 部长
        nomMenu]
    // 普通员工


    const deptList = [
        '研发部',
        '市场部',
        '财务部',
        '运营部',
    ]
    const uesrInfo = reactive({})
    const updateMenuList = (roleId) => {
        menuList.value = roleMenus[roleId]
    }
    return {//暴露数据
        token,
        menuList,
        deptList, uesrInfo, updateMenuList
    }
}, {
    persist: true//持久化设置
})

// 设置登录页数据库
export const useLoginDataStore = defineStore('Login', () => {

    const loginForm = reactive({
        username: '',
        password: '',
    });

    const updateloginForm = () => {
        Object.assign(loginForm, {
            username: '',
            password: '',
        })
    }
    return {

        loginForm, updateloginForm
    }
}, {
    persist: true
})
export const useRegDataStore = defineStore('register', () => {
    const SubmitForm = reactive({
        empId: '',
        empName: '',
        deptId: null,
    })
    
    const updateSubmit = () => {
        Object.assign(SubmitForm, {
            empId: '',
            empName: '',
            deptId: null,
        })
    }
    const options = [

        {
            value: 1,
            label: '研发部',
        },
        {
            value: 2,
            label: '市场部',
        }, {
            value: 3,
            label: '财务部',
        }, {
            value: 4,
            label: '运营部',
        },
    ]


    const roleList = ['管理员', '部长', '员工']

    const RegForm = reactive({
        username: '',
        password: '',
        empId: '',
        roleId:null
    });
    const updateRegForm = () => {
        Object.assign(RegForm, {
            username: '',
            password: '',
            empId: '',
            roleId: null
        })
    
  
    }

    return {
        SubmitForm, options, updateSubmit,   roleList, RegForm, updateRegForm
    }
}, {
    persist: true
})
//设置员工库
export const useHumanDataStore = defineStore('human', () => {
    const empList = ref([])
    const colorList = ref(['#ba5140', '#474787', '#4b7b6b'])
    const eduBacList = ref(["本科", "硕士", "博士"])
    const showList = ref(computed(() => empList.value.map(v => v)).value)
    const empName = ref('')
    const deptId = ref(4)

    const search = () => {
        let result = empList.value
        let result1 = empList.value
        if (deptId.value != 4) {
            result = computed(() => empList.value.filter(val => deptId.value + 1 == val.deptId)).value
        }
        else {
            result = computed(() => empList.value.map(v => v)).value

        }
        if (empName.value) {
            const searchTerm = empName.value.trim().toLowerCase();
            result1= result1.filter(val =>
                val.empName.toLowerCase().includes(searchTerm) || val.id.toString().includes(searchTerm)
            );
        }
        showList.value = [...result,...result1
        ]

    }
    const deptEmpName = ref('')
    const deptempList = ref([])
    const deptShowList = ref(computed(() => deptempList.value.map(v => v)).value)
    const dsearch = () => {
        let result = deptempList.value
        if (deptEmpName.value) {
            const searchTerm = deptEmpName.value.trim().toLowerCase();
            result = result.filter(val =>
                val.empName.toLowerCase().includes(searchTerm) || val.id.toString().includes(searchTerm)
            );
        }
        else {
            result = computed(() => deptempList.value.map(v => v)).value
        }
        deptShowList.value = result

    }

    return {//暴露数据
        empList, colorList, showList, empName, deptId, search, eduBacList, deptempList, deptShowList, dsearch, deptEmpName
    }
}, {
    persist: true//持久化设置
})
export const usePojectDataStore = defineStore('poject', () => {
    const colorList = ref(['linear-gradient(135deg, #81fbb8, #28c76f)', 'linear-gradient(135deg,#ed213a,#93291e)', 'linear-gradient(135deg,#bdc3c7,#2c3e50)', 'linear-gradient(135deg,#17ead9,#6078ea)'])
    const proList = ref([])
    const showList = ref(computed(() => proList.value.map(v => v)).value)
    const dproList=ref([])
    const dShowList=ref([])
    const pproList=ref([])
    const pshowList=ref([])
    const dproName=ref('')
    const pproName=ref('')
    const proName = ref('')
    const deptId = ref(4)
    const search = () => {
        let result = proList.value
        if (deptId.value != 4) {
            result = computed(() => proList.value.filter(val => deptId.value + 1 == val.deptId)).value
        }
        else {
            result = computed(() => proList.value.map(v => v)).value

        }
        if (proName.value) {
            const searchTerm = proName.value.trim().toLowerCase();
            result = result.filter(val =>
                val.projectName.toLowerCase().includes(searchTerm) || val.manName.toLowerCase().includes(searchTerm) || val.id.toString().includes(searchTerm)
            );
        }
        showList.value = result
        console.log(showList.value)
    }
     const dsearch = () => {
        console.log(dproName.value);
        let result = dproList.value
        if (dproName.value) {
            const searchTerm = dproName.value.trim().toLowerCase();
            result = result.filter(val =>
                val.projectName.toLowerCase().includes(searchTerm) || val.manName.toLowerCase().includes(searchTerm) || val.id.toString().includes(searchTerm)
            );
        }
        dShowList.value = result
    }
    const activeList = ['进行中','已暂停','已完成']
    const typeList = ['负责', '参与','全部']
    const type = ref(null)
    const tsearch = () => {
        console.log( pproList.value,type.value);
        
        let result = computed(() => pproList.value.map(v => v)).value
        if (type.value!=null&&type.value<typeList.length-1) {
            result = computed(() => pproList.value.filter(val => val.responsibility==type.value)).value
            console.log(result);
            
        }
        if (pproName.value) {
            const searchTerm = pproName.value.trim().toLowerCase();
            result = result.filter(val =>
                val.projectName.toLowerCase().includes(searchTerm) || val.manName.toLowerCase().includes(searchTerm) || val.id.toString().includes(searchTerm)
            );
        }
        pshowList.value = result
    }
    return {
        colorList, proList, showList,dShowList,dproList,pproList,pshowList,dproName,pproName, deptId, proName, activeList, search, type, typeList, tsearch,dsearch

    }
}, {
    persist: true//持久化设置
})

export const useAttendDataStore=defineStore('attend',()=>{
const pAttendList=ref([])
const pmsg=reactive({
    status:'',
    remark:'',
    checkIn:'',
    checkOut:''
})
const dAttendList=ref([])
const allAttendList=ref([])
const allTheMList=ref([])
return {
    pAttendList,pmsg,dAttendList,allAttendList,allTheMList
}
}, {
    persist: true//持久化设置
})
export const useLeaveDataStore=defineStore('leave',()=>{
    const leaveList=ref([])
    const showList=ref([])
    const status=ref('')
    const leavereList=ref([])
    const rshowList=ref([])
    const rstatus=ref('')
    const rName=ref('')
    return {
        leaveList,showList,status,leavereList,rstatus,rshowList,rName
    }
},{
    persist: true//持久化设置
})