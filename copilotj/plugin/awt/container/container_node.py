# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from abc import ABC
from typing import Literal, override

from copilotj.plugin._base import Verbosity
from copilotj.plugin.awt._base import ComponentBase
from copilotj.plugin.awt.component import (
    ButtonNode,
    CanvasNode,
    CheckboxNode,
    ChoiceNode,
    LabelNode,
    ListNode,
    ScrollbarNode,
    TextAreaNode,
    TextFieldNode,
    UnknownNode,
)

__all__ = ["TypedComponentNode", "ContainerNodeBase", "ContainerNode"]

# NOTE: put typed node here to avoid cycle imports
type TypedComponentNode = "ButtonNode| CanvasNode | CheckboxNode| ChoiceNode| ContainerNode | LabelNode| ListNode | ScrollbarNode | TextAreaNode | TextFieldNode | UnknownNode"


class ContainerNodeBase[T: str](ComponentBase[T], ABC):
    is_container: Literal[True]  # Mark this class as a container, used for pydantic validation
    children: list[TypedComponentNode] | None

    def _describe_one_line(self) -> str:
        """Provides a single-line description for the container itself."""
        return self.type

    @override
    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        """Describe the container and its children in a tree-like structure.

        Generates a multi-line string list representing the container and its children in a tree-like structure.
        """
        # Start with the current container's own one-line description.
        # The 'name' attribute is inherited from ComponentBase and should be set
        # when the node is created if it's available from the Java side.
        # Example: description = f"{self._describe_one_line()} (name='{getattr(self, 'name', 'N/A')}')"
        description = self._describe_one_line()
        lines = [description]
        if verbosity < Verbosity.NORMAL:
            return lines

        lines.extend(self._describe_children(self.children, level=level, verbosity=verbosity))
        return lines

    @classmethod
    def _describe_children(
        cls, children: list[TypedComponentNode] | None, *, level: int, verbosity: Verbosity
    ) -> list[str]:
        lines = []
        num_children = len(children) if children else 0
        for i, child in enumerate(children or []):
            is_last_child = i == num_children - 1

            # Determine the prefix for connecting to the child
            connector_prefix = "└── " if is_last_child else "├── "

            # Recursively get the description lines for the child
            # Pass down the incremented level and the same verbosity
            child_description_lines = child._describe(level=level + 1, verbosity=verbosity)

            if child_description_lines:
                # Add the first line of the child's description with the connector
                lines.append(connector_prefix + child_description_lines[0])

                # Determine the prefix for subsequent lines of this child's description
                # This ensures multi-line descriptions from children are indented correctly
                indentation_prefix = "    " if is_last_child else "│   "
                for child_line in child_description_lines[1:]:
                    lines.append(indentation_prefix + child_line)

        return lines


class ContainerNode(ContainerNodeBase[str]):
    pass
