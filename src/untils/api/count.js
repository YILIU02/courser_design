import request from '../request'
export default{
    humanCount(){
        return request({
            method:'get',
            url:'/emp/count'
        })
    }
}