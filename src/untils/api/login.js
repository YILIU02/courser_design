import request from '../request'
export default {
    Login(data) {
         // 登录接口
    //{
    // username:''
    // password:''
    // }
        return request({
            method: 'post',
            url: 'login',
            data
        })
    }
}