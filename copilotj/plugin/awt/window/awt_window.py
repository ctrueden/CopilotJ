# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import override

from copilotj.plugin._base import Response, Verbosity
from copilotj.plugin.awt.container import ContainerNodeBase

__all__ = ["AwtWindowBase", "AwtWindowDifferenceBase", "AwtWindowDifference"]


class AwtWindowBase[T: str](ContainerNodeBase[T]):
    id: int

    @override
    def _describe_one_line(self) -> str:
        """Provides a single-line description for the AWT window itself."""
        return f"{self.name}: id={self.id}, type={self.type}"


class AwtWindowDifferenceBase[T: str](Response):
    id: int
    type: T


class AwtWindowDifference(AwtWindowDifferenceBase[str]):
    @override
    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        return [f"id={self.id}, type={self.type}"]
