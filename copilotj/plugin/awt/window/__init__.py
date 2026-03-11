# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from copilotj.plugin.awt.window.awt_window import AwtWindowDifference
from copilotj.plugin.awt.window.ij2_console import Ij2ConsoleWindow
from copilotj.plugin.awt.window.ij_contrast_adjuster import IjContrastAdjuster
from copilotj.plugin.awt.window.ij_generic_dialog import IjGenericDialog
from copilotj.plugin.awt.window.ij_image import (
    IjImage,
    IjImageCaptureResponse,
    IjImageDifference,
    IjImagePreview,
    IjImagePreviewWithInfoResponse,
)
from copilotj.plugin.awt.window.ij_imagej import IjImageJ
from copilotj.plugin.awt.window.ij_text_window import (
    IjTextWindow,
    ResultsTableChunk,
    ResultsTableChunkResponse,
    ResultsTableSummary,
)
from copilotj.plugin.awt.window.ij_threshold_adjuster import IjThresholdAdjuster
from copilotj.plugin.awt.window.unknown_window import UnknownWindow

__all__ = [
    "Ij2ConsoleWindow",
    "IjContrastAdjuster",
    "IjGenericDialog",
    "IjImage",
    "IjImageJ",
    "IjImageDifference",
    "IjTextWindow",
    "IjThresholdAdjuster",
    "IjImageCaptureResponse",
    "IjImagePreview",
    "IjImagePreviewWithInfoResponse",
    "ResultsTableChunk",
    "ResultsTableChunkResponse",
    "ResultsTableSummary",
    "TypedWindow",
    "TypedWindowDifference",
]

type TypedWindow = (
    Ij2ConsoleWindow
    | IjContrastAdjuster
    | IjGenericDialog
    | IjImage
    | IjImageJ
    | IjTextWindow
    | IjThresholdAdjuster
    | UnknownWindow
)
type TypedWindowDifference = IjImageDifference | AwtWindowDifference
