# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal, override

from copilotj.plugin._base import Verbosity
from copilotj.plugin.awt.window.awt_window import AwtWindowBase

__all__ = ["IjImageJ"]


class IjImageJ(AwtWindowBase[Literal["ij.ImageJ"]]):
    @override
    def _describe_one_line(self) -> str:
        """Provides a single-line description for the AWT window itself."""
        return "ImageJ Main Window"

    @override
    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        return [self._describe_one_line()]
