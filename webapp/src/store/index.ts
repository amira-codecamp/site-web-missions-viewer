
import { reactive, computed } from 'vue'

interface State {
  user: string
  accessToken: string
  refreshToken: string
  isManager: boolean
  trips: any[]
  missions: any[]
  transports: any[]
  employees: any[]
}

function storageGet<T>(key: string, defaultValue: T): T {
  const val = localStorage.getItem(key)
  if (val === null) return defaultValue
  try {
    return JSON.parse(val) as T
  } catch {
    return val as unknown as T
  }
}

function storageSet(key: string, value: unknown): void {
  if (typeof value === 'object' && value !== null) {
    localStorage.setItem(key, JSON.stringify(value))
  } else {
    localStorage.setItem(key, String(value))
  }
}

function storageRemove(key: string): void {
  localStorage.removeItem(key)
}

const state = reactive<State>({
  user: storageGet<string>('user', ''),
  accessToken: storageGet<string>('accessToken', ''),
  refreshToken: storageGet<string>('refreshToken', ''),
  isManager: storageGet<boolean>('isManager', false),
  trips: storageGet<any[]>('trips', []),
  missions: storageGet<any[]>('missions', []),
  transports: storageGet<any[]>('transports', []),
  employees: storageGet<any[]>('employees', []),
})

function setItem<K extends keyof State>(key: K, value: State[K]) {
  state[key] = value
  if (value === null || value === undefined || value === '') {
    storageRemove(key)
  } else {
    storageSet(key, value)
  }
}

function clearItem<K extends keyof State>(key: K) {
  const defaultValues: Record<string, any> = {
    trips: [],
    employees: [],
    transports: [],
    missions: [],
    isManager: false,
    user: null,
    accessToken: null,
    refreshToken: null,
  };

  const defaultValue = defaultValues[key as keyof typeof defaultValues] || null;

  setItem(key, defaultValue);
  storageRemove(key);
}

const isAuthenticated = computed(() => !!state.user && !!state.accessToken)

export function useStore() {
  return {
    state,
    setItem,
    clearItem,
    isAuthenticated,
  }
}