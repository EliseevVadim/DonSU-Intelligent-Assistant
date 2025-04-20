<script setup>

</script>

<template>
    <v-app>
        <router-view />
    </v-app>
</template>

<style>
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

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background-color: rgba(120, 120, 120, 0.3);
    border-radius: 999px;
    transition: background-color 0.2s ease-in-out;
}

::-webkit-scrollbar-thumb:hover {
    background-color: rgba(120, 120, 120, 0.5);
}

* {
    scrollbar-width: thin;
    scrollbar-color: rgba(120, 120, 120, 0.3) transparent;
}

.dark ::-webkit-scrollbar-thumb {
    background-color: rgba(200, 200, 200, 0.2);
}

.dark ::-webkit-scrollbar-thumb:hover {
    background-color: rgba(200, 200, 200, 0.4);
}

.dark * {
    scrollbar-color: rgba(200, 200, 200, 0.2) transparent;
}
</style>
