import { createApp } from "vue"
import { createPinia } from "pinia"
import piniaPluginPersistedstate from "pinia-plugin-persistedstate"
import router from "./router"
import App from "./App.vue"
import "./style.css"
import "highlight.js/styles/github-dark.css"

// 创建Pinia实例
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// 创建Vue应用
const app = createApp(App)

app.use(pinia)
app.use(router)

app.mount("#app")
