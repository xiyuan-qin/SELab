<script setup lang="ts">
import { computed, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../stores/auth'
import { useRecruitmentStore, type Candidate } from '../../stores/recruitment'

const auth = useAuthStore()
const recruitment = useRecruitmentStore()

const currentCandidate = computed<Candidate | undefined>(() => {
  if (!auth.userId) return undefined
  return recruitment.candidates.find((c) => c.id === auth.userId)
})

const edit = reactive({
  education: '',
  major: '',
  years: 0,
  resumeSummary: '',
  skillsText: '',
})

watch(
  currentCandidate,
  (c) => {
    if (!c) return
    edit.education = c.education
    edit.major = c.major
    edit.years = c.years
    edit.resumeSummary = c.resumeSummary
    edit.skillsText = c.skills.join(',')
  },
  { immediate: true },
)

function parseSkills(text: string) {
  return text
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

function onSave() {
  if (!auth.userId) return
  recruitment.updateCandidateProfile(auth.userId, {
    education: edit.education,
    major: edit.major,
    years: edit.years,
    resumeSummary: edit.resumeSummary,
    skills: parseSkills(edit.skillsText),
  })
  ElMessage.success('保存成功')
}
</script>

<template>
  <div>
    <div style="margin-bottom: 12px; display: flex; align-items: center; gap: 12px">
      <div style="font-weight: 700; font-size: 16px">个人信息</div>
      <div style="margin-left: auto; opacity: 0.7">当前登录：{{ auth.userName }}</div>
    </div>

    <el-card shadow="never">
      <el-form label-width="100px">
        <el-form-item label="姓名">
          <el-input :model-value="auth.userName" disabled />
        </el-form-item>
        <el-form-item label="学历">
          <el-input v-model="edit.education" />
        </el-form-item>
        <el-form-item label="专业">
          <el-input v-model="edit.major" />
        </el-form-item>
        <el-form-item label="工作年限">
          <el-input-number v-model="edit.years" :min="0" :max="50" />
        </el-form-item>
        <el-form-item label="简历摘要">
          <el-input v-model="edit.resumeSummary" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="技能标签（,分隔）">
          <el-input v-model="edit.skillsText" placeholder="例如：Vue, TypeScript, Node.js" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onSave">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

