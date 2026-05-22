import { mockContestRank, mockContests, mockProblems, mockSubmissions } from './mock'

export async function getContests() {
  return mockContests
}

export async function getContest(id) {
  return mockContests.find(item => String(item.id) === String(id)) || mockContests[0]
}

export async function getContestProblems() {
  return mockProblems.slice(0, 3).map((problem, index) => ({
    ...problem,
    contestIndex: String.fromCharCode(65 + index)
  }))
}

export async function getContestRanking() {
  return mockContestRank
}

export async function getContestSubmissions() {
  return mockSubmissions
}
