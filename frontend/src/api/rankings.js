import { mockRanks } from './mock'

export async function getRankings(type = 'all') {
  return type === 'freshman' ? mockRanks.slice(1) : mockRanks
}
