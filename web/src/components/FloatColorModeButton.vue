<!--
SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.

SPDX-License-Identifier: Apache-2.0
-->

<script setup lang="ts">
import { IconMoon, IconSun, IconSunMoon } from "@tabler/icons-vue";
import { useColorMode } from "@vueuse/core";
import { computed } from "vue";
import FloatIconButton from "./FloatIconButton.vue";

const values = ["auto", "light", "dark"] as const;
const icons = [IconSunMoon, IconSun, IconMoon] as const;
const descriptions = ["Follow system preference", "Light mode", "Dark mode"] as const;

const colorMode = useColorMode({ emitAuto: true });

const currentIndex = computed(() => values.indexOf(colorMode.value));
</script>

<template>
  <FloatIconButton
    :title="descriptions[currentIndex]"
    :icon="icons[currentIndex]"
    @click="colorMode = values[currentIndex + (1 % values.length)]"
  />
</template>
