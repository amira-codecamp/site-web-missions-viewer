<template>
  <div class="columns mt-6">
    <div class="column is-6 is-offset-3">
      <form @submit.prevent="submitReset">
        <div class="field mb-4">
          <label>New Password</label>
          <div class="control">
            <input
              type="password"
              class="input"
              v-model="password"
              required
              placeholder=""
            />
          </div>
        </div>

        <div class="field mb-4">
          <label>Confirm Password</label>
          <div class="control">
            <input
              type="password"
              class="input"
              v-model="confirmPassword"
              required
              placeholder=""
            />
          </div>
        </div>

        <div class="field mb-4">
          <div class="control">
            <button class="button is-dark">Reset</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import services from '@/composables/services'

const props = defineProps({ token: String })
const router = useRouter()

const password = ref('')
const confirmPassword = ref('')
const message = ref('')
const success = ref(false)

async function submitReset() {
  message.value = ''

  if (!password.value || !confirmPassword.value) {
    alert('Fields are required.')
    return
  }

  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match.')
    return
  }

  if (!props.token) {
    alert('Token is required.')
    return
  }

  try {
    await services.users.confirmReset(props.token, password.value)
    alert('Password reset successfully!')
    router.push('/login')
  } catch (error) {
    console.error(error)
    alert('Failed to reset password.')
  }
}
</script>