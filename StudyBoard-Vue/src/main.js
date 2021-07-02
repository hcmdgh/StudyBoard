import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';
import { createRouter, createWebHashHistory } from 'vue-router';

import App from './App.vue';
import Study from './components/Study.vue';
import Excerpt from './components/Excerpt.vue';
import Diary from './components/Diary.vue';
import Book from './components/Book.vue';

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: '/', component: Study },
        { path: '/study', component: Study },
        { path: '/excerpt', component: Excerpt },
        { path: '/diary', component: Diary },
        { path: '/book', component: Book },
    ],
});

const app = createApp(App);
app.use(ElementPlus);
app.use(router);
app.mount('#app');
