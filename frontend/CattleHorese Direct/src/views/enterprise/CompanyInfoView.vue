<script setup lang="ts">
import { computed, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'
import { useRecruitmentStore, type Company } from '../../stores/recruitment'

const auth = useAuthStore()
const recruitment = useRecruitmentStore()

const currentCompany = computed<Company | undefined>(() => {
  if (!auth.userId) return undefined
  return recruitment.companies.find((c) => c.id === auth.userId)
})

const edit = reactive({
  industry: '',
  size: '',
  contactEmail: '',
})

watch(
  currentCompany,
  (c) => {
    if (!c) return
    edit.industry = c.industry
    edit.size = c.size
    edit.contactEmail = c.contactEmail
  },
  { immediate: true },
)

function onSave() {
  if (!auth.userId) return
  recruitment.updateCompanyInfo(auth.userId, {
    industry: edit.industry,
    size: edit.size,
    contactEmail: edit.contactEmail,
  })
  ElMessage.success('保存成功')
}
</script>

<template>
  <div>
    <div style="margin-bottom: 12px; display: flex; align-items: center">
      <div style="font-weight: 700; font-size: 16px">公司信息</div>
      <div style="margin-left: auto; opacity: 0.7">当前登录：{{ auth.userName }}</div>
    </div>

    <el-card shadow="never">
      <el-form label-width="100px">
        <el-form-item label="公司名称">
          <el-input :model-value="auth.userName" disabled />
        </el-form-item>
        <el-form-item label="行业">
          <el-input v-model="edit.industry" />
        </el-form-item>
        <el-form-item label="规模">
          <el-input v-model="edit.size" />
        </el-form-item>
        <el-form-item label="联系邮箱">
          <el-input v-model="edit.contactEmail" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onSave">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

