
import { createApp } from 'vue';
import BaseLayout from '@/components/BaseLayout.vue';
import router from '@/router';
import store from '@/store/index';


const app = createApp(BaseLayout);

app.use(router);
app.use(store);
app.mount('#app');