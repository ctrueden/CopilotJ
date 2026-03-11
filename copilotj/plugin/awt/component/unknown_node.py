# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from copilotj.plugin.awt._base import ComponentBase, str_or_empty

__all__ = ["UnknownNode"]


class UnknownNode(ComponentBase[str]):
    def _describe_one_line(self) -> str:
        return f"Unknown: type={self.type}, name={str_or_empty(self.name)}"
