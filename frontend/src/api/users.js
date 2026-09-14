import api from './http'

// 用户管理 API（家长专属）
export const usersApi = {
  /** 公开的小孩列表（选择页用） */
  listKids() {
    return api.get('/users/kids')
  },
  list() {
    return api.get('/users')
  },
  create(data) {
    return api.post('/users', data)
  },
  update(id, data) {
    return api.put(`/users/${id}`, data)
  },
  updatePassword(id, data) {
    return api.put(`/users/${id}/password`, data)
  },
  remove(id) {
    return api.delete(`/users/${id}`)
  },
}
