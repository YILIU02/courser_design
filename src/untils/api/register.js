import request from '../request'
export default {
    //{
    //     "empId": "",
    //     "empName": "",
    //     "deptId": ""
    // }
    register1(data) {
     return   request({
            method: 'post',
            url: '/emp/register_1',
            data
        })
    },
//     {
//     "username": "",
//     "password": "",
//     "empId": "",
//     "roleId": ""
// }
    register2(data) {
      return  request({
            method: 'post',
            url: '/emp/register_2',
            data
        })
    }
}