<script setup>
import { computed } from "vue";
import { useStore } from "vuex";
import { useTheme } from "vuetify";
import {useRouter} from "vue-router";

const store = useStore();
const router = useRouter();
const theme = useTheme();

const currentUser = computed(() => store.getters.CURRENT_USER);
const isDark = computed(() => theme.global.name.value === 'dark');

const toggleTheme = () => {
    theme.global.name.value = isDark.value ? 'light' : 'dark';
};

const logout = async () => {
    store.dispatch('logout')
        .then(() => {
            router.push('/login')
        })
}
</script>

<template>
    <v-menu
        min-width="270px"
        :close-on-content-click="false"
    >
        <template v-slot:activator="{ props }">
            <v-btn v-bind="props" class="d-flex align-center" variant="text">
                <v-avatar size="35" class="me-2">
                    <v-icon>
                        {{ currentUser ? 'mdi-account-check' : 'mdi-account-circle' }}
                    </v-icon>
                </v-avatar>
                <div v-if="currentUser" class="text-body-2 font-weight-medium">
                    {{ currentUser.first_name }} {{ currentUser.last_name }}
                </div>
                <div v-else class="text-body-2 font-italic">Гость</div>
            </v-btn>
        </template>

        <v-card>
            <v-card-title class="bg-black text-caption">⚙️ Настройки</v-card-title>
            <v-card-text class="py-3">
                <div class="d-flex align-center justify-space-between mb-4">
                    <span class="text-subtitle-2 mr-6">Тёмная тема</span>
                    <v-switch
                        hide-details
                        :model-value="isDark"
                        @change="toggleTheme"
                        inset
                        color="primary"
                        track-color="grey lighten-1"
                        class="theme-switch"
                    >
                        <template #thumb>
                            <v-icon size="18">
                                {{ isDark ? 'mdi-weather-night' : 'mdi-white-balance-sunny' }}
                            </v-icon>
                        </template>
                    </v-switch>
                </div>

                <v-divider class="my-3" />

                <v-btn
                    @click="logout"
                    color="red"
                    variant="text"
                    prepend-icon="mdi-logout"
                    block
                >
                    Выйти
                </v-btn>
            </v-card-text>
        </v-card>
    </v-menu>
</template>

<style scoped>

.theme-switch {
    --v-theme-switch-track-size: 38px;
    --v-theme-switch-thumb-size: 24px;
    --v-theme-switch-track-opacity: 0.6;
    --v-theme-switch-track-color: #9e9e9e;
    --v-theme-switch-track-color-checked: #6200ea;
    --v-theme-switch-thumb-color: white;
    --v-theme-switch-thumb-color-checked: #bb86fc;
    transition: all 0.3s ease-in-out;
}

.theme-switch:hover {
    opacity: 1;
    transform: scale(1.02);
}
</style>