<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import ThemeToggler from "@/components/ThemeToggler.vue";

const store = useStore()
const router = useRouter()

const email = ref('')
const errorMessage = ref(null)
const successMessage = ref(null)
const loading = ref(false)
const valid = ref(false)

const emailRules = [
    v => !!v || 'Поле обязательно',
    v => /.+@.+\..+/.test(v) || 'Введите корректный email',
]
const requestPasswordReset = async () => {
    loading.value = true
    errorMessage.value = null

    try {
        let payload = {
            email: email.value,
        }
        store.dispatch('requestPasswordReset', payload)
            .then(() => {
                router.push('/password-reset-confirmed')
            })
            .catch((error) => {
                errorMessage.value = error.response.data.detail
            })
    } catch (error) {
        errorMessage.value = 'Ошибка при запросе восстановления пароля'
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
                        Сброс пароля
                    </v-card-title>

                    <v-card-text class="px-4">
                        <v-form ref="form" v-model="valid" @submit.prevent="requestPasswordReset"
                                @keyup.enter="requestPasswordReset">
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
                            <v-btn color="primary" variant="elevated" block
                                   :disabled="!valid"
                                   :loading="loading" @click="requestPasswordReset"
                                   class="text-none">
                                Продолжить
                            </v-btn>
                            <div class="text-center mt-2">
                                <router-link to="/register" class="register-link">
                                    Нет аккаунта? Зарегистрироваться
                                </router-link>
                            </div>
                            <div class="text-center mt-2">
                                <router-link to="/login" class="register-link">
                                    Уже зарегистрированы? Войти!
                                </router-link>
                            </div>
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