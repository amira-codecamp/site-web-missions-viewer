// src/session.ts
import { useStore } from '@/store'
import services from '@/services'

/**
 * Clears the store and session data.
 */
export function logout() {
  const store = useStore()

  store.clearItem('trips')
  store.clearItem('employees')
  store.clearItem('transports')
  store.clearItem('missions')
  store.clearItem('users')
  store.clearItem('groups')
  store.clearItem('status')
  store.clearItem('isManager')
  store.clearItem('isAdmin')
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
    const refresh: string = store.state.refreshToken

    const responsetok = await services.auth.refresh(refresh)
    const access: string = responsetok.access
    store.setItem('accessToken', access)
    return access

  } catch (error: any) {
    alert('Session expired. Please login again.')
    
    logout()  // call logout
    
    throw error
  }
}