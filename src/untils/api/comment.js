import request from '../request'

export default {
    skill(empId, score) {
        return request({
            method: 'post',
            url: '/ind/rate',
            data: {
                indId: '3',
                empId,
                score
            }
        })
    },
    business(empId, score) {
        return request({
            method: 'post',
            url: '/ind/rate',
            data: {
                indId: '1',
                empId,
                score
            }
        })
    }
}