# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from copilotj.plugin.awt._base import ComponentBase, str_or_empty

__all__ = ["ListNode"]


class ListNode(ComponentBase[Literal["java.awt.List"]]):
    items: list[str]
    selected_item: str | None  # can be null in Java AWT List

    def _describe_one_line(self) -> str:
        items_str = ", ".join([str_or_empty(item) for item in self.items])
        return f"List: selected={str_or_empty(self.selected_item)}, items=[{items_str}]"
