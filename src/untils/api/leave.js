import request from '../request'

export default {
    submit(data){
        return request({
            method:'post',
            url:'/leaveApp/submit',
            data
        })
    },
    selectOne(data){
       return request({
            method:'post',
            url:'/leaveApp/getByEmpId',
            data
        }) 
    },
    selectDept(data){
        return request({
            method:'post',
            url:'/leaveApp/getByDeptId',
            data
        }) 
    },
    permit(data){
         return request({
            method:'post',
            url:'/leaveApp/permit',
            data
        })  
    }
}