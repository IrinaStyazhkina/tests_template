<script setup lang="ts">
import { ref } from 'vue'
import AppInput from './AppInput.vue'

const props = defineProps<{
  onClose: () => void
  isModalOpen: boolean
}>()

const chat = ref<string | null>(null)

const emit = defineEmits<{
  (e: 'add-chat', value: string): void
}>()

const closeModal = () => {
  chat.value = null
  props.onClose()
}

const submit = () => {
  if (chat.value && chat.value.length > 0) {
    emit('add-chat', chat.value)
    chat.value = null
    closeModal()
  }
}
</script>

<template>
  <div v-if="props.isModalOpen" class="modal-overlay">
    <div class="modal">
      <h3>Add new chat</h3>
      <AppInput v-model.string="chat" type="text" placeholder="Enter chat title" name="chat" />
      <div class="modal-actions">
        <button class="confirm-btn" @click="submit" type="submit">Add</button>
        <button class="cancel-btn" @click="closeModal">Cancel</button>
      </div>
    </div>
  </div>
</template>

<style lang="css" scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 25px;
  border-radius: 16px;
  width: 300px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.modal h3 {
  margin-top: 0;
}

.modal input {
  width: 100%;
  padding: 8px;
  margin: 15px 0;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
}

.confirm-btn {
  background-color: #5a6b3c;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #ccc;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}
</style>
