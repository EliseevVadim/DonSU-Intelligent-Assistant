<script setup>
import LogoEmpty from "./LogoEmpty.vue";
import {computed} from "vue";

import { useTheme } from 'vuetify'

const { current } = useTheme()
const isDark = computed(() => current.value.dark);

</script>

<template>
    <v-container class="justify-space-between container">
        <LogoEmpty class="mt-14" />

        <v-row class="justify-center mt-8">
            <v-col cols="12" md="8">
                <div
                    class="info-box"
                    :class="{ 'dark-mode': isDark }"
                >
                    🤖 Этот ИИ-ассистент создан для помощи студентам и абитуриентам Донецкого государственного университета.
                    <br /><br />
                    ⚠️ Пожалуйста, учитывайте, что ответы могут содержать неточности. Всегда перепроверяйте важную информацию, особенно связанную с расписанием, приёмной комиссией, учебными документами и нормативными актами.
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>


<style scoped>
.info-box {
    background-color: #f5f5f5;
    border-left: 5px solid #1976d2;
    padding: 24px;
    font-size: 18px;
    color: #333;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    line-height: 1.6;
    transition: background-color 0.3s, color 0.3s;
}

.info-box.dark-mode {
    background-color: #1e1e1e;
    color: #eee;
    border-left-color: #90caf9;
}

@media (max-width: 600px) {
    .info-box {
        font-size: 16px;
        padding: 16px;
    }
}
</style>

