# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from copilotj.plugin.awt._base import ComponentBase

__all__ = ["CanvasNode"]


class CanvasNode(ComponentBase[Literal["java.awt.Canvas"]]):
    def _describe_one_line(self) -> str:
        return "Canvas"
