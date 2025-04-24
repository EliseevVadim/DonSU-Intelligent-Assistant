<script setup>
import { computed, onMounted, ref, watch, nextTick } from 'vue'
import { useTheme } from 'vuetify'
import { useStore } from "vuex"

const store = useStore()
const theme = useTheme()

const container = ref(null);
const messages = computed(() => store.getters.MESSAGES);
const isTyping = computed(() => store.getters.IS_TYPING);

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
        <div v-if="isTyping" class="chat-message ai-message">
            <div class="message-meta">
                <span class="sender typing-avatar">
                    <v-progress-circular
                        indeterminate
                        color="primary"
                        size="36"
                        width="2"
                        class="typing-spinner"
                    />
                    <v-icon size="18" class="robot-icon">mdi-robot</v-icon>
                    Ассистент
                </span>
            </div>
            <br>
            <div class="message-content typing-indicator">
                <span class="text">Печатает<span class="dot-loader"><span>.</span><span>.</span><span>.</span></span></span>
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
    max-height: 75vh;
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
    background-color: #e8f0fe;
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
    background-color: #7c3aed;
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

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
}

.dot-loader span {
    animation: blink 1.4s infinite both;
    font-weight: bold;
}

.dot-loader span:nth-child(2) {
    animation-delay: 0.2s;
}
.dot-loader span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes blink {
    0% {
        opacity: 0.2;
    }
    20% {
        opacity: 1;
    }
    100% {
        opacity: 0.2;
    }
}

.typing-avatar {
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.typing-spinner {
    position: absolute;
    top: -8px;
    left: -8px;
    z-index: 0;
}

.robot-icon {
    z-index: 1;
    background-color: white;
    border-radius: 50%;
    padding: 2px;
}
.dark .robot-icon {
    background-color: #1e1e1e;
}
</style>