import { createRouter, createWebHistory } from 'vue-router'
import { useMainDataStore } from '../stores'
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
    lable: '项目管理',
    icon: 'File',
    children: [
      {
        path: '/allProject',
        name: 'allproject',
        lable: '项目总览',
        icon: 'FolderOpened',
        url: 'Project/Project.vue'
      },
      {
        path: '/deptProject',
        name: 'deptproject',
        lable: '部门项目',
        icon: 'FolderOpened',
        url: 'Project/deptProject.vue',

      },
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
    name: 'Project',
    lable: '项目管理',
    icon: 'File',
    children: [

      {
        path: '/deptProject',
        name: 'deptproject',
        lable: '部门项目',
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
    lable: '项目管理',
    icon: 'File',
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
const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('../components/Login/Login.vue'),// 当前登录页组件
    children: [
      {
        path: '/registerContent',
        name: 'RegisterContent',
        component: () => import('../components/Register/RegisterContent.vue')
      },
      {
        path: '/registerSub',
        name: 'RegisterSub',
        component: () => import('../components/Register/RegisterSub.vue')
      },
      {
        path: '/loginmain',
        name: 'LoginMain',
        component: () => import('../components/Login/LoginMain.vue')
      }
    ]
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../components/Home.vue'),// 当前登录页组件
    children: [
        {
    path: '/Frist',
    name: 'frist',
    component: () => import('../components/First.vue')

  },
      {
        path: '/human',
        name: 'Human',
        children: [
          {
            path: '/allHuman',
            name: 'allhuman',
            component: () => import('../components/Human/Human.vue')
          },
          {
            path: '/deptHuman',
            name: 'depthuman',
            component: () => import('../components/Human/deptHuman.vue')
          },
        ]
      },
      {
        path: '/attend',
        name: 'Attend',
        children: [
          {
            path: '/allAttend',
            name: 'allattend',
            component: () => import('../components/Attendance/Attendance.vue')
          },
          {
            path: '/deptAttend',
            name: 'deptattend',
            component: () => import('../components/Attendance/deptAttend.vue')
          },
          {
            path: '/personAttend',
            name: 'personattend',
            component: () => import('../components/Attendance/personAttend.vue')
          },
        ]
      },
      {
        path: '/performance',
        name: 'Performance',
        children: [
          {
            path: '/allPerformance',
            name: 'allperformance',
            component: () => import('../components/Performance/Performance.vue')
          },
          {
            path: '/deptPerformance',
            name: 'deptperformance',
            component: () => import('../components/Performance/deptPerformance.vue')
          },
          {
            path: '/personPerformance',
            name: 'personperformance',
            component: () => import('../components/Performance/personPerformance.vue')
          },
        ]
      },
      {
        path: '/project',
        name: 'Project',
        children: [
          {
            path: '/allProject',
            name: 'allproject',
            component: () => import('../components/Project/Project.vue')
          },
          {
            path: '/deptProject',
            name: 'deptproject',
            component: () => import('../components/Project/deptProject.vue')
          },
          {
            path: '/personProject',
            name: 'personproject',
            component: () => import('../components/Project/personProject.vue')
          },
        ]
      },
      {
        path: '/comment',
        name: 'Comment',
        children: [
          {
            path: '/teamComment',
            name: 'teamcomment',
            component: () => import('../components/Comment/teamComment.vue')
          },
          {
            path: '/deptComment',
            name: 'deptcomment',
            component: () => import('../components/Comment/deptComment.vue')
          },

        ]
      },
      {
        path: '/leave',
        name: 'Leave',
        children: [
          {
            path: '/submitLeave',
            name: 'submitLeave',
            component: () => import('../components/Leave/Leave.vue'),
            children: [
              {
                path: '/submit',
                name: 'submit',
                component: () => import('../components/Leave/personLeave/Submit.vue')
              }, {
                path: '/personhistory',
                name: 'personhistory',
                component: () => import('../components/Leave/personLeave/personHistory.vue')
              }
            ]
          },
          {
            path: '/leaveReview',
            name: 'leavereview',
            component: () => import('../components/Leave/leaveReview.vue')
          }
        ]
      }
    ]
  },

  {
    path: '/404',
    name: '404',
    component: () => import('../components/notFound.vue')
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router