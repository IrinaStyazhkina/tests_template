export type Message = {
  id: string
  message_type: 'user' | 'system'
  content: string
}
