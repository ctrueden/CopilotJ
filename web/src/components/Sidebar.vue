<!--
SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.

SPDX-License-Identifier: Apache-2.0
-->

<script setup lang="ts">
import { IconCirclePlus2, IconSettings } from "@tabler/icons-vue";
import { computed } from "vue";
import type { Post } from "../store";
import { useActiveThread, useSettings, useSystemState } from "../store";

const emit = defineEmits<{
  (e: "start-new-thread"): void;
  (e: "click-post", postId: string): void;
}>();

const settings = useSettings();
const state = useSystemState();
const activeThread = useActiveThread();

const summaries = computed(() => {
  const groups: Post[][] = [];
  for (const p of activeThread.thread.posts) {
    if (p.type == "user" || groups.length == 0) {
      groups.push([p]);
    } else {
      groups[groups.length - 1].push(p);
    }
  }

  const summaries = [];
  for (const group of groups) {
    const summary = {
      targetId: "",
      task: "",
      agents: 0,
      tools: 0,
      finished: true,
    };

    const agents = new Set<string>();
    for (const post of group) {
      if (post.type == "user") {
        summary.targetId = post.id;
        summary.task = post.content.data;
      } else if (post.type == "agent") {
        // TODO: time?
        summary.tools += post.thought.reduce((a, b) => a + (b.type == "action" ? 1 : 0), 0);
        summary.finished = !post.streaming;
        agents.add(post.role);
      }
    }
    summary.agents = agents.size;
    summaries.push(summary);
  }
  return summaries;
});

function startNewThread() {
  emit("start-new-thread");
}

function truncate(text?: string): string | undefined {
  const maxLength = 128;
  if (!text || text.length <= maxLength) {
    return text;
  }
  return text.slice(0, maxLength) + "...";
}
</script>

<template>
  <!-- Sidebar -->
  <aside class="shadow-lg flex flex-col bg-white dark:bg-gray-900" :class="settings.expandSidebar ? 'w-64' : 'w-16'">
    <div class="p-4 pt-3" :class="{ 'px-2': !settings.expandSidebar }">
      <button
        :class="[
          'w-full rounded-lg py-2 flex justify-center items-center cursor-pointer transition',
          'text-white bg-violet-500 dark:bg-violet-700 hover:bg-violet-600 hover:dark:bg-violet-600',
          { 'px-4 gap-2': settings.expandSidebar },
        ]"
        @click="startNewThread"
      >
        <IconCirclePlus2 /><span v-if="settings.expandSidebar" class="truncate">New Thread</span>
      </button>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-y-auto flex flex-col gap-3" :class="settings.expandSidebar ? 'p-4' : 'px-2 py-4'">
      <h3 v-if="settings.expandSidebar && summaries.length > 0" class="text-sm">Your inputs</h3>

      <div v-for="s in summaries" :key="`post-summary-${s.targetId}`" class="flex flex-col">
        <div
          class="cursor-pointer transition"
          :class="
            settings.expandSidebar
              ? 'px-3 py-2 rounded-xl border border-violet-200 dark:border-violet-900 bg-violet-50 dark:bg-violet-950/10 dark:hover:bg-violet-950/50 hover:shadow'
              : 'h-6 w-6 self-center rounded-md bg-violet-300 dark:bg-violet-500 hover:bg-violet-400'
          "
          v-tooltip="!settings.expandSidebar ? s.task : null"
          @click="emit('click-post', s.targetId)"
        >
          <p v-if="settings.expandSidebar" class="prose dark:prose-invert text-sm">{{ truncate(s.task) ?? "..." }}</p>
        </div>

        <p v-if="settings.expandSidebar" class="my-1 px-3 text-xs text-gray-500 dark:text-gray-400">
          <template v-if="!s.finished">Working...</template>

          <template v-else>
            {{ s.agents }} agent{{ s.agents > 1 ? "s" : "" }} completed your task<template v-if="s.tools > 0">
              using {{ s.tools }} tool{{ s.tools > 1 ? "s" : "" }}</template
            >.
          </template>
        </p>
      </div>
    </div>

    <!-- Bottom Actions -->
    <div class="w-full p-2 pb-4 border-t border-gray-200 dark:border-gray-700">
      <div class="flex flex-col gap-1">
        <button
          v-for="{ icon, text, onClick } in [
            { icon: IconSettings, text: 'Settings', onClick: () => (state.showSettings = true) },
          ]"
          :key="icon.name"
          :class="[
            'rounded p-2 flex items-center gap-2 text-left cursor-pointer transition-colors',
            'hover:bg-gray-100 dark:hover:bg-gray-700',
            settings.expandSidebar ? 'justify-start' : 'justify-center',
          ]"
          @click="onClick"
        >
          <component :is="icon" class="text-slate-600 dark:text-slate-400" />

          <span v-if="settings.expandSidebar">{{ text }}</span>
        </button>
      </div>
    </div>
  </aside>
</template>
