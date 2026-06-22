<script setup lang="ts">
defineProps({
  name: {
    type: String,
    required: true,
  },
  surname: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
  },
})
</script>
<template>
  <div class="profile__info">
    <p><span class="label">Name:</span> {{ name }}</p>
    <p><span class="label">Surname:</span> {{ surname }}</p>
    <p><span class="label">Email:</span> {{ email }}</p>
  </div>
</template>

<style lang="css" scoped>
.profile__info p {
  margin: 8px 0;
  font-size: 16px;
}

.label {
  font-weight: bold;
}
</style>
