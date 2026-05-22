import { mockProblems, mockTrainings } from './mock'

export async function getTrainings() {
  return mockTrainings
}

export async function getTraining(id) {
  return mockTrainings.find(item => String(item.id) === String(id)) || mockTrainings[0]
}

export async function getTrainingProblems(id) {
  return mockProblems.map((problem, index) => ({
    ...problem,
    order: index + 1,
    status: index === 0 ? 'AC' : index === 1 ? 'TRIED' : 'NONE'
  }))
}
