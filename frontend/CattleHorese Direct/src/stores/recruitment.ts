import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export type AuditStatus = 'pending' | 'approved' | 'rejected'
export type JobStatus = 'open' | 'closed'
export type ApplicationStatus = 'submitted' | 'reviewing' | 'interview' | 'accepted' | 'rejected'

export interface Company {
  id: number
  name: string
  industry: string
  size: string
  contactEmail: string
  enabled: boolean
}

export interface Candidate {
  id: number
  name: string
  phone: string
  email: string
  education: string
  major: string
  years: number
  resumeSummary: string
  skills: string[]
  enabled: boolean
}

export interface Job {
  id: number
  title: string
  companyId: number
  companyName: string
  location: string
  salary: string
  description: string
  tags: string[]
  status: JobStatus
  auditStatus: AuditStatus
  auditReason?: string
  createdAt: string
}

export interface Application {
  id: number
  jobId: number
  jobTitle: string
  companyId: number
  companyName: string
  candidateId: number
  candidateName: string
  appliedAt: string
  status: ApplicationStatus
  note?: string
}

export interface RecruitmentMeta {
  nextCompanyId: number
  nextCandidateId: number
  nextJobId: number
  nextApplicationId: number
}

export interface RecruitmentState {
  companies: Company[]
  candidates: Candidate[]
  jobs: Job[]
  applications: Application[]
  meta: RecruitmentMeta
}

const STORAGE_KEY = 'recruitment_data_v1'

function safeParseState(raw: string | null): RecruitmentState | null {
  if (!raw) return null
  try {
    const parsed = JSON.parse(raw) as Partial<RecruitmentState>
    if (!parsed || !Array.isArray(parsed.companies) || !Array.isArray(parsed.candidates) || !Array.isArray(parsed.jobs)) {
      return null
    }
    return parsed as RecruitmentState
  } catch {
    return null
  }
}

function createMockState(): RecruitmentState {
  const companies: Company[] = [
    {
      id: 1,
      name: 'SELab科技有限公司',
      industry: '软件服务',
      size: '50-200人',
      contactEmail: 'hr@se-lab.example.com',
      enabled: true,
    },
  ]

  const candidates: Candidate[] = [
    {
      id: 1001,
      name: '张三',
      phone: '13800000001',
      email: 'zhangsan@example.com',
      education: '本科',
      major: '计算机科学与技术',
      years: 3,
      resumeSummary: '熟悉 Vue 生态，具备良好的工程化能力与团队协作经验。',
      skills: ['Vue', 'TypeScript', 'Element Plus', 'Node.js'],
      enabled: true,
    },
    {
      id: 1002,
      name: '李四',
      phone: '13800000002',
      email: 'lisi@example.com',
      education: '本科',
      major: '软件工程',
      years: 2,
      resumeSummary: '注重交互体验和性能优化，参与过多轮前端重构。',
      skills: ['Vue', 'React', 'Vite', '性能优化'],
      enabled: true,
    },
  ]

  const jobs: Job[] = [
    {
      id: 101,
      title: '前端开发工程师',
      companyId: 1,
      companyName: 'SELab科技有限公司',
      location: '杭州',
      salary: '15k-25k',
      description:
        '负责产品前端架构设计与开发，参与需求评审、性能优化与交付保障。要求：熟悉 Vue/TypeScript，了解组件化与工程化。',
      tags: ['Vue', 'TypeScript', 'Element Plus'],
      status: 'open',
      auditStatus: 'approved',
      createdAt: '2026-03-01',
    },
    {
      id: 102,
      title: '后端开发工程师',
      companyId: 1,
      companyName: 'SELab科技有限公司',
      location: '杭州',
      salary: '18k-30k',
      description:
        '负责服务端 API 开发与数据建模，参与接口联调与稳定性优化。要求：熟悉 Java/Python 任一，了解数据库与缓存。',
      tags: ['API', '数据库', '缓存'],
      status: 'open',
      auditStatus: 'pending',
      createdAt: '2026-03-10',
    },
  ]

  const applications: Application[] = [
    {
      id: 5001,
      jobId: 101,
      jobTitle: '前端开发工程师',
      companyId: 1,
      companyName: 'SELab科技有限公司',
      candidateId: 1001,
      candidateName: '张三',
      appliedAt: '2026-03-15',
      status: 'reviewing',
    },
  ]

  return {
    companies,
    candidates,
    jobs,
    applications,
    meta: {
      nextCompanyId: 2,
      nextCandidateId: 1003,
      nextJobId: 103,
      nextApplicationId: 5002,
    },
  }
}

function saveState(state: RecruitmentState) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
}

export const useRecruitmentStore = defineStore('recruitment', () => {
  const initial = safeParseState(localStorage.getItem(STORAGE_KEY)) ?? createMockState()

  const companies = ref<Company[]>(initial.companies)
  const candidates = ref<Candidate[]>(initial.candidates)
  const jobs = ref<Job[]>(initial.jobs)
  const applications = ref<Application[]>(initial.applications)
  const meta = ref<RecruitmentMeta>(initial.meta)

  const approvedJobs = computed(() =>
    jobs.value.filter((j) => j.auditStatus === 'approved' && j.status === 'open'),
  )

  function persist() {
    saveState({
      companies: companies.value,
      candidates: candidates.value,
      jobs: jobs.value,
      applications: applications.value,
      meta: meta.value,
    })
  }

  function upsertCandidateByName(name: string): Candidate {
    const trimmed = name.trim()
    const hit = candidates.value.find((c) => c.name === trimmed)
    if (hit) return hit

    const id = meta.value.nextCandidateId++
    const candidate: Candidate = {
      id,
      name: trimmed,
      phone: '1380000' + String(id).slice(-4).padStart(4, '0'),
      email: `user${id}@example.com`,
      education: '本科',
      major: '',
      years: 0,
      resumeSummary: '暂无简历摘要（演示数据）。',
      skills: [],
      enabled: true,
    }
    candidates.value.push(candidate)
    persist()
    return candidate
  }

  function upsertCompanyByName(name: string): Company {
    const trimmed = name.trim()
    const hit = companies.value.find((c) => c.name === trimmed)
    if (hit) return hit

    const id = meta.value.nextCompanyId++
    const company: Company = {
      id,
      name: trimmed,
      industry: '软件服务',
      size: '1-50人',
      contactEmail: `hr${id}@example.com`,
      enabled: true,
    }
    companies.value.push(company)
    persist()
    return company
  }

  function createOrUpdateJob(payload: {
    jobId?: number
    title: string
    location: string
    salary: string
    description: string
    tags: string[]
  }): Job {
    const auth = useAuthStore()
    const companyId = auth.userId
    if (auth.role !== 'enterprise' || !companyId) {
      throw new Error('Only enterprise can manage jobs.')
    }

    const company = companies.value.find((c) => c.id === companyId)
    if (!company) throw new Error('Company not found.')

    const now = new Date().toISOString().slice(0, 10)

    if (payload.jobId) {
      const job = jobs.value.find((j) => j.id === payload.jobId)
      if (!job) throw new Error('Job not found.')
      job.title = payload.title
      job.location = payload.location
      job.salary = payload.salary
      job.description = payload.description
      job.tags = payload.tags
      job.companyName = company.name
      // 更新后需要再次审核
      job.auditStatus = 'pending'
      job.auditReason = undefined
      job.createdAt = job.createdAt || now
      persist()
      return job
    }

    const id = meta.value.nextJobId++
    const job: Job = {
      id,
      title: payload.title,
      companyId: companyId,
      companyName: company.name,
      location: payload.location,
      salary: payload.salary,
      description: payload.description,
      tags: payload.tags,
      status: 'open',
      auditStatus: 'pending',
      createdAt: now,
    }
    jobs.value.push(job)
    persist()
    return job
  }

  function adminSetJobAudit(jobId: number, auditStatus: AuditStatus, reason?: string) {
    const job = jobs.value.find((j) => j.id === jobId)
    if (!job) return
    job.auditStatus = auditStatus
    job.auditReason = reason
    if (auditStatus === 'approved') {
      job.status = 'open'
    } else if (auditStatus === 'rejected') {
      job.status = 'closed'
    }
    persist()
  }

  function applyToJob(jobId: number): { application?: Application; alreadyApplied: boolean } {
    const auth = useAuthStore()
    if (auth.role !== 'candidate' || !auth.userId) {
      return { alreadyApplied: false }
    }
    const candidateId = auth.userId
    const candidate = candidates.value.find((c) => c.id === candidateId)
    const job = jobs.value.find((j) => j.id === jobId)
    if (!candidate || !job) return { alreadyApplied: false }
    if (job.auditStatus !== 'approved' || job.status !== 'open') return { alreadyApplied: false }

    const exists = applications.value.some((a) => a.jobId === jobId && a.candidateId === candidateId)
    if (exists) return { alreadyApplied: true }

    const application: Application = {
      id: meta.value.nextApplicationId++,
      jobId: job.id,
      jobTitle: job.title,
      companyId: job.companyId,
      companyName: job.companyName,
      candidateId: candidate.id,
      candidateName: candidate.name,
      appliedAt: new Date().toISOString().slice(0, 10),
      status: 'submitted',
    }
    applications.value.push(application)
    persist()
    return { application, alreadyApplied: false }
  }

  function updateApplicationStatus(applicationId: number, status: ApplicationStatus, note?: string) {
    const app = applications.value.find((a) => a.id === applicationId)
    if (!app) return
    app.status = status
    app.note = note
    persist()
  }

  function getApplicationsByCandidate(candidateId: number) {
    return applications.value.filter((a) => a.candidateId === candidateId)
  }

  function getApplicationsByCompany(companyId: number, jobId?: number) {
    return applications.value.filter((a) => a.companyId === companyId && (!jobId || a.jobId === jobId))
  }

  function updateCandidateProfile(candidateId: number, patch: Partial<Candidate>) {
    const c = candidates.value.find((x) => x.id === candidateId)
    if (!c) return
    c.education = patch.education ?? c.education
    c.major = patch.major ?? c.major
    c.years = typeof patch.years === 'number' ? patch.years : c.years
    c.resumeSummary = patch.resumeSummary ?? c.resumeSummary
    c.skills = patch.skills ?? c.skills
    persist()
  }

  function updateCompanyInfo(companyId: number, patch: Partial<Company>) {
    const c = companies.value.find((x) => x.id === companyId)
    if (!c) return
    c.industry = patch.industry ?? c.industry
    c.size = patch.size ?? c.size
    c.contactEmail = patch.contactEmail ?? c.contactEmail
    c.enabled = typeof patch.enabled === 'boolean' ? patch.enabled : c.enabled
    persist()
  }

  function toggleCandidateEnabled(candidateId: number) {
    const c = candidates.value.find((x) => x.id === candidateId)
    if (!c) return
    c.enabled = !c.enabled
    persist()
  }

  function toggleCompanyEnabled(companyId: number) {
    const c = companies.value.find((x) => x.id === companyId)
    if (!c) return
    c.enabled = !c.enabled
    persist()
  }

  return {
    companies,
    candidates,
    jobs,
    applications,
    meta,

    approvedJobs,

    upsertCandidateByName,
    upsertCompanyByName,
    createOrUpdateJob,
    adminSetJobAudit,
    applyToJob,
    updateApplicationStatus,
    getApplicationsByCandidate,
    getApplicationsByCompany,
    updateCandidateProfile,
    updateCompanyInfo,
    toggleCandidateEnabled,
    toggleCompanyEnabled,
  }
})

