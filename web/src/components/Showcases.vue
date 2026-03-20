<!--
SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.

SPDX-License-Identifier: Apache-2.0
-->

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRoute, RouterLink, RouterView } from "vue-router";
const vueRoute = useRoute();
const current = computed(() => vueRoute.path.replace(/^\//, "") || "overview");

function navClass(id: string) {
  return (
    "hover:opacity-80 " +
    (current.value === id ? "text-emerald-600 underline decoration-emerald-400 underline-offset-4" : "")
  );
}

onMounted(() => {
  // Pause videos not in view; ensure only one plays at a time
  const videos = Array.from(document.querySelectorAll("video")) as HTMLVideoElement[];
  const vio = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) (e.target as HTMLVideoElement).pause();
      });
    },
    { threshold: [0.25] },
  );
  videos.forEach((v) => {
    vio.observe(v);
    v.addEventListener("play", () => {
      videos.forEach((o) => {
        if (o !== v) o.pause();
      });
    });
  });
});
</script>

<template>
  <div
    class="min-h-screen bg-[radial-gradient(60%_35%_at_50%_-10%,rgba(16,185,129,0.15),transparent),radial-gradient(40%_25%_at_80%_10%,rgba(59,130,246,0.18),transparent)] text-zinc-900"
  >
    <!-- Header -->
    <header
      class="sticky top-0 z-50 border-b border-zinc-200/60 bg-white/70 backdrop-blur supports-[backdrop-filter]:bg-white/50 dark:border-zinc-800/60 dark:bg-zinc-950/40"
    >
      <div class="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-3 md:px-10">
        <div class="flex items-center gap-2">
          <span class="text-sm font-semibold tracking-wide">CopilotJ</span>
        </div>
        <nav class="hidden items-center gap-6 text-sm md:flex">
          <RouterLink to="/overview" :class="navClass('overview')">Overview</RouterLink>
          <RouterLink to="/videos" :class="navClass('video')">Demos</RouterLink>
          <RouterLink to="/config" :class="navClass('config')">User Manual</RouterLink>
          <RouterLink to="/community" :class="navClass('community')">Integrations</RouterLink>
          <RouterLink to="/about" :class="navClass('about')">About</RouterLink>
        </nav>
      </div>
    </header>

    <RouterView />
  </div>
</template>
