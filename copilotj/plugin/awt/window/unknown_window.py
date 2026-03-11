# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from copilotj.plugin.awt.window.awt_window import AwtWindowBase

__all__ = ["UnknownWindow"]


class UnknownWindow(AwtWindowBase[str]):
    pass
