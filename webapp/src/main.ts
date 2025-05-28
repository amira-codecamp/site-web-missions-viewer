// main.ts
import { createApp } from 'vue'
import BaseLayout from '@/components/BaseLayout.vue'
import router from '@/router'
import { useStore } from '@/store'

import 'bulma-multiselect/css/bulma-multiselect.min.css'
import 'bulma-tooltip/dist/css/bulma-tooltip.min.css'
import 'leaflet/dist/leaflet.css'

const app = createApp(BaseLayout)

const store = useStore()

app.provide('store', store)

app.use(router)
app.mount('#app')
