import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export type UserRole = 'candidate' | 'enterprise' | 'admin'

export interface AuthUser {
  id: number
  name: string
  role: UserRole
}

const STORAGE_KEY = 'recruit_auth_v1'

function safeParseAuth(raw: string | null): AuthUser | null {
  if (!raw) return null
  try {
    const parsed = JSON.parse(raw) as Partial<AuthUser>
    if (!parsed || typeof parsed.id !== 'number') return null
    if (parsed.role !== 'candidate' && parsed.role !== 'enterprise' && parsed.role !== 'admin') return null
    if (typeof parsed.name !== 'string') return null
    return { id: parsed.id, name: parsed.name, role: parsed.role }
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<AuthUser | null>(safeParseAuth(localStorage.getItem(STORAGE_KEY)))

  const isLoggedIn = computed(() => !!user.value)
  const role = computed(() => user.value?.role ?? null)
  const userId = computed(() => user.value?.id ?? null)
  const userName = computed(() => user.value?.name ?? '')

  function login(next: AuthUser) {
    user.value = next
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
  }

  function logout() {
    user.value = null
    localStorage.removeItem(STORAGE_KEY)
  }

  return {
    user,
    isLoggedIn,
    role,
    userId,
    userName,
    login,
    logout,
  }
})

