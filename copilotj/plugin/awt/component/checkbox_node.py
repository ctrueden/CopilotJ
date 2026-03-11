# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from copilotj.plugin.awt._base import ActionResponse, ComponentBase, str_or_empty

__all__ = ["CheckboxNode", "CheckboxSetStateResponse"]


class CheckboxNode(ComponentBase[Literal["java.awt.Checkbox"]]):
    label: str | None
    state: bool

    def _describe_one_line(self) -> str:
        return f"Checkbox: label={str_or_empty(self.label)}, state={self.state}"


type CheckboxSetStateResponse = ActionResponse[Literal["java.awt.Checkbox.setState"], None]
