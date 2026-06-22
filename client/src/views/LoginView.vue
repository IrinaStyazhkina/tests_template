<script setup lang="ts">
import { ref } from 'vue'
import AppButton from '@/components/AppButton.vue'
import AppInput from '@/components/AppInput.vue'
import apiClient from '@/api/api'
import { useRouter } from 'vue-router'
import { showSnackbar } from '@/stores/snackbar'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const userStore = useUserStore()

const email = ref('')
const password = ref('')

const handleLogin = async () => {
  if (!email.value || !password.value) {
    showSnackbar('All fields are required')
    return
  }

  try {
    const response = await apiClient.post('/auth/login', {
      email: email.value,
      password: password.value,
    })

    if (response.status === 200) {
      userStore.loadCurrentUser()
      router.push('/')
    }
  } catch (e) {
    showSnackbar('Login failed')
    console.error(e)
  }
}
</script>

<template>
  <div class="login-container">
    <h2>Login to ML Service</h2>
    <h3>Here you can ask LLM everything you want. And maybe you'll get an answer</h3>

    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>Email</label>
        <AppInput type="email" v-model="email" required name="login" placeholder="Type your name" />
      </div>

      <div class="form-group">
        <label>Password</label>
        <AppInput type="password" v-model="password" required name="Type your password" />
      </div>
      <AppButton type="submit"> Login </AppButton>

      <div class="form-group">
        If you don't have an account, please, welcome to <a href="/register">Register page</a>
      </div>
    </form>
  </div>
</template>

<style scoped>
.login-container {
  width: 420px;
  margin: 100px auto;
  background: rgba(200, 210, 180, 0.3);
  padding: 3rem;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
  margin-top: 15px;
}

.error {
  color: red;
  margin-bottom: 10px;
}
</style>
