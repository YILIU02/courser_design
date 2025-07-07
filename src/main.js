import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate' 
import { useMainDataStore } from './stores'
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate)
const app = createApp(App)
app.use(pinia)
app.use(router)
const store=useMainDataStore()
const List=['/','/loginMain','/registerSub','/registerContent','/404']
function isRoute(to) {
  let res=List.filter(v=>v==to.path)
  return res.length || localStorage.getItem('token').length
}
router.beforeEach((to,from) => {
  if (!isRoute(to)) {
    return {name:'404'}
  }

});
app.use(ElementPlus)
app.mount('#app')
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
};//注册所有图标