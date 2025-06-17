<!-- NavBar.vue 内 -->
<script setup>
function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme)
}
</script>

<template>
  <div class="dropdown dropdown-end">
    <label tabindex="0" class="btn m-1">🎨 主题</label>
    <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
      <li><a @click="setTheme('light')">🌞 light</a></li>
      <li><a @click="setTheme('dark')">🌙 dark</a></li>
      <li><a @click="setTheme('cupcake')">🧁 cupcake</a></li>
      <li><a @click="setTheme('dracula')">🧛 dracula</a></li>
      <li><a @click="setTheme('lofi')">📓 lofi</a></li>
    </ul>
  </div>
</template>
