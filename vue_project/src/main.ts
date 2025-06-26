// main.ts
import { createApp } from 'vue'
import BaseLayout from '@/components/BaseLayout.vue'
import router from '@/router'
import { useStore } from '@/store'

const app = createApp(BaseLayout)

const store = useStore()

app.provide('store', store)

app.use(router)
app.mount('#app')
