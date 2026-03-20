<script setup lang="ts">
import { computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'
import { useRecruitmentStore } from '../../stores/recruitment'

const auth = useAuthStore()
const recruitment = useRecruitmentStore()

type Row =
  | { kind: 'candidate'; id: number; name: string; enabled: boolean; count: number }
  | { kind: 'enterprise'; id: number; name: string; enabled: boolean; count: number }

const rows = computed<Row[]>(() => {
  const candidateRows: Row[] = recruitment.candidates.map((c) => ({
    kind: 'candidate',
    id: c.id,
    name: c.name,
    enabled: c.enabled,
    count: recruitment.applications.filter((a) => a.candidateId === c.id).length,
  }))

  const enterpriseRows: Row[] = recruitment.companies.map((c) => ({
    kind: 'enterprise',
    id: c.id,
    name: c.name,
    enabled: c.enabled,
    count: recruitment.jobs.filter((j) => j.companyId === c.id).length,
  }))

  return [...enterpriseRows, ...candidateRows]
})

function enabledTagType(enabled: boolean) {
  return enabled ? 'success' : 'danger'
}

function toggleEnabled(row: Row) {
  if (row.kind === 'candidate') recruitment.toggleCandidateEnabled(row.id)
  if (row.kind === 'enterprise') recruitment.toggleCompanyEnabled(row.id)
  ElMessage.success('状态已更新（演示数据）')
}
</script>

<template>
  <div>
    <div style="margin-bottom: 12px; display: flex; align-items: center; gap: 12px">
      <div style="font-weight: 700; font-size: 16px">用户管理</div>
      <div style="margin-left: auto; opacity: 0.7">当前登录：{{ auth.userName }}</div>
    </div>

    <el-table :data="rows" style="width: 100%">
      <el-table-column label="类型" width="140">
        <template #default="{ row }">
          <el-tag>{{ row.kind === 'candidate' ? '候选人' : '企业' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="名称" min-width="220" />
      <el-table-column label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="enabledTagType(row.enabled)">{{ row.enabled ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="关联数量" width="140">
        <template #default="{ row }">
          <span style="opacity: 0.9">{{ row.count }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button size="small" type="primary" :disabled="row.kind === 'enterprise' && row.id === 0" @click="toggleEnabled(row)">
              {{ row.enabled ? '禁用' : '启用' }}
            </el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

