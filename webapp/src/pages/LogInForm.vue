<template>
  <div class="columns">
    <div class="column is-6 is-offset-3">
      <form @submit.prevent="submitForm">
        <div class="field mb-4">
          <label>Login</label>
          <div class="control">
            <input
              type="text"
              class="input"
              v-model="login"
              required
              maxlength="50"
              placeholder="Enter your login"
            />
          </div>
        </div>

        <div class="field mb-4">
          <label>Password</label>
          <div class="control">
            <input
              type="password"
              class="input"
              v-model="password"
              required
              placeholder="Enter your password"
            />
          </div>
        </div>

        <div class="notification is-danger mb-4" v-if="errors.length">
          <p v-for="error in errors" :key="error">{{ error }}</p>
        </div>

        <div class="field mb-4">
          <div class="control">
            <button class="button is-dark">Log In</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: 'LogInForm',
})

import { ref, onMounted } from 'vue'
import authservice from '@/services/authservice'
import { useStore } from '@/store'
import { useRouter } from 'vue-router'

const login = ref('')
const password = ref('')
const errors = ref<string[]>([])

const store = useStore()
const router = useRouter()

onMounted(() => {
  document.title = 'Log In | LIPN-carbon'
})

async function submitForm() {
  errors.value = []

  if (!login.value || !password.value) {
    errors.value.push('Both login and password are required.')
    return
  }

  try {
    const credentials = { login: login.value, password: password.value }

    store.setItem('user', login.value)

    const { access, refresh } = await authservice.login(credentials)

    store.setItem('accessToken', access)
    store.setItem('refreshToken', refresh)

    router.push('/member')
  } catch (error: any) {
    if (error.response && error.response.data) {
      for (const property in error.response.data) {
        errors.value.push(`${property}: ${error.response.data[property]}`)
      }
    } else {
      errors.value.push('Something went wrong. Please try again')
    }
    console.error(error)
  }
}
</script>