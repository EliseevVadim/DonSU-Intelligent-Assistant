<template>
    <v-dialog v-model="isVisible" max-width="400px">
        <v-card>
            <v-card-title>{{ title }}</v-card-title>
            <v-card-text v-html="message"></v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="cancel">Отмена</v-btn>
                <v-btn color="grey" @click="confirm">OK</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { ref } from 'vue'

const isVisible = ref(false)
const title = ref('')
const message = ref('')
let resolveFn, rejectFn

const open = (dialogTitle, dialogMessage) => {
    title.value = dialogTitle
    message.value = dialogMessage
    isVisible.value = true

    return new Promise((resolve, reject) => {
        resolveFn = resolve
        rejectFn = reject
    })
}

const confirm = () => {
    resolveFn()
    isVisible.value = false
}

const cancel = () => {
    rejectFn()
    isVisible.value = false
}

defineExpose({open})
</script>
