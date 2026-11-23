<template>
  <DefaultLayout>
    <!-- Hero Section -->
    <section class="py-16 md:py-24 bg-gradient-to-br from-indigo-900 via-slate-900 to-indigo-950 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <span class="px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-400/30">About FineExpert</span>
        <h1 class="mt-4 text-4xl sm:text-5xl font-extrabold tracking-tight">
          Democratizing Document Intelligence through Agentic AI
        </h1>
        <p class="mt-4 max-w-2xl mx-auto text-lg text-slate-300">
          Built from the ground up with Clean Architecture, production RAG pipelines, and autonomous LangGraph agents.
        </p>
      </div>
    </section>

    <!-- Mission & Vision Section -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-2 gap-12">
        <div class="p-8 rounded-2xl bg-indigo-50/60 border border-indigo-100">
          <div class="w-12 h-12 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-bold text-xl">M</div>
          <h2 class="mt-4 text-2xl font-bold text-slate-900">Our Mission</h2>
          <p class="mt-2 text-slate-600 leading-relaxed">
            To provide knowledge workers and enterprise teams with lightning-fast, verified, and hallucination-free document intelligence through state-of-the-art Retrieval-Augmented Generation.
          </p>
        </div>
        <div class="p-8 rounded-2xl bg-violet-50/60 border border-violet-100">
          <div class="w-12 h-12 rounded-xl bg-violet-600 text-white flex items-center justify-center font-bold text-xl">V</div>
          <h2 class="mt-4 text-2xl font-bold text-slate-900">Our Vision</h2>
          <p class="mt-2 text-slate-600 leading-relaxed">
            A world where documents are dynamic knowledge bases that actively assist in decision-making, planning, and multi-agent workflow execution.
          </p>
        </div>
      </div>
    </section>

    <!-- Technology Stack Section -->
    <section class="py-16 bg-slate-50 border-y border-slate-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-3xl font-bold text-slate-900">Production-Grade Technology Stack</h2>
          <p class="mt-2 text-slate-600">Engineered for high performance, modularity, and strict type safety.</p>
        </div>

        <div class="mt-12 grid grid-cols-2 md:grid-cols-4 gap-6">
          <div v-for="tech in techStack" :key="tech.name" class="p-6 bg-white rounded-xl border border-slate-200 shadow-sm text-center">
            <h3 class="text-lg font-bold text-slate-800">{{ tech.name }}</h3>
            <span class="inline-block mt-2 px-2.5 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-700">{{ tech.role }}</span>
            <p class="mt-3 text-xs text-slate-500">{{ tech.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Contributors & Open Source -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl font-bold text-slate-900">Open Source & Team Engineering</h2>
        <p class="mt-2 text-slate-600 max-w-2xl mx-auto">
          Co-developed by a 3-engineer collaborative squad practicing standard startup CI/CD workflows and automated deployment.
        </p>

        <div class="mt-10 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto text-left">
          <div class="p-6 rounded-xl border border-slate-200 bg-slate-50">
            <h4 class="font-bold text-slate-900">Developer 1 — Backend & Core</h4>
            <p class="text-xs text-indigo-600 font-medium mt-1">FastAPI, Auth, PostgreSQL, Docker, CI</p>
            <p class="text-sm text-slate-600 mt-3">Architecting scalable RESTful APIs, JWT & OAuth authentication, and repository layer persistence.</p>
          </div>
          <div class="p-6 rounded-xl border border-slate-200 bg-slate-50">
            <h4 class="font-bold text-slate-900">Developer 2 — Frontend & UX</h4>
            <p class="text-xs text-indigo-600 font-medium mt-1">Vue 3, TypeScript, Pinia, Tailwind CSS</p>
            <p class="text-sm text-slate-600 mt-3">Delivering responsive interfaces, interactive dashboards, and robust UI component libraries.</p>
          </div>
          <div class="p-6 rounded-xl border border-slate-200 bg-slate-50">
            <h4 class="font-bold text-slate-900">Developer 3 — AI & RAG</h4>
            <p class="text-xs text-indigo-600 font-medium mt-1">LangChain, LangGraph, Qdrant, Celery</p>
            <p class="text-sm text-slate-600 mt-3">Orchestrating vector similarity retrieval, asynchronous document chunking, and agent graphs.</p>
          </div>
        </div>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '../layouts/DefaultLayout.vue'

const techStack = [
  { name: 'Vue 3 & Vite', role: 'Frontend Core', desc: 'Composition API with strict TypeScript & Tailwind' },
  { name: 'FastAPI', role: 'Backend API', desc: 'Asynchronous Python 3.12 with Clean Architecture' },
  { name: 'PostgreSQL & Neon', role: 'Database', desc: 'Relational persistence with SQLAlchemy 2.0 & Alembic' },
  { name: 'Qdrant Cloud', role: 'Vector Search', desc: 'High-speed embeddings & similarity retrieval' },
  { name: 'LangGraph', role: 'Agentic AI', desc: 'Multi-node stateful workflows with reasoning and tools' },
  { name: 'Celery & Redis', role: 'Background Queue', desc: 'Asynchronous PDF ingestion and chunk indexing' },
  { name: 'Docker Compose', role: 'Containerization', desc: 'Unified development and production environments' },
  { name: 'Cloudflare & Render', role: 'Deployment', desc: 'Automated CI/CD deployment pipelines on main merge' },
]
</script>
