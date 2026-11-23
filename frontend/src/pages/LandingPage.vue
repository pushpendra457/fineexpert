<template>
  <DefaultLayout>
    <section class="py-20 md:py-28 bg-gradient-to-b from-indigo-50/50 to-white text-center">
      <div class="max-w-4xl mx-auto px-4 sm:px-6">
        <h1 class="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900">
          Intelligent Document AI & <span class="bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">Agentic Workflows</span>
        </h1>
        <p class="mt-6 text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto">
          Upload complex documents, extract grounded insights with RAG, and execute autonomous multi-step reasoning agents.
        </p>
        <div class="mt-8 flex justify-center gap-4">
          <router-link to="/about" class="px-6 py-3 rounded-xl bg-indigo-600 text-white font-medium hover:bg-indigo-700 shadow-sm transition-all">Explore About Page</router-link>
        </div>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '../layouts/DefaultLayout.vue'
</script>
