# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Protocol

import ujson

__all__ = ["IndentedJson", "IndentedRawJson"]


class IndentedJson:
    """A custom formatter for logging that formats JSON data lazily."""

    def __init__(self, data: Any, indent: int = 2):
        super().__init__()
        self._data = data
        self._indent = indent

    def __str__(self):
        return ujson.dumps(self._data, indent=self._indent)


class _StrLike(Protocol):
    def __str__(self) -> str: ...


class IndentedRawJson:
    """A custom formatter for logging that formats JSON data lazily."""

    def __init__(self, data: str | _StrLike, indent: int = 2):
        super().__init__()
        self._data = data
        self._indent = indent

    def __str__(self):
        return ujson.dumps(ujson.loads(str(self._data)), indent=self._indent)
