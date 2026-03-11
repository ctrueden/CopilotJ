# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from copilotj.plugin.awt._base import ActionResponse, ComponentBase, str_or_empty

__all__ = ["TextFieldNode", "TextFieldSetTextResponse"]


class TextFieldNode(ComponentBase[Literal["java.awt.TextField"]]):
    text: str | None  # text can be null if component.getText() is null

    def _describe_one_line(self) -> str:
        return f"TextField: text={str_or_empty(self.text)}"


type TextFieldSetTextResponse = ActionResponse[Literal["java.awt.TextField.setText"], None]
