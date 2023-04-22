import Vue, {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import moment from 'moment'

const app = createApp(App)
app.use(store).use(router).use(ElementPlus, {
    locale: zhCn,
})

app.config.globalProperties.$moment = moment;
app.mount('#app')