<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

function getTargetPath() {
  if (!auth.role) return '/login'
  if (auth.role === 'candidate') return '/candidate/jobs'
  if (auth.role === 'enterprise') return '/enterprise/jobs/manage'
  return '/admin/users'
}

onMounted(() => {
  router.replace(getTargetPath())
})
</script>

<template>
  <div style="padding: 20px">
    <el-skeleton rows="4" animated />
  </div>
</template>

