<!--
SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.

SPDX-License-Identifier: Apache-2.0
-->

<script setup lang="ts">
import { marked } from "marked";
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    value: string;
    size?: "sm" | "md" | "lg";
  }>(),
  { size: "md" },
);

const RE_AT = /^@((\w*)|"[\w ]+") /;

const hasAt = computed(() => RE_AT.test(props.value));

const atPrefix = computed(() => {
  const match = props.value.match(RE_AT);
  if (!match) return null;

  // Remove quotes if they exist
  let prefix = match[1];
  if (prefix.startsWith('"') && prefix.endsWith('"')) {
    prefix = prefix.slice(1, -1);
  }
  return prefix;
});

const valueWithoutAt = computed(() => {
  if (hasAt.value) {
    return props.value.replace(RE_AT, "");
  }
  return props.value;
});

const output = computed(() => {
  const html = marked(valueWithoutAt.value) as string;
  return html.replace(/^<p>(.*?)<\/p>/, "$1");
});
</script>

<template>
  <article
    class="prose dark:prose-invert w-full max-w-full prose-violet"
    :class="{
      'prose-sm': size === 'sm',
      'prose-lg': size === 'lg',
    }"
  >
    <span
      v-if="hasAt"
      class="inline-block px-3 py-1 mr-2 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-sm font-medium"
      >@{{ atPrefix }}</span
    >
    <p v-html="output" class="inline" />
  </article>
</template>
