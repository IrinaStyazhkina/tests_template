import type { Message } from './Message'

export type Chat = {
  id: string
  title: string
  messages: Message[]
}
