export const navigationItems = [
  { name: 'dashboard', path: '/app/dashboard', label: '工作台', icon: 'DataAnalysis' },
  { name: 'employees', path: '/app/employees', label: '员工管理', icon: 'UserFilled', roles: ['admin', 'manager'] },
  { name: 'projects', path: '/app/projects', label: '项目管理', icon: 'FolderOpened' },
  { name: 'attendance', path: '/app/attendance', label: '考勤管理', icon: 'Calendar' },
  { name: 'performance', path: '/app/performance', label: '绩效管理', icon: 'TrendCharts' },
  { name: 'leaves', path: '/app/leaves', label: '请假管理', icon: 'Tickets' },
]
