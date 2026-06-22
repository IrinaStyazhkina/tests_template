<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

import SendIcon from './icons/SendIcon.vue'
import AppButton from './AppButton.vue'
import AppInput from './AppInput.vue'
import apiClient from '@/api/api'
import AddChatModal from './AddChatModal.vue'
import { showSnackbar } from '@/stores/snackbar'
import type { Chat } from '@/types/Chat'
import type { Message } from '@/types/Message'
import { useUserStore } from '@/stores/userStore'

const message = ref('')
const chats = ref<Chat[]>([])
const currentChatId = ref<string | undefined>(undefined)
const currentMessages = ref<Message[]>([])

const userStore = useUserStore()

let isComponentAlive = true

const loadChats = async () => {
  try {
    const response = await apiClient.get('/users/chats')
    chats.value = response.data
    if (chats.value.length > 0) {
      currentChatId.value = chats.value[chats.value.length - 1]?.id
      currentMessages.value =
        chats.value.find((chat) => chat.id === currentChatId.value)?.messages ?? []
    }
  } catch (err) {
    showSnackbar('Failed to load chats')
    console.error(err)
  }
}

const updateCurrentChat = (chatId: string) => {
  currentChatId.value = chatId
  currentMessages.value = chats.value.find((chat) => chat.id === chatId)?.messages ?? []
}

const isModalOpen = ref(false)

const openModal = () => {
  isModalOpen.value = true
}

const onCloseModal = () => {
  isModalOpen.value = false
}

const addChat = async (title: string) => {
  const response = await apiClient.post('/users/chats/create', {
    title,
  })

  if (response.data) {
    loadChats()
  }
}

onMounted(() => {
  loadChats()
})

onUnmounted(() => {
  isComponentAlive = false
})

const askMl = async () => {
  const response = await apiClient.post(`/ml/predict/${currentChatId.value}`, {
    message: message.value,
  })
  const newMessage = {
    id: response.data.request_id,
    message_type: 'user',
    content: message.value,
  } as Message

  currentMessages.value.push(newMessage)

  if (response.data) {
    console.log('success')
    let messageStatus = 'processing'
    while (messageStatus !== 'processed' && isComponentAlive) {
      try {
        const finalResponse = await apiClient.get(`/ml/answer/${newMessage.id}`)
        messageStatus = finalResponse.data.message.message_status

        if (messageStatus !== 'processed') {
          await new Promise((resolve) => setTimeout(resolve, 10000))
        } else {
          currentMessages.value.push({
            id: finalResponse.data.message.id,
            content: finalResponse.data.message.content,
            message_type: finalResponse.data.message.message_type,
          })
          await userStore.loadBalance()
        }
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (e) {
        isComponentAlive = false
      }
    }
  }
}
</script>

<template>
  <div class="chat__container">
    <ul class="chat__list">
      <li
        class="chat__item"
        :class="{
          active: chat.id === currentChatId,
        }"
        v-for="chat in chats"
        :key="chat.id"
        @click="() => updateCurrentChat(chat.id)"
      >
        {{ chat.title }}
      </li>
      <li class="chat__item chat__item-button">
        <AppButton @click="openModal">Новый чат</AppButton>
      </li>
    </ul>
    <div class="chat__messages-container">
      <ul class="chat__messages">
        <li
          class="chat__message"
          :class="message.message_type === 'system' ? 'chat__message--system' : ''"
          v-for="message in currentMessages"
          :key="message.id"
        >
          {{ message.content }}
        </li>
      </ul>
      <form class="chat__input-wrapper" @submit.prevent="askMl">
        <AppInput
          v-model.trim="message"
          placeholder="Введите ваш вопрос"
          name="message"
          type="text"
        />
        <div class="chat__button-container">
          <AppButton type="submit">
            <SendIcon />
          </AppButton>
        </div>
      </form>
    </div>
  </div>
  <AddChatModal :isModalOpen="isModalOpen" :onClose="onCloseModal" v-on:addChat="addChat" />
</template>

<style scoped>
.chat__container {
  display: grid;
  grid-template-columns: 1fr 4fr;
  gap: 20px;
  height: 78vh;
}

.chat__list {
  list-style: none;
  margin: 0;
  padding: 0;
  min-width: 0;
}

.chat__item {
  display: block;
  padding: 1rem;
  cursor: pointer;
  list-style: none;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 1rem 0;
  border-radius: 8px;
  background-color: rgba(163, 177, 138, 0.5);
}

.chat__item.active {
  background-color: rgba(77, 83, 67, 0.5);
}

.chat__item-button {
  margin: 0;
  margin-top: auto;
  background: transparent;
}

.chat__messages-container {
  width: 98%;
  height: 95%;
  display: flex;
  flex-direction: column;
  background-color: rgba(200, 210, 180, 0.3);
  margin: 1rem;
  padding: 1rem;
  box-sizing: border-box;
  border-radius: 12px;
}

.chat__messages {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.chat__message {
  padding: 0.5rem 1rem;
  margin: 0.25rem;
  border-radius: 8px;
  max-width: 70%;
  word-wrap: break-word;
  background-color: rgba(163, 177, 138, 0.5);
  align-self: flex-end;
}

.chat__message--system {
  background-color: rgba(120, 140, 80, 0.9);
  color: #f4f4f4;
  align-self: flex-start;
}

.chat__input-wrapper {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  border-top: 1px solid rgba(120, 140, 80, 0.7);
}

.chat__button-container {
  margin: 1rem;
}
</style>
