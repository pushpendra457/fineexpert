<template>
  <header class="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
      <router-link to="/" class="flex items-center space-x-2">
        <span class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">FineExpert</span>
      </router-link>
      <nav class="hidden md:flex space-x-8">
        <router-link to="/" class="text-sm font-medium text-slate-700 hover:text-indigo-600 transition-colors">Home</router-link>
        <router-link to="/about" class="text-sm font-medium text-slate-700 hover:text-indigo-600 transition-colors">About</router-link>
      </nav>
      <div class="flex items-center space-x-4">
        <router-link to="/about" class="text-sm font-medium px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors">Get Started</router-link>
      </div>
    </div>
  </header>
</template>
