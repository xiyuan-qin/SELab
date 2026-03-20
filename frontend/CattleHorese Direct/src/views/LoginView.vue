<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore, type UserRole } from '../stores/auth'
import { useRecruitmentStore } from '../stores/recruitment'

const router = useRouter()
const auth = useAuthStore()
const recruitment = useRecruitmentStore()

const form = reactive({
  role: 'candidate' as UserRole,
  name: '',
})

const submitting = ref(false)

function getTargetPath(role: UserRole) {
  if (role === 'candidate') return '/candidate/jobs'
  if (role === 'enterprise') return '/enterprise/jobs/manage'
  return '/admin/users'
}

function normalizeName(name: string) {
  return name.trim()
}

async function onLogin() {
  const name = normalizeName(form.name)
  if (form.role !== 'admin' && !name) {
    ElMessage.warning('请输入用户名/企业名称')
    return
  }

  submitting.value = true
  try {
    if (form.role === 'admin') {
      auth.login({ id: 0, name: '管理员', role: 'admin' })
    } else if (form.role === 'candidate') {
      const c = recruitment.upsertCandidateByName(name)
      auth.login({ id: c.id, name: c.name, role: 'candidate' })
    } else {
      const company = recruitment.upsertCompanyByName(name)
      auth.login({ id: company.id, name: company.name, role: 'enterprise' })
    }

    router.push(getTargetPath(form.role))
  } catch (e) {
    ElMessage.error((e as Error).message || '登录失败')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="login-wrap">
    <el-card class="login-card" shadow="never">
      <template #header>
        <div class="login-title">人才招聘系统登录</div>
      </template>

      <el-form :model="form" label-width="80px">
        <el-form-item label="角色">
          <el-select v-model="form.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="候选人" value="candidate" />
            <el-option label="企业用户" value="enterprise" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>

        <el-form-item v-if="form.role !== 'admin'" label="名称">
          <el-input v-model="form.name" placeholder="请输入你的姓名/企业名称" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" style="width: 100%" @click="onLogin">
            {{ submitting ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.login-card {
  width: 520px;
}

.login-title {
  font-size: 18px;
  font-weight: 700;
}
</style>

