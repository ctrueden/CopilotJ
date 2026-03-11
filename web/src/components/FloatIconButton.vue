<!--
SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.

SPDX-License-Identifier: Apache-2.0
-->

<script setup lang="ts">
import type { Icon } from "@tabler/icons-vue";

const props = withDefaults(
  defineProps<{
    icon: Icon;
    disabled?: boolean;
  }>(),
  { disabled: false },
);

const emit = defineEmits<{
  (e: "click"): void;
}>();

function onClick() {
  if (props.disabled) return;
  emit("click");
}
</script>

<template>
  <div
    class="rounded-lg p-2 flex gap-4 transition-colors hover:bg-gray-200 dark:hover:bg-gray-800"
    :class="{ 'opacity-50 cursor-not-allowed': props.disabled, 'cursor-pointer': !props.disabled }"
    @click="onClick"
  >
    <component :is="props.icon" class="w-6 h-6" />
  </div>
</template>
