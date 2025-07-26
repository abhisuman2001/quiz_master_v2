import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // 1. Import your router
import 'bootstrap/dist/css/bootstrap.min.css' // Import Bootstrap CSS

const app = createApp(App)

app.use(router) // 2. Tell the app to use the router

app.mount('#app')