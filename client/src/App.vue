<script setup>
import { useTheme } from 'vuetify'
import { ref } from 'vue'

const theme = useTheme()

theme.global.name.value = localStorage.getItem('theme') ?? 'lightTheme'

const isDark = ref(theme.global.name.value === 'darkTheme')

const toggleTheme = () => {
    isDark.value = !isDark.value
    theme.global.name.value = isDark.value ? 'darkTheme' : 'lightTheme'
    localStorage.setItem('theme', theme.global.name.value)
}
</script>

<template>
    <v-app>
        <router-view />
        <v-container class="d-flex justify-end pa-4">
            <v-btn icon @click="toggleTheme" class="theme-switcher">
                <v-icon>{{ isDark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
            </v-btn>
        </v-container>
    </v-app>
</template>

<style scoped>
header {
    line-height: 1.5;
}

.theme-switcher {
    position: fixed;
    bottom: 16px;
    right: 16px;
    z-index: 1000;
    border-radius: 50%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 12px;
}

.logo {
    display: block;
    margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
    header {
        display: flex;
        place-items: center;
        padding-right: calc(var(--section-gap) / 2);
    }

    .logo {
        margin: 0 2rem 0 0;
    }

    header .wrapper {
        display: flex;
        place-items: flex-start;
        flex-wrap: wrap;
    }
}
</style>
