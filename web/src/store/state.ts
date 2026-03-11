/**
 * SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

import { acceptHMRUpdate, defineStore } from "pinia";
import { ref } from "vue";

export const useSystemState = defineStore("state", () => {
  const showSettings = ref(false);
  const showManageAgents = ref(false);
  return { showManageAgents, showSettings };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useSystemState, import.meta.hot));
}
