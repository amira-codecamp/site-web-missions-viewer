
import { createApp } from 'vue';
import BaseLayout from '@/components/BaseLayout.vue';
import router from '@/router';
import store from '@/store/index';
import 'bulma-multiselect/css/bulma-multiselect.min.css';
import 'bulma-tooltip/dist/css/bulma-tooltip.min.css';
import 'leaflet/dist/leaflet.css';


const app = createApp(BaseLayout);

app.use(router);
app.use(store);
app.mount('#app');