export const clearCookie = async (name: string) => {
  if ('cookieStore' in window) {
    try {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      await (window as any).cookieStore.delete('access_token')
    } catch (err) {
      console.error('Ошибка удаления через Cookie Store API:', err)
    }
  }
}
