# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal, override

from copilotj.plugin._base import Verbosity
from copilotj.plugin.awt.window.awt_window import AwtWindowBase

__all__ = ["Ij2ConsoleWindow"]

type TYPE = Literal["ij.Console"]


class Ij2ConsoleWindow(AwtWindowBase[Literal["ij.Console"]]):
    @override
    def _describe_one_line(self) -> str:
        return "ImageJ Console"

    @override
    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        return [self._describe_one_line()]
