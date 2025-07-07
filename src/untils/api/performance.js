import request from '../request'
import load from '../load'
export default {
    getOne(data) {
        return request({
            method: 'post',
            url: '/ind/getByEmpId',
            data
        })
    },
    getDept(data) {
        return request({
            method: 'post',
            url: '/ind/getByDeptId',
            data
        })
    },
    getAll(data) {
        return request({
            method: 'post',
            url: '/ind/list',
            data
        })
    },
    getYear() {
        return request({
            method: 'get',
            url: '/ind/getYear',
        })
    },
    loadAll() {
        return load({
            method: 'get',
            url: '/ind/report',
      
        })
}
}