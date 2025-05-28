<script setup>
import {computed, onMounted, ref} from 'vue'
import { useRouter } from 'vue-router'
import User from "@/views/user/User.vue";
import store from "@/store/index.js";
import {useTheme} from "vuetify";
import notify from "@/utils/notify.js";

const router = useRouter()

const theme = useTheme()
theme.global.name.value = localStorage.getItem('theme') ?? 'light'

const dialog = ref(false)
const formRef = ref(null)
const isFormValid = ref(false)
const appCreated = ref(false)

const editDialog = ref(false)
const editFormValid = ref(false)
const editFormRef = ref()
let editForm = ref({
    app_key: null,
    name: '',
    description: ''
})

const editingAppKey = ref(null)

const responseMessage = ref('')
const responseData = ref({ app_key: '', api_key: '' })

let form = ref({
    name: null,
    description: '',
    auth_provider_name: null
})

const apps = computed(() => store.getters.APPS);
const isAuthenticated = computed(() => store.getters.isAuthenticated);

const createApp = () => {
    dialog.value = true;
}

const openEditDialog = (app) => {
    editForm.value = { ...app }
    editDialog.value = true
}

const closeAddingModal = () => {
    form = ref({
        name: null,
        description: '',
        auth_provider_name: null
    })
    dialog.value = false;
    appCreated.value = false;
    responseMessage.value = '';
    responseData.value = { app_key: '', api_key: '' };
}

const closeEditingModal = () => {
    editForm = ref({
        name: '',
        description: '',
        auth_provider_name: ''
    })
    editDialog.value = false;
    editingAppKey.value = null;
}

const onDialogToggle = (val) => {
    dialog.value = val
    if (!val)
        closeAddingModal()
}

const onEditDialogToggle = (val) => {
    if (!val)
        closeEditingModal()
}

const submitApp = async () => {
    isFormValid.value = await formRef.value.validate()
    if (!isFormValid.value.valid) return
    await store.dispatch('createApp', form.value)
        .then(async (response) => {
            responseMessage.value = response.data.message;
            responseData.value = {
                app_key: response.data.app_key,
                api_key: response.data.api_key
            }
            await fetchApps();
            appCreated.value = true;
        })
        .catch(() => {
            notify.error('Ошибка создания приложения', 'Введенные Вами данные некорректны');
        })
}

const editApp = async () => {
    editFormValid.value = await editFormRef.value.validate()
    if (!editFormValid.value.valid) return
    editForm.value.app_key = editingAppKey.value
    await store.dispatch('updateApp', editForm.value)
        .then(async (response) => {
            notify.success('Успех', response.data.message);
            await fetchApps();
            closeEditingModal();
        })
        .catch(() => {
            notify.error('Ошибка создания приложения', 'Введенные Вами данные некорректны');
        })
}


const goBackToChats = () => {
    router.push('/chat')
}

const copyToClipboard = async (value) => {
    try {
        await navigator.clipboard.writeText(value)
        notify.success('Скопировано!')
    } catch (e) {
        notify.error('Не удалось скопировать')
    }
}

const fetchApps = async () => await store.dispatch('loadApps')
const fetchUserInfo = () => store.dispatch('loadUserInfo')

onMounted(async () => {
    if (!isAuthenticated.value) {
        await router.push('/login')
        return
    }
    await fetchApps();
    await fetchUserInfo();
})
</script>

<template>
    <v-app-bar class="px-3 z" flat height="72" border>
        <v-spacer>
            <v-btn
                @click="goBackToChats"
                variant="outlined"
                prepend-icon="mdi-arrow-left"
                class="me-3"
            >
                Назад к чатам
            </v-btn>
        </v-spacer>
        <User />
    </v-app-bar>
    <div class="apps-page px-5 w-100">
        <div class="d-flex justify-space-between align-center mb-6">
            <h1 class="text-h5 font-weight-medium">Приложения</h1>
            <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="createApp"
            >
                Создать
            </v-btn>
        </div>

        <v-row dense align="stretch" justify="start">
            <v-col
                v-for="app in apps"
                :key="app.app_key"
                cols="12"
                sm="6"
                md="4"
                lg="3"
            >
                <v-card class="app-card d-flex flex-column" elevation="2" style="height: 100%;">
                    <v-card-title class="d-flex justify-space-between align-center">
                        <span class="text-subtitle-1 font-weight-bold">{{ app.name }}</span>
                    </v-card-title>

                    <v-card-text class="flex-grow-1">
                        <v-list density="compact" class="pa-0">
                            <v-list-item>
                                <v-list-item-title class="text-subtitle-1">Описание:</v-list-item-title>
                                <v-list-item-subtitle
                                    class="text-body-1"
                                    style="white-space: pre-wrap; overflow: visible; display: block;"
                                >
                                    {{ app.description ?? 'Нет описания' }}
                                </v-list-item-subtitle>
                            </v-list-item>
                            <v-divider class="my-1" />
                            <v-list-item>
                                <v-list-item-title class="text-subtitle-1">Имя провайдера авторизации:</v-list-item-title>
                                <v-list-item-subtitle class="text-body-1">{{ app.auth_provider_name }}</v-list-item-subtitle>
                            </v-list-item>
                            <v-divider class="my-1" />
                            <v-list-item>
                                <v-list-item-title class="text-subtitle-2">Зарегистрировалось пользователей:</v-list-item-title>
                                <v-list-item-subtitle class="text-body-1">{{ app.users_count }}</v-list-item-subtitle>
                            </v-list-item>
                        </v-list>
                    </v-card-text>

                    <v-card-actions class="justify-start">
                        <v-btn
                            variant="outlined"
                            @click="openEditDialog(app)"
                            prepend-icon="mdi-pencil"
                        >
                            Редактировать
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>

        <v-alert
            v-if="apps.length === 0"
            type="info"
            text="У вас пока нет приложений. Нажмите 'Создать', чтобы начать."
            border="start"
            color="primary"
            variant="tonal"
        />
    </div>
    <v-dialog v-model="dialog" max-width="500" @update:modelValue="onDialogToggle">
        <v-card>
            <v-card-title class="text-h6 font-weight-bold">
                {{ appCreated ? 'Приложение успешно создано' : 'Создание приложения' }}
            </v-card-title>

            <v-card-text>
                <template v-if="!appCreated">
                    <v-form ref="formRef" @submit.prevent="submitApp">
                        <v-text-field
                            v-model="form.name"
                            label="Название"
                            :rules="[v => !!v || 'Обязательное поле', v => v.length >= 5 || 'Минимум 5 символов']"
                            required
                        />
                        <v-text-field
                            v-model="form.auth_provider_name"
                            label="Провайдер авторизации"
                            :rules="[v => !!v || 'Обязательное поле', v => v.length >= 2 || 'Минимум 2 символа']"
                            required
                        />
                        <v-textarea
                            v-model="form.description"
                            label="Описание (необязательно)"
                            rows="3"
                        />
                    </v-form>
                </template>

                <template v-else>
                    <v-alert type="success" variant="tonal" class="mb-4">
                        {{ responseMessage }}
                    </v-alert>

                    <v-btn
                        class="mb-2"
                        color="primary"
                        prepend-icon="mdi-key"
                        @click="copyToClipboard(responseData.app_key)"
                        block
                    >
                        Скопировать app_key
                    </v-btn>

                    <v-btn
                        color="primary"
                        prepend-icon="mdi-key-chain"
                        @click="copyToClipboard(responseData.api_key)"
                        block
                    >
                        Скопировать api_key
                    </v-btn>
                </template>
            </v-card-text>

            <v-card-actions v-if="!appCreated">
                <v-spacer />
                <v-btn @click="closeAddingModal">Отмена</v-btn>
                <v-btn color="primary" @click="submitApp">Создать</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <v-dialog
        v-model="editDialog"
        max-width="500"
        @update:modelValue="onEditDialogToggle"
    >
        <v-card>
            <v-card-title class="text-h6 font-weight-medium">
                Редактирование приложения
            </v-card-title>
            <v-card-text>
                <v-form ref="editFormRef" v-model="editFormValid" @submit.prevent="editApp">
                    <v-text-field
                        v-model="editingAppKey"
                        label="Ключ приложения"
                        :rules="[v => !!v || 'Обязательное поле']"
                        required
                    />
                    <v-text-field
                        v-model="editForm.name"
                        label="Название"
                        :rules="[v => !!v || 'Обязательное поле', v => v.length >= 5 || 'Минимум 5 символов']"
                        required
                    />
                    <v-textarea
                        v-model="editForm.description"
                        label="Описание (необязательно)"
                        rows="3"
                    />
                </v-form>
            </v-card-text>
            <v-card-actions class="justify-end">
                <v-btn @click="closeEditingModal">Отмена</v-btn>
                <v-btn color="primary" @click="editApp">Сохранить</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<style scoped>
.apps-page {
    margin-top: 88px;
}

.app-card {
    transition: box-shadow 0.2s;
}
.app-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
</style>