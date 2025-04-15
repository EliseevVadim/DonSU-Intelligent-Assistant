<script setup>

</script>

<template>
    <v-app>
        <router-view />
    </v-app>
</template>

<style scoped>
header {
    line-height: 1.5;
}

@media (min-width: 1024px) {
    header {
        display: flex;
        place-items: center;
        padding-right: calc(var(--section-gap) / 2);
    }
}
</style>
