import { reactive } from 'vue'

export const authStore = reactive({
  currentUser: {
    id: 1,
    username: 'demo-admin',
    role: 'admin'
  }
})

export function canAccessAdmin() {
  return ['admin', 'team_member'].includes(authStore.currentUser?.role)
}
