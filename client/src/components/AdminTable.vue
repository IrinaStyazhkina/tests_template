<script setup lang="ts">
import type { Transaction } from '@/types/Transaction'

const props = defineProps<{
  transactions: Transaction[]
  approveTransaction: (transactionId: string) => void
  declineTransaction: (transactionId: string) => void
}>()
</script>
<template>
  <table class="transactions__table">
    <thead>
      <tr>
        <th>Operation ID</th>
        <th>User ID</th>
        <th>Date</th>
        <th>Operation Type</th>
        <th>Sum</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="transaction in props.transactions" :key="transaction.id">
        <td>{{ transaction.id }}</td>
        <td>{{ transaction.userId }}</td>
        <td>{{ transaction.createdAt }}</td>
        <td>{{ transaction.transactionType }}</td>
        <td
          :class="{
            positive: transaction.transactionType == 'deposit',
            negative: transaction.transactionType == 'withdrawal',
          }"
        >
          {{ transaction.amount }}
        </td>
        <td>
          <div
            class="actions"
            v-if="
              transaction.transactionType == 'deposit' &&
              transaction.transactionStatus === 'pending'
            "
          >
            <button class="confirm-btn" @click="() => approveTransaction(transaction.id)">
              Approve
            </button>
            <button class="cancel-btn" @click="() => declineTransaction(transaction.id)">
              Decline
            </button>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style lang="css" scoped>
.transactions__table {
  width: 100%;
  border-collapse: collapse;
}

.transactions__table th,
.transactions__table td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  text-align: left;
}

.transactions__table th {
  background-color: #f4f6ef;
}

.positive {
  color: green;
  font-weight: bold;
}

.negative {
  color: red;
  font-weight: bold;
}

.actions {
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
  margin-right: 4px;
}

.cancel-btn {
  background-color: #ccc;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}
</style>
