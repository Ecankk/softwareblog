<template>
  <div
    class="border rounded-lg overflow-hidden shadow hover:shadow-md transition cursor-pointer"
    @click="$router.push(`/posts/${post.slug}`)"
  >
    <img v-if="post.cover" :src="post.cover" class="w-full h-40 object-cover" />
    <div class="p-4">
      <h2 class="text-xl font-semibold mb-2">{{ post.title }}</h2>
      <p class="text-gray-600 text-sm">{{ post.summary }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  post: { type: Object, required: true },
})
</script>
