# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import re

__all__ = ["extract_code_block"]

RE_CODE_BLOCK = re.compile(r"```(?:\w+)?\n(.*?)\n```\n*", re.DOTALL)


def extract_code_block(text: str) -> str | None:
    match = RE_CODE_BLOCK.search(text)
    if match is None:
        return None

    return match.group(1)
