import { defineStore } from "pinia"
import { ref } from "vue"

export const useGlobalStore = defineStore(
  "global",
  () => {
    const isLoading = ref(false)
    const sidebarOpen = ref(false)
    const theme = ref("light")

    const setLoading = (loading) => {
      isLoading.value = loading
    }

    const toggleSidebar = () => {
      sidebarOpen.value = !sidebarOpen.value
    }

    const toggleTheme = () => {
      theme.value = theme.value === "light" ? "dark" : "light"
    }

    return {
      isLoading,
      sidebarOpen,
      theme,
      setLoading,
      toggleSidebar,
      toggleTheme,
    }
  },
  {
    persist: {
      paths: ["theme"],
    },
  },
)
