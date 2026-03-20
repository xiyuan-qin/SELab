<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore, type UserRole } from '../stores/auth'

type MenuItem = {
  label: string
  path: string
  role: UserRole
}

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const activePath = computed(() => route.path)
const userName = computed(() => auth.userName || '未登录')

const menuItems: MenuItem[] = [
  // Candidate
  { label: '职位搜索', path: '/candidate/jobs', role: 'candidate' },
  { label: '我的投递', path: '/candidate/applications', role: 'candidate' },
  { label: '个人信息', path: '/candidate/profile', role: 'candidate' },

  // Enterprise
  { label: '职位管理', path: '/enterprise/jobs/manage', role: 'enterprise' },
  { label: '申请管理', path: '/enterprise/applications', role: 'enterprise' },
  { label: '公司信息', path: '/enterprise/company', role: 'enterprise' },

  // Admin
  { label: '用户管理', path: '/admin/users', role: 'admin' },
  { label: '职位审核', path: '/admin/job-audit', role: 'admin' },
]

const filteredMenuItems = computed(() => {
  if (!auth.role) return []
  return menuItems.filter((m) => m.role === auth.role)
})

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <el-container class="app-layout">
    <el-header height="60" class="app-header">
      <div class="left">
        <img alt="logo" class="logo" src="@/assets/logo.svg" />
        <div class="title">人才招聘系统</div>
      </div>

      <div class="right">
        <el-dropdown trigger="click">
          <span class="user">
            {{ userName }}
            <span class="caret">▼</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-container>
      <el-aside width="220" class="app-aside">
        <el-menu
          router
          :default-active="activePath"
          class="menu"
          background-color="transparent"
          text-color="inherit"
          active-text-color="#409eff"
        >
          <el-menu-item v-for="m in filteredMenuItems" :key="m.path" :index="m.path">
            {{ m.label }}
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-main class="app-main">
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  background: var(--color-background-soft);
  border-bottom: 1px solid var(--color-border);
}

.left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 34px;
  height: 34px;
}

.title {
  font-weight: 700;
}

.user {
  cursor: pointer;
  user-select: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.caret {
  font-size: 10px;
  color: var(--color-text);
}

.app-aside {
  border-right: 1px solid var(--color-border);
  padding: 12px 0;
}

.menu {
  border-right: none;
}

.app-main {
  padding: 20px;
}
</style>

