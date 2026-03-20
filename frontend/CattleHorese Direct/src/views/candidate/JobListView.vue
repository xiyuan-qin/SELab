<script setup lang="ts">
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'
import { useRecruitmentStore, type Job } from '../../stores/recruitment'

const auth = useAuthStore()
const recruitment = useRecruitmentStore()

const keyword = ref('')
const location = ref('')

const filteredJobs = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  const loc = location.value.trim()

  return recruitment.approvedJobs.filter((j) => {
    const matchKw =
      !kw || j.title.toLowerCase().includes(kw) || j.companyName.toLowerCase().includes(kw) || j.tags.some((t) => t.toLowerCase().includes(kw))
    const matchLoc = !loc || j.location.includes(loc)
    return matchKw && matchLoc
  })
})

const jobDialogVisible = ref(false)
const selectedJob = ref<Job | null>(null)

function openJob(job: Job) {
  selectedJob.value = job
  jobDialogVisible.value = true
}

function onApply(job: Job) {
  const res = recruitment.applyToJob(job.id)
  if (res.alreadyApplied) {
    ElMessage.info('你已投递过该职位')
    return
  }
  ElMessage.success('投递成功')
}
</script>

<template>
  <div>
    <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 16px">
      <el-input v-model="keyword" placeholder="搜索职位/公司/技能" style="width: 360px" clearable />
      <el-input v-model="location" placeholder="工作地点" style="width: 220px" clearable />
      <div style="margin-left: auto; color: var(--color-text); opacity: 0.7">
        当前登录：{{ auth.userName }}
      </div>
    </div>

    <el-table :data="filteredJobs" style="width: 100%">
      <el-table-column prop="title" label="职位" min-width="260" />
      <el-table-column prop="companyName" label="公司" min-width="200" />
      <el-table-column prop="location" label="地点" width="120" />
      <el-table-column prop="salary" label="薪资" width="140" />
      <el-table-column label="标签" min-width="220">
        <template #default="{ row }">
          <div style="display: flex; flex-wrap: wrap; gap: 6px">
            <el-tag v-for="t in row.tags" :key="t" size="small">{{ t }}</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="190" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button size="small" @click="openJob(row)">详情</el-button>
            <el-button size="small" type="primary" @click="onApply(row)">投递</el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="jobDialogVisible" title="职位详情" width="720">
      <div v-if="selectedJob">
        <div style="font-weight: 700; font-size: 16px">{{ selectedJob.title }}</div>
        <div style="margin-top: 8px; color: var(--color-text); opacity: 0.8">
          {{ selectedJob.companyName }} · {{ selectedJob.location }} · {{ selectedJob.salary }}
        </div>

        <div style="margin-top: 14px">
          <div style="font-weight: 700; margin-bottom: 6px">岗位描述</div>
          <div style="white-space: pre-wrap">{{ selectedJob.description }}</div>
        </div>

        <div style="margin-top: 14px">
          <div style="font-weight: 700; margin-bottom: 6px">技能标签</div>
          <div style="display: flex; flex-wrap: wrap; gap: 6px">
            <el-tag v-for="t in selectedJob.tags" :key="t">{{ t }}</el-tag>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="jobDialogVisible = false">关闭</el-button>
        <el-button v-if="selectedJob" type="primary" @click="onApply(selectedJob)">确认投递</el-button>
      </template>
    </el-dialog>
  </div>
</template>

