<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import SocialAuth from "@/components/SocialAuth.vue";

const store = useStore()
const router = useRouter()

const first_name = ref('')
const last_name = ref('')
const email = ref('')
const password = ref('')
const confirm_password = ref('')
const errorMessage = ref(null)
const successMessage = ref(null)
const loading = ref(false)
const valid = ref(false)

const emailRules = [
    v => !!v || 'Поле обязательно',
    v => /.+@.+\..+/.test(v) || 'Введите корректный email',
]

const passwordRules = [
    v => !!v || 'Поле обязательно',
    v => v.length >= 6 || 'Пароль должен быть не менее 6 символов',
]

const confirmPasswordRules = [
    v => !!v || 'Поле обязательно',
    v => v === password.value || 'Пароли должны совпадать',
]

const commonRules = [
    v => !!v || 'Поле обязательно'
]

const register = async () => {
    loading.value = true
    errorMessage.value = null

    try {
        let payload = {
            first_name: first_name.value,
            last_name: last_name.value,
            email: email.value,
            password: password.value
        }
        store.dispatch('register', payload)
            .then(() => {
                successMessage.value = 'Регистрация прошла успешно! Сейчас вы будете перенаправлены...'
                setTimeout(() => {
                    router.push('/login')
                }, 2000)
            })
            .catch((error) => {
                errorMessage.value = error.response.data.detail
            })
    } catch (error) {
        errorMessage.value = 'Ошибка при регистрации'
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
                        Регистрация
                    </v-card-title>
                    <v-card-text class="px-4">
                        <v-form ref="form" v-model="valid" @submit.prevent="register">
                            <v-text-field
                                v-model="first_name"
                                label="Имя"
                                type="text"
                                variant="outlined"
                                density="compact"
                                class="mt-2"
                                prepend-inner-icon="mdi-account"
                                :rules="commonRules"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="last_name"
                                label="Фамилия"
                                type="text"
                                variant="outlined"
                                density="compact"
                                class="mt-2"
                                prepend-inner-icon="mdi-account"
                                :rules="commonRules"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="email"
                                label="Email"
                                type="email"
                                variant="outlined"
                                density="compact"
                                class="mt-2"
                                prepend-inner-icon="mdi-email"
                                :rules="emailRules"
                                required
                            ></v-text-field>

                            <v-text-field
                                v-model="password"
                                label="Пароль"
                                type="password"
                                variant="outlined"
                                density="compact"
                                class="mt-2"
                                prepend-inner-icon="mdi-lock"
                                :rules="passwordRules"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="confirm_password"
                                label="Подтвердите пароль"
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
                                   :loading="loading" @click="register"
                                   class="text-none">
                                Зарегистрироваться
                            </v-btn>
                            <div class="text-center mt-2">
                                <router-link to="/login" class="register-link">
                                    Уже зарегистрированы? Войти
                                </router-link>
                            </div>
                            <SocialAuth/>
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
