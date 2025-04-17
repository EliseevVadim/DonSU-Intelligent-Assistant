import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'home',
        meta: {
            title: 'Интеллектуальный ассистент ДонГУ'
        },
        component: () => import('../views/LandingPage.vue')
    },
    {
        path: '/login',
        name: 'login',
        meta: {
            title: 'Авторизация'
        },
        component: () => import('../views/LoginView.vue')
    },
    {
        path: '/register',
        name: 'register',
        meta: {
            title: 'Регистрация'
        },
        component: () => import('../views/RegistrationView.vue')
    },
    {
        path: '/external_auth',
        name: 'external-auth',
        meta: {
            title: 'Заврешение авторизации'
        },
        component: () => import('../views/ExternalAuthComplete.vue')
    },
    {
        path: '/chat',
        name: 'panel',
        meta: {
            title: 'Главная'
        },
        component: () => import('../views/user/MainPage.vue'),
        children: [
            {
                path: '',
                name: 'EmptyChat',
                component: () => import('../components/chat/EmptyChat.vue')
            },
            {
                path: ':id',
                name: 'ChatMessages',
                component: () => import('../components/chat/MessageView.vue')
            }
        ]
    }
]

const router = createRouter({
        history: createWebHistory(),
        routes
    }
)

router.beforeEach((to, from, next) => {
    document.title = to.meta.title || 'DonSU Knowledge Database Admin';
    next();
});

export default router