<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const router = useRouter();
const store = useStore();

onMounted( () => {
    const urlParams = new URLSearchParams(window.location.search);
    const accessToken = urlParams.get('access_token');
    if (accessToken) {
        try {
            store.dispatch('authenticateExternally', { access_token: accessToken });
            router.push('/chat');
        } catch (error) {
            console.error('Ошибка авторизации через Google:', error);
            router.push('/login');
        }
    } else {
        router.push('/login');
    }
});
</script>

<template>
    <v-container fluid class="d-flex align-center justify-center" style="height: 100vh;">
        <v-progress-circular indeterminate color="primary" size="50"></v-progress-circular>
    </v-container>
</template>

<style scoped>

</style>