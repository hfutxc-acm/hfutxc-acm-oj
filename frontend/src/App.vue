<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { currentRoute, destroyRouter, initRouter } from './router'
import MainLayout from './components/layout/MainLayout.vue'
import AdminLayout from './components/layout/AdminLayout.vue'
import HomePage from './pages/HomePage.vue'
import ProblemsPage from './pages/ProblemsPage.vue'
import ProblemDetailPage from './pages/ProblemDetailPage.vue'
import ProblemSolutionsPage from './pages/ProblemSolutionsPage.vue'
import SolutionPublishPage from './pages/SolutionPublishPage.vue'
import TrainingsPage from './pages/TrainingsPage.vue'
import TrainingDetailPage from './pages/TrainingDetailPage.vue'
import ContestsPage from './pages/ContestsPage.vue'
import ContestDetailPage from './pages/ContestDetailPage.vue'
import ContestRankingPage from './pages/ContestRankingPage.vue'
import SubmissionsPage from './pages/SubmissionsPage.vue'
import SubmissionDetailPage from './pages/SubmissionDetailPage.vue'
import RankingsPage from './pages/RankingsPage.vue'
import ProfilePage from './pages/ProfilePage.vue'
import PlaceholderPage from './pages/PlaceholderPage.vue'
import AdminHomePage from './pages/AdminHomePage.vue'
import AdminProblemsPage from './pages/AdminProblemsPage.vue'
import AdminProblemFormPage from './pages/AdminProblemFormPage.vue'
import AdminPlaceholderPage from './pages/AdminPlaceholderPage.vue'
import AdminUsersPage from './pages/admin/AdminUsersPage.vue'


const routeComponent = computed(() => {
  const map = {
    home: HomePage,
    problems: ProblemsPage,
    'problem-detail': ProblemDetailPage,
    'problem-solutions': ProblemSolutionsPage,
    'problem-discussions': PlaceholderPage,
    'solution-publish': SolutionPublishPage,
    trainings: TrainingsPage,
    'training-detail': TrainingDetailPage,
    contests: ContestsPage,
    'contest-detail': ContestDetailPage,
    'contest-problem': ProblemDetailPage,
    'contest-ranking': ContestRankingPage,
    'contest-submissions': SubmissionsPage,
    submissions: SubmissionsPage,
    'submission-detail': SubmissionDetailPage,
    rankings: RankingsPage,
    'freshman-ranking': RankingsPage,
    discussions: PlaceholderPage,
    'user-profile': ProfilePage,
    me: ProfilePage,
    about: PlaceholderPage,
    join: PlaceholderPage,
    forbidden: PlaceholderPage,
    'not-found': PlaceholderPage
  }
  return map[currentRoute.value.name] || PlaceholderPage
})

const adminComponent = computed(() => {
  const map = {
    admin: AdminHomePage,
    'admin-problems': AdminProblemsPage,
    'admin-problem-new': AdminProblemFormPage,
    'admin-problem-edit': AdminProblemFormPage,
    'admin-contests': AdminPlaceholderPage,
    'admin-contest-new': AdminPlaceholderPage,
    'admin-trainings': AdminPlaceholderPage,
    'admin-users': AdminUsersPage
  }
  return map[currentRoute.value.name] || AdminHomePage
})

const isAdminRoute = computed(() => currentRoute.value.name?.startsWith('admin'))

onMounted(initRouter)
onUnmounted(destroyRouter)
</script>

<template>
  <MainLayout>
    <AdminLayout v-if="isAdminRoute">
      <component :is="adminComponent" :key="currentRoute.path" />
    </AdminLayout>
    <component v-else :is="routeComponent" :key="currentRoute.path" />
  </MainLayout>
</template>