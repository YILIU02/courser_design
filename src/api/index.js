import http from './http'

const api = {
  auth: {
    login: (payload) => http.post('/auth/login', payload),
    me: () => http.get('/auth/me'),
  },
  meta: {
    options: () => http.get('/meta/options'),
  },
  dashboard: {
    overview: () => http.get('/dashboard/overview'),
  },
  employees: {
    list: (params) => http.get('/employees', { params }),
    create: (payload) => http.post('/employees', payload),
    update: (id, payload) => http.put(`/employees/${id}`, payload),
  },
  projects: {
    list: (params) => http.get('/projects', { params }),
    create: (payload) => http.post('/projects', payload),
    update: (id, payload) => http.put(`/projects/${id}`, payload),
  },
  attendance: {
    list: (params) => http.get('/attendance', { params }),
    checkIn: () => http.post('/attendance/check-in'),
    checkOut: () => http.post('/attendance/check-out'),
  },
  performance: {
    list: (params) => http.get('/performance', { params }),
  },
  leaves: {
    list: (params) => http.get('/leaves', { params }),
    create: (payload) => http.post('/leaves', payload),
    decide: (id, payload) => http.post(`/leaves/${id}/decision`, payload),
  },
}

export default api
