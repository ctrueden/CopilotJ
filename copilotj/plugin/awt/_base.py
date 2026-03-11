# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
from typing import override

from copilotj.plugin._base import Response, Verbosity

__all__ = ["ComponentBase", "ActionResponse", "str_or_empty"]


class ComponentBase[T: str](Response, ABC):
    type: T
    name: str | None

    @abstractmethod
    def _describe_one_line(self) -> str: ...

    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        return [self._describe_one_line()]


class ActionResponse[T: str, K: Response | None](Response):
    type: T
    result: K

    @override
    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        if self.result is None:
            return ["success"]

        return self.result._describe(level=level, verbosity=verbosity)


def str_or_empty(value: str | None, *, max_length: int = 300) -> str:
    if value is None or len(value) == 0:
        return "<empty>"

    value = value.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    if len(value) > max_length:
        return f'"{value[:max_length]}..."'

    return f'"{value}"'
