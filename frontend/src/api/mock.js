export const mockStats = {
  problems: 128,
  users: 316,
  todaySubmissions: 247,
  upcomingContests: 3
}

export const mockProblems = [
  {
    id: 1001,
    title: 'A+B Problem',
    difficulty: '入门',
    description: '输入两个整数 a 和 b，输出它们的和。',
    input_description: '一行两个整数 a,b。',
    output_description: '一行一个整数，表示 a+b。',
    sample_input: '1 2',
    sample_output: '3',
    time_limit_ms: 1000,
    memory_limit_mb: 256,
    tags: ['语法', '入门'],
    source: '新生训练',
    accepted: 238,
    submissions: 301,
    status: 'AC',
    testcase_count: 2
  },
  {
    id: 1002,
    title: 'STL 计数练习',
    difficulty: '普及-',
    description: '给定若干字符串，统计每个字符串出现次数。',
    input_description: '第一行 n，接下来 n 行字符串。',
    output_description: '按字典序输出每个字符串和出现次数。',
    sample_input: '3\na\nb\na',
    sample_output: 'a 2\nb 1',
    time_limit_ms: 1000,
    memory_limit_mb: 256,
    tags: ['STL', '模拟'],
    source: '专题训练',
    accepted: 91,
    submissions: 142,
    status: 'TRIED',
    testcase_count: 6
  },
  {
    id: 1003,
    title: '基础迷宫',
    difficulty: '普及+',
    description: '在网格中从起点走到终点，求最短步数。',
    input_description: 'n,m 和 n 行地图。',
    output_description: '最短步数，不可达输出 -1。',
    sample_input: '3 3\nS..\n.#.\n..T',
    sample_output: '4',
    time_limit_ms: 2000,
    memory_limit_mb: 256,
    tags: ['搜索', 'BFS'],
    source: '新生赛',
    accepted: 64,
    submissions: 129,
    status: 'NONE',
    testcase_count: 8
  }
]

export const mockTrainings = [
  { id: 1, title: '新生入门路线', type: '新生入门', description: '从 C++ 语法到基础搜索，适合零基础同学。', count: 24, done: 8, difficulty: '入门 - 普及-', tags: ['语法', 'STL', '模拟'] },
  { id: 2, title: '搜索基础专题', type: '专题训练', description: 'DFS、BFS、连通块、最短路建模入门。', count: 18, done: 5, difficulty: '普及- - 普及+', tags: ['搜索', '图论'] },
  { id: 3, title: '校赛补题 2026 春', type: '校赛补题', description: '校赛原题整理与补题路线。', count: 12, done: 3, difficulty: '入门 - 提高', tags: ['模拟', 'DP', '贪心'] },
  { id: 4, title: '队内周作业：DP 入门', type: '队内作业', description: '线性 DP、背包、区间 DP 的基础题单。', count: 20, done: 6, difficulty: '普及+ - 提高', tags: ['DP'] }
]

export const mockContests = [
  { id: 1, title: 'HFUTXC 新生热身赛', start: '2026-06-01 19:00', end: '2026-06-01 22:00', duration: '3h', status: '未开始', rule: 'ACM' },
  { id: 2, title: 'XCPC 周赛 #12', start: '2026-05-25 19:00', end: '2026-05-25 22:00', duration: '3h', status: '未开始', rule: 'ACM' },
  { id: 3, title: '校赛补题场', start: '2026-05-10 00:00', end: '2026-06-10 23:59', duration: '长期', status: '补题中', rule: 'ACM' }
]

export const mockSubmissions = [
  { id: 901, user: 'demo', problem_id: 1001, problem_title: 'A+B Problem', language: 'cpp', status: 'AC', time_ms: 12, memory_kb: 512, created_at: '2026-05-23 10:12:01' },
  { id: 902, user: 'freshman01', problem_id: 1003, problem_title: '基础迷宫', language: 'cpp', status: 'WA', time_ms: 24, memory_kb: 640, created_at: '2026-05-23 10:15:29' }
]

export const mockRanks = [
  { rank: 1, username: 'xcpc_jiang', signature: '2026 继续冲', ac: 188, submissions: 290, lastActive: '今天' },
  { rank: 2, username: 'freshman01', signature: 'C++ 入门中', ac: 76, submissions: 140, lastActive: '今天' },
  { rank: 3, username: 'demo', signature: '补题使我快乐', ac: 42, submissions: 80, lastActive: '昨天' }
]

export const mockContestRank = [
  { rank: 1, team: 'XCPC-Alpha', solved: 7, penalty: 612, problems: ['+', '+1', '+', '-', '+', '+2', '+'] },
  { rank: 2, team: 'Freshman-01', solved: 5, penalty: 438, problems: ['+', '+', '-', '+1', '+', '.', '+'] },
  { rank: 3, team: 'Demo Team', solved: 3, penalty: 260, problems: ['+', '-', '+', '.', '.', '+', '.'] }
]

export const roadmap = ['C++ 语法入门', 'STL 与模拟', '搜索基础', 'DP 入门', '图论基础', '数论基础']

export const announcements = [
  { title: '2026 春季校赛报名开放', type: '校赛通知', date: '2026-05-23' },
  { title: 'HFUTXC ACM 新生招新说明会', type: '招新通知', date: '2026-05-25' },
  { title: 'XCPC 暑期训练队选拔安排', type: '训练安排', date: '2026-06-02' }
]
