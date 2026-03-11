# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from copilotj.plugin.awt._base import ActionResponse, ComponentBase, str_or_empty

__all__ = ["ButtonNode", "ButtonClickResponse"]


class ButtonNode(ComponentBase[Literal["java.awt.Button"]]):
    label: str

    def _describe_one_line(self) -> str:
        return f"Button: label={str_or_empty(self.label)}"


ButtonClickResponse = ActionResponse[Literal["java.awt.Button.click"], None]
