import request from '../request'
export default {
    getAll() {
        return request({
            method: 'get',
            url: '/project/list'
        })
    },
    addPro(data) {
        return request({
            method: 'post',
            url: '/project/add',
            data
        })
    },
    editPro(data) {
        return request({
            method: 'post',
            url: '/project/alter',
            data
        })
    },
    getById(projectId) {
        return request({
            method: 'get',
            url: "/project/getById",
            params: {
                projectId
            }
        })
    },
    deleteEmp(projId,empId){
        return request({
            method:'post',
            url:'/project/delEmp',
            data:{
                projId,
                empId
            }
        })
    },
    addEmp(projId,empId){
        return request({
            method:'post',
            url:'/project/addEmp',
              data:{
                projId,
                empId
            }
        })
    }
    ,
    getBydId(deptId){
        return request({
            method:'get',
            url:'/project/getByDeptId',
            params:{
                deptId
            }
        })
    },
    getByempID(empId){
        return request({
            method:'get',
            url:'/project/getByEmpId',
            params:{
                empId
            }
        })
    }
}