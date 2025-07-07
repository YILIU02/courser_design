import axios from "axios";
const service = axios.create({
    baseURL: 'http://111.230.242.244:8081',//设置后端接口
    // baseURL:'127.0.0.1:8082',
    responseType: 'blob'

})
//请求拦截器，前端给后端发送数据
service.interceptors.request.use(config => {
    config.headers['token'] = localStorage.getItem('token')
    return config
}, err => {
    if (err.response.status == 401) {
        return Promise.reject('token已过期,请重新登录')
    }
    return Promise.reject(err)
});
service.interceptors.response.use(response => {
    return response

}, err => {
    console.log(err);

})
export default service