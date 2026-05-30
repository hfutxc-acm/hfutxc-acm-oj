import { request } from './request'

export function createProblem(payload) {
  return request('/api/admin/problems', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function updateProblem(id, payload) {
  return request(`/api/admin/problems/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload)
  })
}

export function deleteProblem(id, confirmProblemId) {
  return request(`/api/admin/problems/${id}`, {
    method: 'DELETE',
    body: JSON.stringify({ confirm_problem_id: Number(confirmProblemId) })
  })
}

export function uploadProblemData(problemId, file) {
  const formData = new FormData()
  formData.append('file', file)
  return request(`/api/admin/problems/${problemId}/testcases/upload`, {
    method: 'POST',
    body: formData
  })
}

export function getTestcases(problemId) {
  return request(`/api/admin/problems/${problemId}/testcases`)
}

export function getUsers() {
  return request('/api/admin/users')
}

export function updateUserRole(userId, role) {
  return request(`/api/admin/users/${userId}/role`, {
    method: 'PUT',
    body: JSON.stringify({ role })
  })
}

export function transferSuperAdmin(userId) {
  return request(`/api/admin/transfer_super_admin/${userId}`, {
    method: 'POST'
  })
}
