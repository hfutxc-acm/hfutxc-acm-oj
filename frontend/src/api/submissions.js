import { request } from './request'

function normalizeSubmission(item) {
  return {
    id: item.id,
    user: item.username || item.user || `User #${item.user_id || 1}`,
    user_id: item.user_id,
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
  const data = await request('/api/submissions')
  return data.map(normalizeSubmission)
}

export async function getSubmission(id) {
  const data = await request(`/api/submissions/${id}`)
  return normalizeSubmission(data)
}
