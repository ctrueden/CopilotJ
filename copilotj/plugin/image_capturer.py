# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from copilotj.plugin._base import Request, Response, Verbosity
from copilotj.plugin.awt import IjImagePreview, IjImagePreviewWithInfoResponse

__all__ = ["IjImagePreview", "CaptureImageRequest", "CaptureScreenRequest"]


class ScreenPreviews(Response):
    screenshots: list[IjImagePreview]
    count_screen: int

    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        if self.count_screen == 0 or len(self.screenshots) == 0:
            return ["No screenshots captured."]

        if self.count_screen == 1:
            return self.screenshots[0]._describe(level=level, verbosity=verbosity)

        if verbosity < Verbosity.NORMAL:
            return [f"Captured screenshots: {len(self.screenshots)}"]

        lines = []
        if self.count_screen == len(self.screenshots):
            lines.append(f"Captured screenshots: {len(self.screenshots)}")
        else:
            lines.append(
                f"Captured screenshots: {self.count_screen} "
                f"(total: {len(self.screenshots)}, skipped: {self.count_screen - len(self.screenshots)})"
            )

        for i, screenshot in enumerate(self.screenshots, start=1):
            lines.append(f"Screenshot {i}:")
            lines.extend(screenshot._describe(level=level + 1, verbosity=verbosity))

        return lines


class CaptureScreenRequest(Request[ScreenPreviews], event="capture_screen", response_type=ScreenPreviews, timeout=8):
    pass


class CaptureImageRequest(
    Request[IjImagePreviewWithInfoResponse], event="capture_image", response_type=IjImagePreviewWithInfoResponse
):
    title: str | None = None
