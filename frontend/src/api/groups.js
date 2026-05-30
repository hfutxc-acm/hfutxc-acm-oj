import { request } from './request'

export const groupsApi = {
  getGroups() {
    return request('/api/groups')
  },
  
  createGroup(name, description) {
    return request('/api/groups', {
      method: 'POST',
      body: JSON.stringify({ name, description })
    })
  },
  
  joinGroup(groupId) {
    return request(`/api/groups/${groupId}/join`, {
      method: 'POST'
    })
  },
  
  leaveGroup(groupId) {
    return request(`/api/groups/${groupId}/leave`, {
      method: 'POST'
    })
  }
}
