import { createApp } from 'vue'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import router from './router'
import store from "./store";

import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

// Components
import App from './App.vue'

const lightTheme = {
    dark: false,
    colors: {
        background: '#FFFFFF',
        surface: '#F5F5F5',
        primary: '#1976D2',
        secondary: '#424242',
        accent: '#82B1FF',
        error: '#FF5252',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FB8C00',
    },
}

const darkTheme = {
    dark: true,
    colors: {
        background: '#121212',
        surface: '#1E1E1E',
        primary: '#BB86FC',
        secondary: '#03DAC6',
        accent: '#FF4081',
        error: '#CF6679',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FB8C00',
    },
}


const vuetify = createVuetify({
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: { mdi },
    },
    theme: {
        defaultTheme: 'darkTheme',
        themes: {
            lightTheme,
            darkTheme,
        },
    },
    components,
    directives,
})

createApp(App)
    .use(vuetify)
    .use(router)
    .use(store)
    .mount('#app')