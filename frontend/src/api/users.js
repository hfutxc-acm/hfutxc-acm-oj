import { request } from './request'

export const usersApi = {
  getUserProfile(userId) {
    return request(`/api/users/${userId}`)
  },
  
  uploadAvatar(userId, file) {
    const formData = new FormData()
    formData.append('file', file)
    return request(`/api/users/${userId}/avatar`, {
      method: 'POST',
      body: formData
    })
  }
}
