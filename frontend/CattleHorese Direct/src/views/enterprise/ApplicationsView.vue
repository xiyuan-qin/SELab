<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'
import { useRecruitmentStore, type Application, type ApplicationStatus } from '../../stores/recruitment'

const auth = useAuthStore()
const recruitment = useRecruitmentStore()

const selectedJobId = ref<number | null>(null)

const myJobs = computed(() => {
  if (!auth.userId) return []
  return recruitment.jobs.filter((j) => j.companyId === auth.userId)
})

watch(
  myJobs,
  (jobs) => {
    if (jobs.length === 0) {
      selectedJobId.value = null
      return
    }
    if (selectedJobId.value === null) selectedJobId.value = jobs[0]?.id ?? null
  },
  { immediate: true },
)

const appsForSelectedJob = computed(() => {
  if (!auth.userId || !selectedJobId.value) return []
  return recruitment.getApplicationsByCompany(auth.userId, selectedJobId.value)
})

const processDialogVisible = ref(false)
const processingApp = ref<Application | null>(null)

const newStatus = ref<ApplicationStatus>('reviewing')
const note = ref('')

const currentCandidate = computed(() => {
  if (!processingApp.value) return undefined
  return recruitment.candidates.find((c) => c.id === processingApp.value?.candidateId)
})

function statusTagType(status: ApplicationStatus) {
  if (status === 'submitted') return 'info'
  if (status === 'reviewing') return 'warning'
  if (status === 'interview') return 'primary'
  if (status === 'accepted') return 'success'
  return 'danger'
}

function openProcess(app: Application) {
  processingApp.value = app
  newStatus.value = app.status
  note.value = app.note || ''
  processDialogVisible.value = true
}

function saveProcess() {
  if (!processingApp.value) return
  recruitment.updateApplicationStatus(processingApp.value.id, newStatus.value, note.value)
  processDialogVisible.value = false
  ElMessage.success('处理结果已更新（演示数据）')
}
</script>

<template>
  <div>
    <div style="margin-bottom: 12px; display: flex; align-items: center; gap: 12px">
      <div style="font-weight: 700; font-size: 16px">申请管理</div>
      <div style="margin-left: auto; opacity: 0.7">当前登录：{{ auth.userName }}</div>
    </div>

    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px">
      <div style="width: 220px; color: var(--color-text); opacity: 0.85">选择职位</div>
      <el-select v-model="selectedJobId" placeholder="请选择职位" style="width: 360px" clearable>
        <el-option v-for="j in myJobs" :key="j.id" :label="j.title" :value="j.id" />
      </el-select>
    </div>

    <el-empty v-if="!selectedJobId || appsForSelectedJob.length === 0" description="暂无申请记录" />

    <el-table v-else :data="appsForSelectedJob" style="width: 100%">
      <el-table-column prop="candidateName" label="候选人" min-width="180" />
      <el-table-column prop="appliedAt" label="申请日期" width="120" />
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
      <el-table-column label="操作" width="170" fixed="right">
        <template #default="{ row }">
          <el-button size="small" type="primary" @click="openProcess(row)">处理</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="processDialogVisible" title="更新申请状态" width="760">
      <div v-if="processingApp">
        <div style="font-weight: 700; font-size: 16px">{{ processingApp.candidateName }}</div>
        <div style="margin-top: 6px; opacity: 0.8">
          {{ processingApp.jobTitle }} · {{ processingApp.companyName }}
        </div>

        <div style="margin-top: 14px">
          <div style="font-weight: 700; margin-bottom: 6px">候选人概览</div>
          <div style="opacity: 0.9">
            <div>学历：{{ currentCandidate?.education || '-' }}</div>
            <div>专业：{{ currentCandidate?.major || '-' }}</div>
            <div>工作年限：{{ currentCandidate?.years ?? '-' }}</div>
            <div style="margin-top: 8px">简历摘要：{{ currentCandidate?.resumeSummary || '-' }}</div>
          </div>
          <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px">
            <el-tag v-for="s in currentCandidate?.skills || []" :key="s" size="small">{{ s }}</el-tag>
          </div>
        </div>

        <el-form style="margin-top: 16px" label-width="110px">
          <el-form-item label="新状态">
            <el-select v-model="newStatus" style="width: 240px">
              <el-option label="submitted-已提交" value="submitted" />
              <el-option label="reviewing-审核中" value="reviewing" />
              <el-option label="interview-面试" value="interview" />
              <el-option label="accepted-录用" value="accepted" />
              <el-option label="rejected-淘汰" value="rejected" />
            </el-select>
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="note" type="textarea" :rows="3" placeholder="例如：通过初筛、安排面试时间等" />
          </el-form-item>
        </el-form>
      </div>

      <template #footer>
        <el-button @click="processDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProcess">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

