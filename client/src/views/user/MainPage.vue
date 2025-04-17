<script setup>
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { computed, onMounted, ref, watch } from 'vue'
import { useTheme } from 'vuetify'

import ConfirmDialog from '../../components/ConfirmDialog.vue'
import RenameDialog from '@/components/chat/RenameChatModal.vue'
import CreateButton from "@/components/chat/CreateButton.vue"
import MessageField from "@/components/chat/MessageField.vue"
import User from "@/views/user/User.vue"

const theme = useTheme()
theme.global.name.value = localStorage.getItem('theme') ?? 'light'

const store = useStore()
const router = useRouter()
const route = useRoute()

const confirmDialog = ref(null)
const renameDialog = ref(false)
const renameTarget = ref(null)

const drawer = window.innerWidth < 768 ? ref(false) : ref(true);
const message = ref("");

const chats = computed(() => store.getters.CHATS);
const isAuthenticated = computed(() => store.getters.isAuthenticated);

const fetchChats = async () => await store.dispatch('loadChats')
const fetchUserInfo = () => store.dispatch('loadUserInfo')

const fetchMessages = async (chatId) => {
    await store.dispatch('loadMessagesByChat', chatId)
}

const createNewChat = async () => {
    await router.push('/chat')
}

const renameChat = (chat) => {
    renameTarget.value = chat
    renameDialog.value = true
}

const applyRename = async (newName) => {
    await store.dispatch('renameChat', {
        'chat_id': renameTarget.value.id,
        'new_name': newName
    })
    await fetchChats()
}

const deleteChat = async (chat) => {
    await confirmDialog.value.open(
        'Подтверждение удаления чата',
        `Вы действительно хотите удалить чат: <b>${chat.name}</b>?`
    ).then(() => {
        if (route.params.id === chat.id) {
            router.push('/chat');
        }
        store.dispatch('deleteChat', chat.id).then(() => fetchChats())
    }).catch(() => {})
}

const sendMessage = async () => {
    let chatId = route.params.id;
    if (!chatId) {
        await store.dispatch('createChat')
            .then(async (response) => {
                chatId = response.data.chat_id;
                await fetchChats();
                await router.push('/chat/' + chatId);
            })
            .catch((error) => {
                console.log(error);
            })
    }
    await store.dispatch('sendMessage', {
        'chat_id': chatId,
        'text_content': message.value
    });
    await fetchMessages(chatId);
    message.value = '';
}

const openChat = async (id) => {
    await router.push(`/chat/${id}`)
}

watch(() => route.params.id, async (id) => {
    if (id) {
        await fetchMessages(id)
    }
}, { immediate: true })

onMounted(async () => {
    if (!isAuthenticated.value) {
        await router.push('/login')
        return
    }
    await fetchChats();
    await fetchUserInfo();
})

</script>

<template>
    <v-app id="inspire">
        <v-app-bar class="px-3 z" flat height="72" border>
            <v-spacer>
                <CreateButton :createNewChat="createNewChat" />
            </v-spacer>

            <v-app-bar-nav-icon
                class="d-sm-none d-block"
                variant="text"
                @click.stop="drawer = !drawer"
            ></v-app-bar-nav-icon>
            <User />
        </v-app-bar>
        <v-main>
            <router-view />
        </v-main>
        <v-navigation-drawer v-model="drawer" outline location="left" width="300">
            <v-list class="z">
                <v-list-item
                    v-for="(chat, i) in chats.values()"
                    :key="i"
                    :value="i"
                    :active="route.params.id === chat.id"
                    base-color="tonal"
                    @click.stop="openChat(chat.id)"
                    link
                    prepend-icon="mdi-message-text"
                    class="chat-list-item"
                >
                    <template v-slot:title>
                        <span class="truncate">{{ chat.name }}</span>
                    </template>

                    <template v-slot:append>
                        <v-menu
                            location="bottom end"
                            offset="4"
                        >
                            <template v-slot:activator="{ props }">
                                <v-btn
                                    icon="mdi-dots-horizontal"
                                    variant="text"
                                    v-bind="props"
                                    @click.stop
                                />
                            </template>
                            <v-list>
                                <v-list-item @click="renameChat(chat)">
                                    <v-list-item-title class="d-flex align-center">
                                        <v-icon class="mr-2">mdi-pencil</v-icon>
                                        Переименовать
                                    </v-list-item-title>
                                </v-list-item>
                                <v-list-item @click="deleteChat(chat)">
                                    <v-list-item-title class="d-flex align-center text-error">
                                        <v-icon color="error" class="mr-2">mdi-delete</v-icon>
                                        Удалить
                                    </v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-menu>
                    </template>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
        <v-footer class="z" app height="92">
            <MessageField id="footer" v-model="message" :send="sendMessage" />
        </v-footer>
        <ConfirmDialog ref="confirmDialog" />
        <RenameDialog
            v-model="renameDialog"
            :current-name="renameTarget?.name"
            @rename="applyRename"
        />
    </v-app>
</template>

<style scoped>

</style>