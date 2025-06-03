<script setup>
import { useRouter } from 'vue-router';
import ThemeToggler from "@/components/ThemeToggler.vue";

import chatExample1 from "@/assets/images/chat1.jpg";
import chatExample2 from "@/assets/images/chat2.png";
import chatExample3 from "@/assets/images/chat3.png";
import {computed} from "vue";
import store from "@/store/index.js";

const slides = [
    {
        src: chatExample1,
        alt: "Пример чата 1",
        caption: "Получите консультацию по поступлению",
    },
    {
        src: chatExample2,
        alt: "Пример чата 2",
        caption: "Официальные боты в ВК и Telegram",
    },
    {
        src: chatExample3,
        alt: "Пример чата 3",
        caption: "Управляйте чатами, хранящими собственный контекст",
    },
];


const router = useRouter();
const isAuthenticated = computed(() => store.getters.isAuthenticated);

const start = () => {
    let path = isAuthenticated.value ? '/chat' : '/login';
    router.push(path);
}
</script>

<template>
    <v-app>
        <v-container>
            <v-row align="center" justify="center" class="mb-16">
                <v-col cols="12" md="8" class="text-center">
                    <h1 class="text-h2 font-weight-bold mb-4">MyFaculty AI</h1>
                    <p class="text-h6 mb-6">
                        Ваш интеллектуальный ассистент для учёбы, общения и получения информации об университете
                        с открытым исходным кодом
                    </p>
                    <v-btn color="primary" class="me-4" size="large" @click="start">
                        Начать
                    </v-btn>
                </v-col>
            </v-row>
            <v-row align="center" justify="center" class="mb-16">
                <v-col cols="12" md="10" class="text-center">
                    <h2 class="text-h5 font-weight-medium mb-4">Что я умею?</h2>
                    <v-carousel hide-delimiters cycle show-arrows="hover">
                        <v-carousel-item v-for="(item, index) in slides" :key="index">
                            <div class="slider-image-wrapper">
                                <img :src="item.src" :alt="item.alt" class="slider-image" />
                                <div class="slider-caption">{{ item.caption }}</div>
                            </div>
                        </v-carousel-item>
                    </v-carousel>
                </v-col>
            </v-row>
            <v-row class="text-center mb-16">
                <v-col cols="12" md="4">
                    <v-icon size="56" color="primary">mdi-brain</v-icon>
                    <h3 class="text-h6 font-weight-bold mt-4">Интеллектуальные ответы</h3>
                    <p class="text-body-1">Задавайте вопросы об университете, учебе, расписании — и получайте точные ответы от ИИ.</p>
                </v-col>
                <v-col cols="12" md="4">
                    <v-icon size="56" color="primary">mdi-bots</v-icon>
                    <h3 class="text-h6 font-weight-bold mt-4">Боты в соцсетях</h3>
                    <p class="text-body-1">Подключайтесь через Telegram или VK, чтобы получать помощь прямо в мессенджере.</p>
                </v-col>
                <v-col cols="12" md="4">
                    <v-icon size="56" color="primary">mdi-code-tags</v-icon>
                    <h3 class="text-h6 font-weight-bold mt-4">Открытый код</h3>
                    <p class="text-body-1">Присоединяйтесь к развитию MyFaculty AI. Мы — open source и любим pull requests.</p>
                </v-col>
            </v-row>

            <v-row align="center" justify="center" class="mb-12">
                <v-col cols="12" md="8" class="text-center">
                    <h2 class="text-h5 font-weight-medium mb-4">Готовы попробовать?</h2>
                    <v-btn color="primary" size="large" @click="start">
                        Задать первый вопрос
                    </v-btn>
                </v-col>
            </v-row>

            <v-row justify="center" class="text-center">
                <v-col cols="12" md="8">
                    <v-divider class="mb-4" />
                    <div class="mt-1 mb-1">
                        <v-btn icon href="https://t.me/DonSU_AI_bot" target="_blank">
                            <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="40" height="40" viewBox="0 0 48 48">
                                <path fill="#29b6f6" d="M24 4A20 20 0 1 0 24 44A20 20 0 1 0 24 4Z"></path>
                                <path fill="#fff" d="M33.95,15l-3.746,19.126c0,0-0.161,0.874-1.245,0.874c-0.576,0-0.873-0.274-0.873-0.274l-8.114-6.733
                                    l-3.97-2.001l-5.095-1.355c0,0-0.907-0.262-0.907-1.012c0-0.625,0.933-0.923,0.933-0.923l21.316-8.468
                                    c-0.001-0.001,0.651-0.235,1.126-0.234C33.667,14,34,14.125,34,14.5C34,14.75,33.95,15,33.95,15z"></path>
                                <path fill="#b0bec5" d="M23,30.505l-3.426,3.374c0,0-0.149,0.115-0.348,0.12c-0.069,0.002-0.143-0.009-0.219-0.043
                                    l0.964-5.965L23,30.505z"></path>
                                <path fill="#cfd8dc" d="M29.897,18.196c-0.169-0.22-0.481-0.26-0.701-0.093L16,26c0,0,2.106,5.892,2.427,6.912
                                    c0.322,1.021,0.58,1.045,0.58,1.045l0.964-5.965l9.832-9.096C30.023,18.729,30.064,18.416,29.897,18.196z"></path>
                            </svg>
                        </v-btn>
                        <v-btn icon href="https://vk.com/im?sel=-230592555" target="_blank">
                            <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="40" height="40" viewBox="0 0 48 48">
                                <path fill="#1976d2" d="M42,37c0,2.762-2.238,5-5,5H11c-2.761,0-5-2.238-5-5V11c0-2.762,2.239-5,5-5h26c2.762,0,5,2.238,5,5
                                    V37z"></path>
                                <path fill="#fff" d="M35.937,18.041c0.046-0.151,0.068-0.291,0.062-0.416C35.984,17.263,35.735,17,35.149,17h-2.618
                                    c-0.661,0-0.966,0.4-1.144,0.801c0,0-1.632,3.359-3.513,5.574c-0.61,0.641-0.92,0.625-1.25,0.625C26.447,24,26,23.786,26,23.199
                                    v-5.185C26,17.32,25.827,17,25.268,17h-4.649C20.212,17,20,17.32,20,17.641c0,0.667,0.898,0.827,1,2.696v3.623
                                    C21,24.84,20.847,25,20.517,25c-0.89,0-2.642-3-3.815-6.932C16.448,17.294,16.194,17,15.533,17h-2.643
                                    C12.127,17,12,17.374,12,17.774c0,0.721,0.6,4.619,3.875,9.101C18.25,30.125,21.379,32,24.149,32c1.678,0,1.85-0.427,1.85-1.094
                                    v-2.972C26,27.133,26.183,27,26.717,27c0.381,0,1.158,0.25,2.658,2c1.73,2.018,2.044,3,3.036,3h2.618
                                    c0.608,0,0.957-0.255,0.971-0.75c0.003-0.126-0.015-0.267-0.056-0.424c-0.194-0.576-1.084-1.984-2.194-3.326
                                    c-0.615-0.743-1.222-1.479-1.501-1.879C32.062,25.36,31.991,25.176,32,25c0.009-0.185,0.105-0.361,0.249-0.607
                                    C32.223,24.393,35.607,19.642,35.937,18.041z"></path>
                            </svg>
                        </v-btn>
                    </div>

                    <p class="text-caption">
                        MyFaculty AI — Open Source проект.
                    </p>
                    <iframe src="https://ghbtns.com/github-btn.html?user=EliseevVadim&repo=DonSU-Intelligent-Assistant&type=star&count=true&size=large" frameborder="0" scrolling="0" width="110" height="30" title="GitHub"></iframe>
                </v-col>
            </v-row>
        </v-container>

        <ThemeToggler />
    </v-app>
</template>

<style scoped>
.text-h2 {
    font-size: 3.5rem;
}
.slider-image-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.slider-image {
    width: 100%;
    aspect-ratio: 1280 / 589;
    object-fit: cover;
    border-radius: 12px;
    display: block;
}

.slider-caption {
    margin-top: 0.75rem;
    font-size: 1rem;
    text-align: center;
}
</style>
