# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

import pydantic

__all__ = ["TextMessage", "ImageMessage", "HandoffMessage"]


class TextMessage(pydantic.BaseModel):
    role: Literal["assistant", "system", "user"]
    text: str


class ImageMessage(pydantic.BaseModel):
    role: Literal["assistant", "system", "user"]
    image: str


class HandoffMessage(pydantic.BaseModel):
    target: str
    message: TextMessage | ImageMessage
