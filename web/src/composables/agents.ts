/**
 * SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

import { useStorage } from "@vueuse/core";
import { v4 as uuidv4 } from "uuid";
import { computed, ref } from "vue";

export interface Agent {
  id: string;
  name: string;
  icon: string;
  type: string;
  status: "active" | "inactive";
  role: string;
  createdAt: Date;
  updatedAt: Date;
  config: Record<string, any>;
  permissions: string[];
}

export interface AgentFormData {
  name: string;
  role: string;
  type: string;
  config: Record<string, any>;
}

export type AgentFilter = {
  search: string;
  status: "all" | "active" | "inactive";
  role: string;
};

export function useAgents() {
  const agents = useStorage<Agent[]>("agents", []);
  const filter = ref<AgentFilter>({
    search: "",
    status: "all",
    role: "",
  });

  const filteredAgents = computed(() => {
    return agents.value.filter((agent) => {
      const matchesSearch =
        agent.name.toLowerCase().includes(filter.value.search.toLowerCase()) ||
        agent.role.toLowerCase().includes(filter.value.search.toLowerCase());
      const matchesStatus = filter.value.status === "all" || agent.status === filter.value.status;
      const matchesRole = !filter.value.role || agent.role === filter.value.role;

      return matchesSearch && matchesStatus && matchesRole;
    });
  });

  const addAgent = (data: AgentFormData): Agent => {
    // Check for duplicate names
    if (agents.value.some((a) => a.name.toLowerCase() === data.name.toLowerCase())) {
      throw new Error("An agent with this name already exists");
    }

    const newAgent: Agent = {
      id: uuidv4(),
      name: data.name,
      icon: data.name.charAt(0).toUpperCase(),
      type: data.type,
      status: "active",
      role: data.role,
      createdAt: new Date(),
      updatedAt: new Date(),
      config: data.config,
      permissions: ["read", "execute"], // Default permissions
    };

    agents.value.push(newAgent);
    return newAgent;
  };

  const updateAgent = (id: string, data: Partial<Agent>): Agent => {
    const index = agents.value.findIndex((a) => a.id === id);
    if (index === -1) {
      throw new Error("Agent not found");
    }

    // Check for duplicate names if name is being updated
    if (
      data.name &&
      data.name !== agents.value[index].name &&
      agents.value.some((a) => a.name.toLowerCase() === data.name!.toLowerCase())
    ) {
      throw new Error("An agent with this name already exists");
    }

    const updatedAgent = {
      ...agents.value[index],
      ...data,
      updatedAt: new Date(),
    };

    agents.value[index] = updatedAgent;
    return updatedAgent;
  };

  const deleteAgent = (id: string): void => {
    const index = agents.value.findIndex((a) => a.id === id);
    if (index === -1) {
      throw new Error("Agent not found");
    }
    agents.value.splice(index, 1);
  };

  const toggleAgentStatus = (id: string): void => {
    const agent = agents.value.find((a) => a.id === id);
    if (!agent) {
      throw new Error("Agent not found");
    }
    agent.status = agent.status === "active" ? "inactive" : "active";
    agent.updatedAt = new Date();
  };

  const exportAgents = (): string => {
    return JSON.stringify(agents.value, null, 2);
  };

  const importAgents = (data: string): void => {
    try {
      const importedAgents = JSON.parse(data);
      if (!Array.isArray(importedAgents)) {
        throw new Error("Invalid import data format");
      }

      // Validate each agent
      importedAgents.forEach((agent) => {
        if (!agent.name || !agent.role || !agent.type) {
          throw new Error("Invalid agent data");
        }
      });

      agents.value = importedAgents.map((agent) => ({
        ...agent,
        id: uuidv4(), // Generate new IDs for imported agents
        createdAt: new Date(),
        updatedAt: new Date(),
      }));
    } catch (error) {
      throw new Error(`Failed to import agents: ${error}`);
    }
  };

  return {
    agents,
    filter,
    filteredAgents,
    addAgent,
    updateAgent,
    deleteAgent,
    toggleAgentStatus,
    exportAgents,
    importAgents,
  };
}
