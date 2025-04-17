<script setup>
import { computed, onMounted, ref, watch, nextTick } from 'vue'
import { useTheme } from 'vuetify'
import { useRoute } from "vue-router"
import { useStore } from "vuex"

const route = useRoute()
const store = useStore()
const theme = useTheme()

const container = ref(null)
const messages = computed(() => store.getters.MESSAGES)

const senderMap = {
    'ai': 'Ассистент',
    'human': 'Вы'
}

const scrollToBottom = () => {
    nextTick(() => {
        if (container.value) {
            container.value.scrollTop = container.value.scrollHeight
        }
    })
}

onMounted(async () => {
    const chatId = route.params.id
    await store.dispatch('loadMessagesByChat', chatId)
    scrollToBottom()
})

watch(messages, scrollToBottom, { deep: true })
</script>

<template>
    <div
        ref="container"
        class="chat-container"
        :class="{ dark: theme.global.name.value === 'dark' }"
    >
        <div
            v-for="item in messages"
            :key="item.id"
            class="chat-message"
            :class="item.sender === 'AI' ? 'ai-message' : 'user-message'"
        >
            <div class="message-meta">
        <span class="sender">
          <v-icon size="18" class="me-1">
            {{ item.sender === 'AI' ? 'mdi-robot' : 'mdi-account' }}
          </v-icon>
          {{ senderMap[item.sender.toLocaleLowerCase()] }}
        </span>
                <span class="timestamp">
          {{ new Date(item.created_at).toLocaleTimeString() }}
        </span>
            </div>

            <div class="message-content">
                <template v-if="item.text_content.includes('```')">
                    <template v-for="(line, index) in item.text_content.split('`')" :key="line + index">
                        <template v-if="line.trim() !== ''">
                            <template v-if="index % 2 === 0">{{ line }}</template>
                            <template v-else>
                                <div class="code-block">{{ line }}</div>
                            </template>
                        </template>
                    </template>
                </template>

                <template v-else-if="item.sender === 'AI' && item.text_content.startsWith('Ошибка')">
                    <div class="code-block error">
                        {{ item.text_content }}
                    </div>
                </template>

                <template v-else>
                    <div class="text">{{ item.text_content }}</div>
                </template>
            </div>
        </div>
    </div>
</template>




<style scoped>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 16px;
    max-height: 80vh;
    overflow-y: auto;
    transition: background-color 0.3s ease;
}

.chat-message {
    display: flex;
    flex-direction: column;
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 16px;
    word-break: break-word;
    white-space: pre-wrap;
    font-size: 15px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
    transition: background-color 0.3s ease, color 0.3s ease;
}

.ai-message {
    align-self: flex-start;
    background-color: #e8f0fe; /* мягкий голубой */
    color: #1a1a1a;
}

.user-message {
    align-self: flex-end;
    background-color: #1976d2;
    color: white;
}

.dark .ai-message {
    background-color: #2a2e3b;
    color: #e2e8f0;
}

.dark .user-message {
    background-color: #7c3aed; /* сиреневый */
    color: white;
}

.message-meta {
    font-size: 12px;
    margin-bottom: 4px;
    opacity: 0.7;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
}

.message-meta .sender {
    display: flex;
    align-items: center;
    flex-shrink: 0;
}

/* Контент */
.message-content {
    display: flex;
    flex-direction: column;
}

.code-block {
    background-color: #1e1e1e;
    color: #f8f8f2;
    font-family: "Fira Code", monospace;
    padding: 12px;
    border-radius: 8px;
    margin-top: 8px;
    overflow-x: auto;
    font-size: 14px;
}

.code-block.error {
    color: #ff6b6b;
}

.text {
    white-space: pre-wrap;
}
</style>