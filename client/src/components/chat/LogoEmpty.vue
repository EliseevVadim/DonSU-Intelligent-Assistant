<script setup>
import { useTheme } from 'vuetify'
import {computed, onMounted} from "vue";
import { useStore } from 'vuex'

const store = useStore();
const theme = useTheme();

const currentUser = computed(() => store.getters.CURRENT_USER);

onMounted(async () => {
    if (!currentUser.value) {
        await store.dispatch('loadUserInfo')
    }
})
</script>

<template>
    <div
        v-if="currentUser"
        class="welcome-text"
        :class="theme.global.current.value.dark ? 'dark' : 'light'"
    >
        {{ `Добро пожаловать, ${currentUser.first_name}` }}
    </div>
</template>

<style scoped>
.welcome-text {
    font-family: 'Pacifico', cursive;
    font-size: 48px;
    text-align: center;
    margin-top: 40px;
    margin-bottom: 20px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    -webkit-text-fill-color: transparent;
    animation: shine 6s linear infinite;
}

.welcome-text.light {
    background-image: linear-gradient(90deg, #1a73e8, #34a853, #fbbc05, #ea4335);
}

.welcome-text.dark {
    background-image: linear-gradient(90deg, #bb86fc, #03dac6, #3700b3, #03a9f4);
}

.welcome-text.light,
.welcome-text.dark {
    background-size: 200% auto;
}

@media (max-width: 600px) {
    .welcome-text {
        font-size: 32px;
        padding: 0 12px;
    }
}
</style>
