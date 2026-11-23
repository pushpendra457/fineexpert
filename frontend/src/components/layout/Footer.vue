<template>
  <footer class="bg-slate-900 text-slate-400 py-12 border-t border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-4 gap-8">
      <div>
        <span class="text-xl font-bold text-white">FineExpert</span>
        <p class="mt-2 text-sm">Enterprise-grade AI document intelligence and agentic workflows.</p>
      </div>
      <div>
        <h4 class="text-sm font-semibold text-white uppercase tracking-wider">Product</h4>
        <ul class="mt-4 space-y-2 text-sm">
          <li><router-link to="/" class="hover:text-white">Features</router-link></li>
          <li><router-link to="/about" class="hover:text-white">Tech Stack</router-link></li>
        </ul>
      </div>
      <div>
        <h4 class="text-sm font-semibold text-white uppercase tracking-wider">Company</h4>
        <ul class="mt-4 space-y-2 text-sm">
          <li><router-link to="/about" class="hover:text-white">About Us</router-link></li>
          <li><router-link to="/about" class="hover:text-white">Mission & Vision</router-link></li>
        </ul>
      </div>
      <div>
        <h4 class="text-sm font-semibold text-white uppercase tracking-wider">Open Source</h4>
        <p class="mt-4 text-sm">Built collaboratively with modern startup engineering standards.</p>
      </div>
    </div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 pt-8 border-t border-slate-800 text-xs text-center">
      &copy; 2026 FineExpert Team. All rights reserved.
    </div>
  </footer>
</template>
