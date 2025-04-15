<script setup>
import { useTheme } from 'vuetify'
import { ref, onMounted } from 'vue'

const theme = useTheme()
const isDark = ref(false)

onMounted(() => {
    const savedTheme = localStorage.getItem('theme') ?? 'lightTheme'
    theme.global.name.value = savedTheme
    isDark.value = savedTheme === 'darkTheme'
})

const toggleTheme = () => {
    isDark.value = !isDark.value
    theme.global.name.value = isDark.value ? 'darkTheme' : 'lightTheme'
    localStorage.setItem('theme', theme.global.name.value)
}
</script>

<template>
    <v-btn icon @click="toggleTheme" class="theme-switcher" :color="isDark ? 'black' : 'white'">
        <v-icon>{{ isDark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
    </v-btn>
</template>

<style scoped>
.theme-switcher {
    position: fixed;
    bottom: 16px;
    right: 16px;
    z-index: 1000;
    border-radius: 50%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    padding: 12px;
}
</style>