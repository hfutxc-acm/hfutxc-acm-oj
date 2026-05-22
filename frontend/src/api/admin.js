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

export function deleteProblem(id) {
  return request(`/api/admin/problems/${id}`, {
    method: 'DELETE'
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
