import { reactive, computed } from 'vue'

interface State {
  loggedUser: any
  accessToken: string
  refreshToken: string
  loadedData: Record<string, any>
}

// --- Local Storage Utilities ---
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
  localStorage.setItem(
    key,
    typeof value === 'object' && value !== null
      ? JSON.stringify(value)
      : String(value)
  )
}

function storageRemove(key: string): void {
  localStorage.removeItem(key)
}

// --- Reactive State ---
const state = reactive<State>({
  loggedUser: storageGet<any>('loggedUser', {}),
  accessToken: storageGet<string>('accessToken', ''),
  refreshToken: storageGet<string>('refreshToken', ''),
  loadedData: storageGet<Record<string, any>>('loadedData', {}),
})

// --- Set a value in state and localStorage ---
function setItem<K extends keyof State>(key: K, value: State[K]) {
  state[key] = value
  if (value === null || value === undefined || value === '') {
    storageRemove(key)
  } else {
    storageSet(key, value)
  }
}

// --- Reset a specific state item to its default ---
function clearItem<K extends keyof State>(key: K) {
  const defaultValues: Partial<State> = {
    loggedUser: {},
    accessToken: '',
    refreshToken: '',
    loadedData: {},
  }

  const defaultValue = defaultValues[key] as State[K]
  setItem(key, defaultValue)
}

// --- Authentication Status ---
const isAuthenticated = computed(() => !!state.loggedUser.user_id)

export function useStore() {
  return {
    state,
    setItem,
    clearItem,
    isAuthenticated,
  }
}