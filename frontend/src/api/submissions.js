import { request } from './request'
import { mockSubmissions } from './mock'

function normalizeSubmission(item) {
  return {
    id: item.id,
    user: item.user || item.username || `User #${item.user_id || 1}`,
    problem_id: item.problem_id,
    problem_title: item.problem_title || `Problem ${item.problem_id || '-'}`,
    language: item.language,
    status: item.status,
    time_ms: item.time_ms ?? 0,
    memory_kb: item.memory_kb ?? 0,
    created_at: item.created_at,
    code: item.code || '',
    results: item.results || []
  }
}

export async function getSubmissions() {
  try {
    const data = await request('/api/submissions')
    return data.map(normalizeSubmission)
  } catch {
    return mockSubmissions.map(normalizeSubmission)
  }
}

export async function getSubmission(id) {
  try {
    const data = await request(`/api/submissions/${id}`)
    return normalizeSubmission(data)
  } catch {
    return mockSubmissions.map(normalizeSubmission).find(item => String(item.id) === String(id)) || mockSubmissions[0]
  }
}
