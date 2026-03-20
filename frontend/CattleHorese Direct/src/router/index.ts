import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../layout/AppLayout.vue'
import LoginView from '../views/LoginView.vue'
import RedirectView from '../views/RedirectView.vue'

import CandidateJobsView from '../views/candidate/JobListView.vue'
import CandidateApplicationsView from '../views/candidate/MyApplicationsView.vue'
import CandidateProfileView from '../views/candidate/ProfileView.vue'

import EnterpriseJobManagementView from '../views/enterprise/JobManagementView.vue'
import EnterpriseApplicationsView from '../views/enterprise/ApplicationsView.vue'
import EnterpriseCompanyInfoView from '../views/enterprise/CompanyInfoView.vue'

import AdminUserManagementView from '../views/admin/UserManagementView.vue'
import AdminJobAuditView from '../views/admin/JobAuditView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'root-redirect',
          component: RedirectView,
        },
        // Candidate
        { path: 'candidate/jobs', name: 'candidate-jobs', component: CandidateJobsView },
        {
          path: 'candidate/applications',
          name: 'candidate-applications',
          component: CandidateApplicationsView,
        },
        {
          path: 'candidate/profile',
          name: 'candidate-profile',
          component: CandidateProfileView,
        },

        // Enterprise
        { path: 'enterprise/jobs/manage', name: 'enterprise-jobs', component: EnterpriseJobManagementView },
        {
          path: 'enterprise/applications',
          name: 'enterprise-applications',
          component: EnterpriseApplicationsView,
        },
        {
          path: 'enterprise/company',
          name: 'enterprise-company',
          component: EnterpriseCompanyInfoView,
        },

        // Admin
        { path: 'admin/users', name: 'admin-users', component: AdminUserManagementView },
        {
          path: 'admin/job-audit',
          name: 'admin-job-audit',
          component: AdminJobAuditView,
        },
      ],
    },
  ],
})

export default router
