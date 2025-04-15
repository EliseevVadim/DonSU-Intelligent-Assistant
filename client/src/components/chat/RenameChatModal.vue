<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
    modelValue: Boolean,
    currentName: String,
})

const emits = defineEmits(['update:modelValue', 'rename'])

const model = ref(props.modelValue)
const name = ref(props.currentName || '')

watch(() => props.modelValue, (val) => {
    model.value = val
    if (val) name.value = props.currentName || ''
})

watch(model, (val) => emits('update:modelValue', val))

function close() {
    model.value = false
}

function submit() {
    if (name.value.trim()) {
        emits('rename', name.value.trim())
        model.value = false
    }
}
</script>

<template>
    <v-dialog v-model="model" max-width="400">
        <v-card>
            <v-card-title class="text-h6">Переименовать чат</v-card-title>
            <v-card-text>
                <v-text-field
                    v-model="name"
                    label="Новое имя чата"
                    autofocus
                    @keyup.enter="submit"
                />
            </v-card-text>
            <v-card-actions>
                <v-spacer />
                <v-btn text @click="close">Отмена</v-btn>
                <v-btn color="primary" @click="submit">Сохранить</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<style scoped>

</style>