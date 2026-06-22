<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import AdminTable from '@/components/AdminTable.vue'
import type { Transaction } from '@/types/Transaction'
import apiClient from '@/api/api'
import { showSnackbar } from '@/stores/snackbar'

const transactions = ref<Transaction[]>([])

const loadTransactions = async () => {
  try {
    const response = await apiClient.get('/admin/transactions/all')
    transactions.value = response.data.map(
      (item: {
        id: string
        amount: number
        created_at: string
        transaction_type: string
        transaction_status: string
        updated_at: string
        user_id: string
      }) => ({
        id: item.id,
        amount: item.amount,
        createdAt: new Date(item.created_at).toLocaleString(),
        transactionType: item.transaction_type,
        transactionStatus: item.transaction_status,
        updatedAt: new Date(item.updated_at).toLocaleString(),
        userId: item.user_id,
      }),
    )
  } catch (err) {
    showSnackbar('Failed to load transactions')
    console.error(err)
  }
}

const approveTransaction = async (transactionId: string) => {
  const response = await apiClient.patch(`/admin/transactions/approve/${transactionId}`)
  if (response.data) {
    loadTransactions()
  }
}

const declineTransaction = async (transactionId: string) => {
  const response = await apiClient.patch(`/admin/transactions/decline/${transactionId}`)
  if (response.data) {
    loadTransactions()
  }
}

onMounted(() => {
  loadTransactions()
})
</script>
<template>
  <div class="transactions">
    <div class="transactions__card">
      <div class="header">
        <h2>Transactions</h2>
      </div>
      <AdminTable
        :transactions="transactions"
        :approveTransaction="approveTransaction"
        :declineTransaction="declineTransaction"
      />
      <p v-if="!transactions.length" class="empty">No transactions yet</p>
    </div>
  </div>
</template>

<style scoped>
.transactions {
  min-height: 78vh;
  padding: 40px;
  background: rgba(200, 210, 180, 0.3);
  font-family: Arial, sans-serif;
}

.transactions__card {
  background: #ffffff;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.empty {
  text-align: center;
  margin-top: 20px;
  color: #777;
}
</style>
