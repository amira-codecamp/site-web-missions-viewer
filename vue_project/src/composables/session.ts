// session.ts

import { computed } from 'vue'
import { useStore } from '@/store'
import services from '@/composables/services'

/* ============================
 * Session
 * ============================ */

/**
 * Clears the store and session data.
 */
export function logout() {
  const store = useStore()

  store.clearItem('loadedData')
  store.clearItem('loggedUser')
  store.clearItem('accessToken')
  store.clearItem('refreshToken')

  window.location.href = '/login'  // Redirect to login page
}

/**
 * Check tokens validity, if expired then logout session.
 */
export async function fetchToken(): Promise<string> {
  const store = useStore()

  try {
    const access: string = store.state.accessToken
    await services.token.verify(access)

  } catch (error: any) {
    try {
      const refresh: string = store.state.refreshToken
      await services.token.verify(refresh)

      const responsetok = await services.token.refresh(refresh)
      const access: string = responsetok.access
      store.setItem('accessToken', access)
    }
    catch (error: any) {
      alert('Session expired. Please login again.')
      logout()
      throw error
    }
  }
  return store.state.accessToken
}

/**
 * Returns the loadedData from the store.
 */
export function getData() {
  const store = useStore()
  return store.state.loadedData
}

/**
 * Updates the Data in the store.
 */
export function setData(newData: any[]) {
  const store = useStore()
  store.state.loadedData = newData
}

/* ===================
 * Role Permission Hook
 * =================== */

export function getPermission() {
  const store = useStore()

  const isAdmin = computed<boolean>(() => store.state.loggedUser.group === 'ADMIN')
  const isManager = computed<boolean>(() => store.state.loggedUser.group === 'MISSIONMANAGER')
  const isStandard = computed<boolean>(() => store.state.loggedUser.group === 'STANDARD')

  return { isAdmin, isManager, isStandard }
}