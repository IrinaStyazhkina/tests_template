import { ref } from 'vue'

export const snackbarMessage = ref('')
export const snackbarVisible = ref(false)

export function showSnackbar(message: string, duration = 3000) {
  snackbarMessage.value = message
  snackbarVisible.value = true

  setTimeout(() => {
    snackbarVisible.value = false
    snackbarMessage.value = ''
  }, duration)
}
