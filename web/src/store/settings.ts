/**
 * SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

import { acceptHMRUpdate, defineStore } from "pinia";
import { computed, ref } from "vue";
import type { ThreadConfigModel, ThreadConfigQuery } from "../apis";

export const useSettings = defineStore("settings", () => {
  const expandSidebar = ref(false);
  const autoScroll = ref(true);

  const model = ref<ThreadConfigModel | null>(null);
  const value = computed<ThreadConfigQuery>(() => ({
    model: model.value,
  }));

  function toggleExpandSidebar(enable?: boolean) {
    expandSidebar.value = enable ?? !expandSidebar.value;
  }

  function toggleAutoScroll(enable?: boolean) {
    autoScroll.value = enable ?? !autoScroll.value;
  }

  function setModel(newModel: ThreadConfigModel | null) {
    model.value = newModel;
  }

  function reset() {
    expandSidebar.value = true;
    autoScroll.value = false;
  }

  return { expandSidebar, autoScroll, value, model, toggleAutoScroll, toggleExpandSidebar, setModel, reset };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSettings, import.meta.hot));
}
