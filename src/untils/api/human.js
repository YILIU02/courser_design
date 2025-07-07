import request from '../request'
export default {
    getAll() {
        return request({
            method: 'get',
            url: '/emp/list'
        })
    },
    addEmp(data) {
        return request({
            method: 'post',
            url: '/emp/add',
            data
        })
    },
    upEmp(data){
        return request({
            method:'post',
            url:'/emp/alter',
            data
        })
    },
    getNowInfo(){
        return request({
            method:'get',
            url:'/user/getUserInfo'
        })
    },

    //部门
    getDeptHuman(data){
        return request({
            method:'get',
            url:'/emp/getByDeptId',
            params:data
        })
    },
    getById(data){
        return request({
            method:'get',
            url:'/emp/getById',
            params:{
                empId:data
            }
        })
    },
    getBoss(deptId){
        return request({
            method:'get',
            url:'/emp/getBoss',
            params:{
                deptId
            }
        })
    }

}