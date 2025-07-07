import axios from "axios";
const service=axios.create({
      baseURL:'http://111.230.242.244:8081',//设置后端接口
    //    baseURL:'http://127.0.0.1:8082',
        headers:{"Content-Type":'application/json',    
    }
})
//请求拦截器，前端给后端发送数据
service.interceptors.request.use(config=>{
    config.headers['token']=localStorage.getItem('token')
    return config
},err=>{
    if(err.response.status==401){
        return  Promise.reject('token已过期,请重新登录')
    }
  return  Promise.reject(err)
});
//响应拦截器，后端给前端返回数据
service.interceptors.response.use(response =>{
      console.log(response);
    if(response.data.code==1) return response.data;
    else return Promise.reject(new Error(response.data.msg))
},err=>{
    console.log(err);
    
})
export default service
