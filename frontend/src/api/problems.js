import { request } from './request'
import { mockProblems } from './mock'

function normalizeProblem(problem) {
  const submissions = problem.submissions ?? problem.submit_count ?? 0
  const accepted = problem.accepted ?? problem.ac_count ?? 0
  return {
    ...problem,
    tags: problem.tags || [],
    source: problem.source || 'HFUTXC',
    status: problem.status || 'NONE',
    accepted,
    submissions,
    passRate: submissions ? Math.round((accepted / submissions) * 100) : 0
  }
}

export async function getProblems(params = {}) {
  try {
    const data = await request('/api/problems')
    return data.map(normalizeProblem)
  } catch {
    return mockProblems.map(normalizeProblem)
  }
}

export async function getProblem(id) {
  try {
    const data = await request(`/api/problems/${id}`)
    return normalizeProblem(data)
  } catch {
    const problem = mockProblems.find(item => String(item.id) === String(id)) || mockProblems[0]
    return normalizeProblem(problem)
  }
}

export async function submitCode({ userId = 1, problemId, language, code }) {
  return request('/api/submit', {
    method: 'POST',
    body: JSON.stringify({
      user_id: userId,
      problem_id: Number(problemId),
      language,
      code
    })
  })
}
