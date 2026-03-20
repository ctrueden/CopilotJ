<!--
SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.

SPDX-License-Identifier: Apache-2.0
-->

<script setup lang="ts">
import Logo from "./Logo.vue";

const suggestions = [
  "Find best segmentation method for this image",
  "Segment this low signal-to-noise cell image",
  "Show my workflows",
  "Compare these two analysis methods",
];

const emit = defineEmits<{
  (event: "usePromptSuggestion", suggestion: string): void;
}>();

function usePromptSuggestion(suggestion: string) {
  emit("usePromptSuggestion", suggestion);
}
</script>

<template>
  <div class="my-20 flex flex-col items-center justify-center h-full text-center">
    <Logo class="w-24 h-24" />

    <h2 class="my-4 text-2xl font-semibold">CopilotJ</h2>

    <p class="text-sm max-w-md">Ask questions or give tasks for the Leader Agent to process.</p>

    <div class="w-full mt-8 grid md:grid-cols-2 grid-cols-1 gap-4">
      <div
        v-for="suggestion in suggestions"
        :key="suggestion"
        class="rounded-lg p-4 text-left bg-white dark:bg-gray-900 transition shadow-sm hover:shadow-md cursor-pointer"
        @click="usePromptSuggestion(suggestion)"
      >
        {{ suggestion }}
      </div>
    </div>
  </div>
</template>
