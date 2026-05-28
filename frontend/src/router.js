import { computed, reactive } from 'vue'
import { canAccessAdmin } from './stores/authStore'

const routes = [
  { name: 'home', path: /^\/$/, title: '首页' },
  { name: 'problems', path: /^\/problems$/, title: '题库' },
  { name: 'problem-detail', path: /^\/problems\/([^/]+)$/, title: '题目详情', keys: ['pid'] },
  { name: 'problem-solutions', path: /^\/problems\/([^/]+)\/solutions$/, title: '题解', keys: ['pid'] },
  { name: 'problem-discussions', path: /^\/problems\/([^/]+)\/discussions$/, title: '讨论', keys: ['pid'] },
  { name: 'solution-publish', path: /^\/solutions\/publish$/, title: '发布题解' },
  { name: 'trainings', path: /^\/trainings$/, title: '训练' },
  { name: 'training-detail', path: /^\/trainings\/([^/]+)$/, title: '训练详情', keys: ['tid'] },
  { name: 'contests', path: /^\/contests$/, title: '比赛' },
  { name: 'contest-detail', path: /^\/contests\/([^/]+)$/, title: '比赛主页', keys: ['cid'] },
  { name: 'contest-problem', path: /^\/contests\/([^/]+)\/problems\/([^/]+)$/, title: '比赛题目', keys: ['cid', 'pid'] },
  { name: 'contest-ranking', path: /^\/contests\/([^/]+)\/ranking$/, title: '比赛榜单', keys: ['cid'] },
  { name: 'contest-submissions', path: /^\/contests\/([^/]+)\/submissions$/, title: '比赛提交', keys: ['cid'] },
  { name: 'submissions', path: /^\/submissions$/, title: '提交' },
  { name: 'submission-detail', path: /^\/submissions\/([^/]+)$/, title: '提交详情', keys: ['sid'] },
  { name: 'rankings', path: /^\/rankings$/, title: '排名' },
  { name: 'freshman-ranking', path: /^\/rankings\/freshman$/, title: '新生排名' },
  { name: 'discussions', path: /^\/discussions$/, title: '交流' },
  { name: 'teams', path: /^\/teams$/, title: '组织大厅' },
  { name: 'auth', path: /^\/auth$/, title: '登录/注册' },
  { name: 'user-profile', path: /^\/users\/([^/]+)$/, title: '用户主页', keys: ['uid'] },
  { name: 'me', path: /^\/me$/, title: '个人中心' },
  { name: 'about', path: /^\/about$/, title: '关于我们' },
  { name: 'join', path: /^\/about\/join$/, title: '加入 ACM' },
  { name: 'admin', path: /^\/admin$/, title: '后台首页', admin: true },
  { name: 'admin-problems', path: /^\/admin\/problems$/, title: '题目管理', admin: true },
  { name: 'admin-problem-new', path: /^\/admin\/problems\/new$/, title: '新建题目', admin: true },
  { name: 'admin-problem-edit', path: /^\/admin\/problems\/([^/]+)\/edit$/, title: '编辑题目', keys: ['pid'], admin: true },
  { name: 'admin-contests', path: /^\/admin\/contests$/, title: '比赛管理', admin: true },
  { name: 'admin-contest-new', path: /^\/admin\/contests\/new$/, title: '新建比赛', admin: true },
  { name: 'admin-trainings', path: /^\/admin\/trainings$/, title: '训练管理', admin: true },
  { name: 'admin-users', path: /^\/admin\/users$/, title: '用户管理', admin: true }
]

export const routeState = reactive({
  path: window.location.pathname || '/',
  query: Object.fromEntries(new URLSearchParams(window.location.search))
})

function matchRoute(path) {
  for (const route of routes) {
    const match = path.match(route.path)
    if (match) {
      const params = {}
      route.keys?.forEach((key, index) => {
        params[key] = decodeURIComponent(match[index + 1])
      })
      if (route.admin && !canAccessAdmin()) {
        return { name: 'forbidden', title: '无权访问', params: {}, query: routeState.query }
      }
      return { ...route, params, query: routeState.query }
    }
  }
  return { name: 'not-found', title: '页面不存在', params: {}, query: routeState.query }
}

export const currentRoute = computed(() => matchRoute(routeState.path))

export function navigateTo(path) {
  if (path === `${window.location.pathname}${window.location.search}`) return
  window.history.pushState({}, '', path)
  updateRoute()
}

export function updateRoute() {
  routeState.path = window.location.pathname || '/'
  routeState.query = Object.fromEntries(new URLSearchParams(window.location.search))
}

export function initRouter() {
  window.addEventListener('popstate', updateRoute)
  updateRoute()
}

export function destroyRouter() {
  window.removeEventListener('popstate', updateRoute)
}
