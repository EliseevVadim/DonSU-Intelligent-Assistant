<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import {useRoute, useRouter} from 'vue-router'
import ThemeToggler from "@/components/ThemeToggler.vue";

const store = useStore()
const router = useRouter()
const route = useRoute()

const new_password = ref('')
const confirmed_new_password = ref('')

const errorMessage = ref(null)
const successMessage = ref(null)
const loading = ref(false)
const valid = ref(false)

const passwordRules = [
    v => !!v || 'Поле обязательно',
    v => v.length >= 6 || 'Пароль должен быть не менее 6 символов',
]

const confirmPasswordRules = [
    v => !!v || 'Поле обязательно',
    v => v === new_password.value || 'Пароли должны совпадать',
]

const resetPassword = async () => {
    loading.value = true
    errorMessage.value = null


    try {
        let payload = {
            token: route.query.token,
            new_password: new_password.value,
            confirm_new_password: confirmed_new_password.value
        }
        store.dispatch('resetPassword', payload)
            .then(() => {
                router.push('/reset-password-success');
            })
            .catch((error) => {
                errorMessage.value = error.response.data.detail
            })
    } catch (error) {
        errorMessage.value = 'Ошибка при авторизации'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <v-container fluid class="login-container">
        <v-row justify="center" align="center" class="fill-height">
            <v-col cols="12" sm="8" md="4">
                <v-card class="login-card" elevation="10">
                    <v-card-title class="text-center text-h5">
                        <v-icon size="32" class="mr-2">mdi-account-lock</v-icon>
                        Восстановление пароля
                    </v-card-title>

                    <v-card-text class="px-4">
                        <v-form ref="form" v-model="valid" @submit.prevent="resetPassword" @keyup.enter="resetPassword">
                            <v-text-field
                                v-model="new_password"
                                label="Новый пароль"
                                type="password"
                                variant="outlined"
                                density="compact"
                                class="mt-2"
                                prepend-inner-icon="mdi-lock"
                                :rules="passwordRules"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="confirmed_new_password"
                                label="Повторите пароль"
                                type="password"
                                variant="outlined"
                                density="compact"
                                class="mt-2"
                                prepend-inner-icon="mdi-lock"
                                :rules="confirmPasswordRules"
                                required
                            ></v-text-field>
                            <v-btn color="primary" variant="elevated" block
                                   :disabled="!valid"
                                   :loading="loading" @click="resetPassword"
                                   class="text-none">
                                Восстановить пароль
                            </v-btn>
                        </v-form>
                        <v-alert v-if="errorMessage" type="error" dense class="mt-2" closable
                                 @click:close="errorMessage = null">
                            {{ errorMessage }}
                        </v-alert>
                        <v-alert v-if="successMessage" type="success" dense class="mt-2" closable
                                 @click:close="successMessage = null">
                            {{ successMessage }}
                        </v-alert>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
    <ThemeToggler/>
</template>

<style scoped>
.register-link {
    color: #1976D2;
    text-decoration: none;
    font-size: 14px;
}
.register-link:hover {
    text-decoration: underline;
}
</style>