<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'
import { useRecruitmentStore, type Job } from '../../stores/recruitment'

const auth = useAuthStore()
const recruitment = useRecruitmentStore()

const keyword = ref('')

const myJobs = computed(() => {
  if (!auth.userId) return []
  const kw = keyword.value.trim().toLowerCase()
  return recruitment.jobs
    .filter((j) => j.companyId === auth.userId)
    .filter((j) => !kw || j.title.toLowerCase().includes(kw) || j.location.includes(kw) || j.tags.some((t) => t.toLowerCase().includes(kw)))
})

const dialogVisible = ref(false)
const editingJobId = ref<number | null>(null)

const form = reactive({
  title: '',
  location: '',
  salary: '',
  description: '',
  tagsText: '',
})

const detailDialogVisible = ref(false)
const selectedJob = ref<Job | null>(null)

function resetForm() {
  form.title = ''
  form.location = ''
  form.salary = ''
  form.description = ''
  form.tagsText = ''
}

function parseTags(text: string) {
  return text
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

function openCreate() {
  editingJobId.value = null
  resetForm()
  dialogVisible.value = true
}

function openEdit(job: Job) {
  editingJobId.value = job.id
  form.title = job.title
  form.location = job.location
  form.salary = job.salary
  form.description = job.description
  form.tagsText = job.tags.join(',')
  dialogVisible.value = true
}

function openDetail(job: Job) {
  selectedJob.value = job
  detailDialogVisible.value = true
}

function submit() {
  if (!form.title.trim()) {
    ElMessage.warning('请输入职位名称')
    return
  }
  recruitment.createOrUpdateJob({
    jobId: editingJobId.value ?? undefined,
    title: form.title.trim(),
    location: form.location.trim(),
    salary: form.salary.trim(),
    description: form.description.trim(),
    tags: parseTags(form.tagsText),
  })
  dialogVisible.value = false
  ElMessage.success('已提交职位审核（演示数据）')
}

function auditTagType(auditStatus: Job['auditStatus']) {
  if (auditStatus === 'approved') return 'success'
  if (auditStatus === 'pending') return 'warning'
  return 'danger'
}
</script>

<template>
  <div>
    <div style="margin-bottom: 16px; display: flex; align-items: center; gap: 12px">
      <el-input v-model="keyword" placeholder="搜索职位/地点/标签" style="width: 360px" clearable />
      <el-button type="primary" style="margin-left: auto" @click="openCreate">发布职位</el-button>
    </div>

    <el-table :data="myJobs" style="width: 100%">
      <el-table-column prop="title" label="职位" min-width="240" />
      <el-table-column prop="location" label="地点" width="120" />
      <el-table-column prop="salary" label="薪资" width="140" />
      <el-table-column label="审核状态" width="140">
        <template #default="{ row }">
          <el-tag :type="auditTagType(row.auditStatus)">{{ row.auditStatus }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="标签" min-width="220">
        <template #default="{ row }">
          <div style="display: flex; flex-wrap: wrap; gap: 6px">
            <el-tag v-for="t in row.tags" :key="t" size="small">{{ t }}</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" width="120" prop="createdAt" />
      <el-table-column label="操作" width="240" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button size="small" @click="openDetail(row)">详情</el-button>
            <el-button size="small" type="primary" @click="openEdit(row)">编辑</el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="editingJobId ? '编辑职位' : '发布职位'" width="720">
      <el-form label-width="100px">
        <el-form-item label="职位名称">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="工作地点">
          <el-input v-model="form.location" />
        </el-form-item>
        <el-form-item label="薪资范围">
          <el-input v-model="form.salary" />
        </el-form-item>
        <el-form-item label="标签（逗号分隔）">
          <el-input v-model="form.tagsText" placeholder="例如：Vue, TypeScript" />
        </el-form-item>
        <el-form-item label="岗位描述">
          <el-input v-model="form.description" type="textarea" :rows="5" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submit">提交审核</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="detailDialogVisible" title="职位详情" width="720">
      <div v-if="selectedJob">
        <div style="font-weight: 700; font-size: 16px">{{ selectedJob.title }}</div>
        <div style="margin-top: 8px; color: var(--color-text); opacity: 0.8">
          {{ selectedJob.location }} · {{ selectedJob.salary }}
        </div>
        <div style="margin-top: 14px">
          <div style="font-weight: 700; margin-bottom: 6px">岗位描述</div>
          <div style="white-space: pre-wrap">{{ selectedJob.description }}</div>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

