<script setup>

import ThemeToggler from "@/components/ThemeToggler.vue";
</script>

<template>
    <div class="reset-confirmation">
        <v-card class="reset-card" elevation="10">
            <v-card-title class="reset-title text-h6 text-center">
                Пароль был успешно восстановлен
            </v-card-title>
            <v-card-text class="text-body-1 text-center">
                Для входа в приложение авторизуйтесь с новым паролем, нажав кнопку ниже.
            </v-card-text>
            <v-card-actions class="justify-center">
                <v-btn color="primary" to="/login">Авторизоваться</v-btn>
            </v-card-actions>
        </v-card>
    </div>
    <ThemeToggler/>
</template>

<style scoped>
.reset-title {
    white-space: normal;
    word-break: break-word;
    overflow-wrap: break-word;
}

.reset-confirmation {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    padding: 16px;
}

.reset-card {
    word-break: break-all;
    text-overflow: ellipsis;
    width: 100%;
    max-width: 500px;
    padding: 24px;
}
</style>