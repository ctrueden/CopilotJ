# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import glob
import importlib
import os
import tomllib

from copilotj.core import FunctionTool, ModelClient, Tool
from copilotj.multiagent.Executor import Executor

__all__ = ["load_agent_configs"]

GLOB_PATTERN = os.path.join(os.path.dirname(__file__), "agent_configs", "*_agent.toml")


def load_agent_configs(*, model_client: ModelClient):
    return _load_agent_configs(GLOB_PATTERN, model_client=model_client)


def _load_agent_configs(glob_pattern: str, *, model_client: ModelClient):
    agents = {}
    configs = glob.glob(glob_pattern)
    print(f"Found {len(configs)} configs in {glob_pattern}.")
    for file in configs:
        try:
            with open(file, "rb") as f:
                config = tomllib.load(f)

        except Exception as e:
            print(f"Failed to load {file}: {e}")
            continue

        # Skip files that are commented out or empty
        if not config or config == "pass":
            print(f"Skipping {file}: empty or commented out")
            continue

        if "name" not in config or "class" not in config:
            print(f"Configuration file {file} is missing required 'name' or 'class' field")
            continue

        module_class_str = config["class"]
        module_name, class_name = module_class_str.rsplit(".", 1)
        print(f"Loading agent class {class_name} from module {module_name}...")
        try:
            module = importlib.import_module(module_name)
            agent_class = getattr(module, class_name)
            assert issubclass(agent_class, Executor), f"{agent_class} is not a subclass of Executor"

            name = config["name"]
            description = config.get("description", "")
            prompt = config.get("prompt", "")
            agent_tools_config = config.get("tools", [])

            # Load and prepare tools with descriptions
            agent_tools: list[Tool] = []

            for tool_conf in agent_tools_config:
                tool_name = tool_conf.get("name")
                tool_display_name = tool_conf.get("display_name")
                tool_description = tool_conf.get("description", f"Tool for {tool_name}")

                if "function" in tool_conf:
                    func_full = tool_conf["function"]
                    mod_name, func_name = func_full.rsplit(".", 1)
                    mod = importlib.import_module(mod_name)
                    fn = getattr(mod, func_name)
                    agent_tools.append(
                        FunctionTool(fn, tool_description, name=tool_name, display_name=tool_display_name)
                    )

                elif "class" in tool_conf:
                    class_full = tool_conf["class"]
                    mod_name, tool_class_name = class_full.rsplit(".", 1)
                    mod = importlib.import_module(mod_name)
                    tool_class = getattr(mod, tool_class_name)
                    assert issubclass(tool_class, Tool), f"{tool_class} is not a subclass of Tool"
                    agent_tools.append(tool_class())

                else:
                    print(f"Tool configuration for {tool_name} is missing 'function' or 'class' field")

            print(f"Loaded tools for {name}: {list(agent_tools)}")

            # Create agent instance with tool descriptions
            agents[name] = agent_class(
                name=name, description=description, prompt=prompt, tools=agent_tools, model_client=model_client
            )
            print(f"Successfully loaded agent: {name}")

        except Exception as e:
            print(f"Error loading agent from {file}: {e}")
            import traceback

            traceback.print_exc()

    return agents


if __name__ == "__main__":
    from copilotj.core import load_env, new_model_client

    load_env()

    # Test: Load agent configurations and print each agent's tool list
    print("Loading agent configurations...")
    agent_configs = os.path.join(os.path.dirname(__file__), "agent_configs")
    agents = load_agent_configs(model_client=new_model_client())
    for name, agent in agents.items():
        print(f"Loaded agent: {name}")
        print(
            "Agent tools:",
            getattr(agent, "tools", "No tools attribute"),
            getattr(agent, "tool_descriptions", "No tool descriptions"),
        )
