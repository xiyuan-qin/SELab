<script setup lang="ts">
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'
import { useRecruitmentStore, type Application } from '../../stores/recruitment'

const auth = useAuthStore()
const recruitment = useRecruitmentStore()

const jobDialogVisible = ref(false)
const selectedApp = ref<Application | null>(null)

const myApps = computed(() => {
  if (!auth.userId) return []
  return recruitment.getApplicationsByCandidate(auth.userId)
})

function statusTagType(status: Application['status']) {
  if (status === 'submitted') return 'info'
  if (status === 'reviewing') return 'warning'
  if (status === 'interview') return 'primary'
  if (status === 'accepted') return 'success'
  return 'danger'
}

function openApp(app: Application) {
  selectedApp.value = app
  jobDialogVisible.value = true
}

function withdraw(app: Application) {
  if (!app) return
  recruitment.updateApplicationStatus(app.id, 'rejected', '候选人撤回（演示）')
  ElMessage.success('已撤回')
}
</script>

<template>
  <div>
    <div style="margin-bottom: 12px; display: flex; align-items: center">
      <div style="font-weight: 700; font-size: 16px">我的投递</div>
      <div style="margin-left: auto; opacity: 0.7">当前登录：{{ auth.userName }}</div>
    </div>

    <el-empty v-if="myApps.length === 0" description="暂无投递记录" />

    <el-table v-else :data="myApps" style="width: 100%">
      <el-table-column prop="jobTitle" label="职位" min-width="260" />
      <el-table-column prop="companyName" label="公司" min-width="200" />
      <el-table-column prop="appliedAt" label="投递日期" width="120" />
      <el-table-column label="状态" width="140">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="备注" min-width="220">
        <template #default="{ row }">
          <span style="opacity: 0.85">{{ row.note || '-' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button size="small" @click="openApp(row)">详情</el-button>
            <el-button
              size="small"
              type="danger"
              :disabled="row.status === 'accepted' || row.status === 'rejected'"
              @click="withdraw(row)"
            >
              撤回
            </el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="jobDialogVisible" title="投递详情" width="720">
      <div v-if="selectedApp">
        <div style="font-weight: 700; font-size: 16px">{{ selectedApp.jobTitle }}</div>
        <div style="margin-top: 6px; color: var(--color-text); opacity: 0.8">
          {{ selectedApp.companyName }} · {{ selectedApp.appliedAt }}
        </div>

        <div style="margin-top: 14px">
          <div style="font-weight: 700; margin-bottom: 6px">当前状态</div>
          <el-tag :type="statusTagType(selectedApp.status)">{{ selectedApp.status }}</el-tag>
        </div>

        <div style="margin-top: 14px">
          <div style="font-weight: 700; margin-bottom: 6px">备注</div>
          <div style="white-space: pre-wrap">{{ selectedApp.note || '-' }}</div>
        </div>
      </div>

      <template #footer>
        <el-button @click="jobDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

