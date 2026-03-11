<!--
SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.

SPDX-License-Identifier: Apache-2.0
-->

<script setup lang="ts">
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
    <div class="chatbox-hello_icon w-24 h-24 rounded-full flex justify-center items-center">
      <img src="../assets/copilotj.png" class="w-7/12 h-7/12 select-none" />
    </div>

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

<style>
.chatbox-hello_icon {
  --c: var(--color-violet-500);

  background-color: var(--c);
  color: #fff;
  border: none;
  cursor: pointer;
  position: relative;
  box-shadow: 0px 0px 25px color-mix(in oklch, var(--c) 50%, transparent);
  outline: 0;
  transition:
    transform ease-in 0.1s,
    background-color ease-in 0.1s,
    box-shadow ease-in 0.5s;

  &:hover {
    box-shadow: 0px 0px 50px color-mix(in oklch, var(--c) 75%, transparent);
  }

  &::before {
    position: absolute;
    content: "";
    left: -2em;
    right: -2em;
    top: -2em;
    bottom: -2em;
    pointer-events: none;
    transition: ease-in-out 0.5s;
    background-repeat: no-repeat;
    background-image:
      radial-gradient(circle, var(--c) 20%, transparent 20%), radial-gradient(circle, var(--c) 20%, transparent 20%),
      radial-gradient(circle, var(--c) 20%, transparent 20%), radial-gradient(circle, var(--c) 20%, transparent 20%),
      radial-gradient(circle, var(--c) 20%, transparent 20%), radial-gradient(circle, var(--c) 20%, transparent 20%),
      radial-gradient(circle, var(--c) 20%, transparent 20%), radial-gradient(circle, var(--c) 20%, transparent 20%),
      radial-gradient(circle, var(--c) 20%, transparent 20%), radial-gradient(circle, var(--c) 20%, transparent 20%),
      radial-gradient(circle, var(--c) 20%, transparent 20%), radial-gradient(circle, var(--c) 20%, transparent 20%),
      radial-gradient(circle, var(--c) 20%, transparent 20%), radial-gradient(circle, var(--c) 20%, transparent 20%),
      radial-gradient(circle, var(--c) 20%, transparent 20%), radial-gradient(circle, var(--c) 20%, transparent 20%);
    background-size:
      10% 10%,
      20% 20%,
      15% 15%,
      20% 20%,
      18% 18%,
      10% 10%,
      15% 15%,
      10% 10%,
      18% 18%,
      15% 15%,
      20% 20%,
      18% 18%,
      20% 20%,
      15% 15%,
      10% 10%,
      20% 20%;

    background-position:
      18% 40%,
      20% 31%,
      30% 27%,
      40% 19%,
      50% 15%,
      57% 17%,
      65% 22%,
      80% 32%,
      83% 60%,
      16% 60%,
      20% 68%,
      25% 75%,
      41% 82%,
      50% 85%,
      64% 80%,
      80% 71%;
    animation: bubbles ease-in-out 0.75s forwards;
  }

  &:active {
    transform: scale(0.95);
    background-color: var(--color-violet-700);

    &::before {
      animation: none;
      background-size: 0;
    }
  }
}

@keyframes bubbles {
  0% {
    background-position:
      18% 40%,
      20% 31%,
      30% 27%,
      40% 19%,
      50% 15%,
      57% 17%,
      65% 22%,
      80% 32%,
      83% 60%,
      16% 60%,
      20% 68%,
      25% 75%,
      41% 82%,
      51% 85%,
      64% 80%,
      80% 71%;
  }

  50% {
    background-position:
      10% 44%,
      0% 20%,
      15% 5%,
      30% 0%,
      43% 0%,
      62% -2%,
      75% 0%,
      95% 20%,
      95% 55%,
      0% 80%,
      7% 100%,
      24% 100%,
      41% 100%,
      53% 95%,
      68% 96%,
      95% 83%;
  }

  100% {
    background-position:
      5% 44%,
      -5% 20%,
      7% 5%,
      23% 0%,
      37% 0%,
      58% -2%,
      80% 0%,
      100% 20%,
      100% 55%,
      -5% 80%,
      2% 100%,
      23% 100%,
      42% 102%,
      55% 99%,
      70% 96%,
      100% 85%;

    background-size: 0% 0%;
  }
}
</style>
