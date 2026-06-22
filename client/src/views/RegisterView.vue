<script setup lang="ts">
import { ref } from 'vue'
import AppButton from '@/components/AppButton.vue'
import AppInput from '@/components/AppInput.vue'
import axios from 'axios'

const firstName = ref('')
const surname = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

const handleRegister = async () => {
  error.value = ''

  if (!email.value || !firstName.value || !surname.value || !password.value) {
    error.value = 'All fields are required'
    return
  }

  const response = await axios.post('http://localhost/api/auth/register', {
    name: firstName.value,
    surname: surname.value,
    email: email.value,
    password: password.value,
    role: 'user',
  })

  return await response.data
}
</script>

<template>
  <div class="register-container">
    <h2>Register to ML Service</h2>

    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label>Name</label>
        <AppInput
          type="text"
          v-model="firstName"
          required
          name="name"
          placeholder="Type your name"
        />
      </div>

      <div class="form-group">
        <label>Surname</label>
        <AppInput
          type="text"
          v-model="surname"
          required
          name="surname"
          placeholder="Type your surname"
        />
      </div>

      <div class="form-group">
        <label>Email</label>
        <AppInput
          type="email"
          v-model="email"
          required
          name="login"
          placeholder="Type your email"
        />
      </div>

      <div class="form-group">
        <label>Password</label>
        <AppInput type="password" v-model="password" required name="Type your password" />
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <AppButton type="submit"> Register </AppButton>
    </form>
  </div>
</template>

<style scoped>
.register-container {
  width: 420px;
  margin: 100px auto;
  background: rgba(200, 210, 180, 0.3);
  padding: 3rem;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

.error {
  color: red;
  margin-bottom: 10px;
}
</style>
