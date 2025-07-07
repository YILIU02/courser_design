import request from '../request'
export default {
    getToday(data) {
        return request({
            method: 'get',
            url: '/attd/getToday',
            params: { empId: data }
        })
    },
    checkIn(data) {
        return request({
            method: 'post',
            url: '/attd/checkIn',
            data: { empId: data }
        })
    },
    checkOut(data) {
        return request({
            method: 'post',
            url: '/attd/checkOut',
            data: { empId: data }
        })
    },
    getpHistory(data, date) {
        return request({
            method: 'post',
            url: '/attd/getHistory',
            data: {
                empId: data,
                date
            }
        })
    },
    getdHistory(deptId, empId, empName, date) {
        return request({
            method: 'post',
            url: '/attd/getByDeptId',
            data: {
                empId,
                date,
                empName,
                deptId
            }
        })
    },
    getHistory(deptId, empId, empName, date) {
        return request({
            method: 'post',
            url: '/attd/list',
            data: {
                empId,
                date,
                empName,
                deptId
            }
        })
    }
}