<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<template>
    <v-app>
        <v-container class="fill-height d-flex flex-column justify-center align-center text-center">
            <v-card class="elevation-12 pa-8 rounded-lg" max-width="500">
                <h1 class="text-h4 font-weight-bold mb-4">Добро пожаловать!</h1>
                <p class="text-body-1 mb-6">Интеллектуальный ассистент университета</p>
                <v-btn block color="primary" class="mb-4" @click="router.push('/login')">Войти</v-btn>
                <v-btn block color="secondary" outlined @click="router.push('/register')">Зарегистрироваться</v-btn>
            </v-card>
        </v-container>
    </v-app>
</template>

<style scoped>

</style>