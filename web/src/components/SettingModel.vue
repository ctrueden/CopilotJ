<!--
SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.

SPDX-License-Identifier: Apache-2.0
-->

<script setup lang="ts">
import { ref, watch } from "vue";
import type { ThreadConfigModel } from "../apis";
import { getModelName } from "../util";

const props = defineProps<{
  model: ThreadConfigModel | null;
}>();

const emit = defineEmits<{
  (e: "update:model", value: ThreadConfigModel | null): void;
}>();

const useDefaultModel = ref(true);
const model = ref("");
const apiKey = ref("");

const modelOptions = [
  "gpt-5",
  "gpt-5-mini",
  "gpt-5-nano",
  "gpt-4.1",
  "gpt-4.1-mini",
  "gpt-4.1-nano",
  "gpt-4o",
  "gpt-4o-mini",
  "gemini-2.5-pro",
  "gemini-2.5-flash",
  "gemini-2.5-flash-lite",
].map((m) => ({ label: m, value: getModelName(m) }));

watch(
  props,
  (newProps) => {
    if (newProps.model) {
      model.value = newProps.model.name ? newProps.model.name : modelOptions[0].value;
      apiKey.value = newProps.model.api_key || "";
      useDefaultModel.value = false;
    } else {
      model.value = "";
      apiKey.value = "";
      useDefaultModel.value = true;
    }
  },
  { immediate: true },
);

function submit() {
  if (useDefaultModel.value) {
    emit("update:model", null);
  } else {
    emit("update:model", {
      name: model.value,
      api_key: apiKey.value,
    });
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <FormItem for="defaultModel" label="Use Default Model" layout="row">
      <ToggleSwitch v-model="useDefaultModel" inputId="defaultModel" />
    </FormItem>

    <FormItem for="model" label="Model Configuration">
      <Select
        v-model="model"
        labelId="model"
        :options="modelOptions"
        optionLabel="label"
        optionValue="value"
        :disabled="useDefaultModel"
      />
    </FormItem>

    <FormItem for="apiKey" label="API Key">
      <InputText
        type="text"
        v-model="apiKey"
        inputId="apiKey"
        placeholder="Enter your API key"
        :disabled="useDefaultModel"
      />
    </FormItem>

    <Button label="Submit" @click="submit" />
  </div>
</template>
