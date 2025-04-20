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
        component: () => import('../views/auth/LoginView.vue')
    },
    {
        path: '/register',
        name: 'register',
        meta: {
            title: 'Регистрация'
        },
        component: () => import('../views/auth/RegistrationView.vue')
    },
    {
        path: '/external_auth',
        name: 'external-auth',
        meta: {
            title: 'Заврешение авторизации'
        },
        component: () => import('../views/auth/ExternalAuthComplete.vue')
    },
    {
        path: '/forgot-password',
        name: 'forgot-password',
        meta: {
            title: 'Восстановление пароля'
        },
        component: () => import('../views/auth/ForgotPasswordView.vue')
    },
    {
        path: '/password-reset-confirmed',
        name: 'password-reset-confirmed',
        meta: {
            title: 'Запрос на восстановление пароля подтвержден'
        },
        component: () => import('../views/auth/PasswordResetConfirmed.vue')
    },
    {
        path: '/auth/password/reset/confirm',
        name: 'change-password',
        meta: {
            title: 'Изменение пароля'
        },
        component: () => import('../views/auth/ResetPasswordView.vue')
    },
    {
        path: '/reset-password-success',
        name: 'reset-password-success',
        meta: {
            title: 'Пароль успешно изменен'
        },
        component: () => import('../views/auth/ResetPasswordSuccess.vue')
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
    document.title = to.meta.title || 'Интеллектуальный ассистент ДонГУ';
    next();
});

export default router