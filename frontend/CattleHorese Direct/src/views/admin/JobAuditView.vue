<script setup lang="ts">
import { computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRecruitmentStore, type Job } from '../../stores/recruitment'

const recruitment = useRecruitmentStore()

const pendingJobs = computed(() => recruitment.jobs.filter((j) => j.auditStatus === 'pending'))

function auditTagType(auditStatus: Job['auditStatus']) {
  if (auditStatus === 'approved') return 'success'
  if (auditStatus === 'pending') return 'warning'
  return 'danger'
}

function approve(job: Job) {
  recruitment.adminSetJobAudit(job.id, 'approved')
  ElMessage.success('已通过审核')
}

async function reject(job: Job) {
  const result = await ElMessageBox.prompt('请输入拒绝原因', '拒绝职位', {
    inputType: 'textarea',
    inputPlaceholder: '例如：岗位信息不符合要求（演示数据）',
    confirmButtonText: '确认拒绝',
    cancelButtonText: '取消',
  }).catch(() => null)

  if (!result) return
  recruitment.adminSetJobAudit(job.id, 'rejected', String(result.value || ''))
  ElMessage.success('已拒绝审核')
}
</script>

<template>
  <div>
    <div style="margin-bottom: 12px; font-weight: 700; font-size: 16px">职位审核</div>

    <el-empty v-if="pendingJobs.length === 0" description="暂无待审核职位" />

    <el-table v-else :data="pendingJobs" style="width: 100%">
      <el-table-column prop="title" label="职位" min-width="260" />
      <el-table-column prop="companyName" label="企业" min-width="220" />
      <el-table-column prop="location" label="地点" width="120" />
      <el-table-column prop="salary" label="薪资" width="140" />
      <el-table-column label="审核状态" width="140">
        <template #default="{ row }">
          <el-tag :type="auditTagType(row.auditStatus)">{{ row.auditStatus }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createdAt" label="提交时间" width="120" />
      <el-table-column label="操作" width="260" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button size="small" type="success" @click="approve(row)">通过</el-button>
            <el-button size="small" type="danger" @click="reject(row)">拒绝</el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

