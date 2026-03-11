# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import re

__all__ = ["truncated_base64_image", "extract_base64_image", "Base64ImageTruncator"]

_re_base64_image = re.compile(r"^data:image\/\w+;base64,")


def truncated_base64_image(data: str, *, max_length: int = 16) -> str:
    match = _re_base64_image.match(data)
    if match:
        prefix = match.group(0)
        content = data[len(prefix) :]
        if len(content) > max_length:
            content = content[: max_length - 3] + "..."
        return prefix + content

    return data


def extract_base64_image(data: str) -> str:
    match = _re_base64_image.match(data)
    if match:
        prefix = match.group(0)
        content = data[len(prefix) :]
        return content

    return data


_re_base64_image_field = re.compile(r'("data:image\/\w+;base64,)([^"]+)(")')


class Base64ImageTruncator:
    def __init__(self, data: str, *, max_length: int = 16) -> None:
        super().__init__()
        self._data = data
        self._max_length = max_length

    def __str__(self) -> str:
        return _re_base64_image_field.sub(self._replacer, self._data)

    def _replacer(self, match):
        prefix, content, suffix = match.groups()
        if len(content) > self._max_length:
            content = content[: self._max_length - 3] + "..."

        return prefix + content + suffix
