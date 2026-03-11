# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from copilotj.plugin.awt._base import ComponentBase, str_or_empty

__all__ = ["LabelNode"]


class LabelNode(ComponentBase[Literal["java.awt.Label"]]):
    text: str

    def _describe_one_line(self) -> str:
        return f"Label: text={str_or_empty(self.text)}"
