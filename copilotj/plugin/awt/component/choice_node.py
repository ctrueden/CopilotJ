# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from copilotj.plugin.awt._base import ActionResponse, ComponentBase, str_or_empty

__all__ = ["ChoiceNode", "ChoiceSelectItemResponse"]


class ChoiceNode(ComponentBase[Literal["java.awt.Choice"]]):
    items: list[str]
    selected_item: str

    def _describe_one_line(self) -> str:
        items_str = ", ".join([str_or_empty(item) for item in self.items])
        return f"Choice: selected={str_or_empty(self.selected_item)}, items=[{items_str}]"


type ChoiceSelectItemResponse = ActionResponse[Literal["java.awt.Choice.selectItem"], None]
