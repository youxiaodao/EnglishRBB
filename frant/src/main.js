import Vue from 'vue'
import App from './App.vue'
import ViewUI from 'view-design'
import 'view-design/dist/styles/iview.css';
import VueResource from 'vue-resource'

Vue.use(ViewUI);
Vue.use(VueResource)
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
