// main.ts
import { createApp } from 'vue'
import Layout from '@/components/Layout.vue'
import router from '@/router'
import { useStore } from '@/store'

const app = createApp(Layout)

const store = useStore()

app.provide('store', store)

app.use(router)
app.mount('#app')