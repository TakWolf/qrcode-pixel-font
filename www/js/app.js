import { createApp } from './vue.esm-browser.prod.js'

createApp({
    data() {
        return {
            input: '你好，世界！',
        }
    },
}).mount('#app')
