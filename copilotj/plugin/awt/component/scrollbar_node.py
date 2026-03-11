# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from copilotj.plugin.awt._base import ComponentBase

__all__ = ["ScrollbarNode"]


class ScrollbarNode(ComponentBase[Literal["java.awt.Scrollbar"]]):
    value: int
    orientation: Literal["horizontal", "vertical"]

    def _describe_one_line(self) -> str:
        return f"Scrollbar: value={self.value}, orientation={self.orientation}"
