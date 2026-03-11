# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal, cast, override

from copilotj.plugin._base import Verbosity
from copilotj.plugin.awt.component import ButtonNode, CanvasNode, CheckboxNode, ChoiceNode, ScrollbarNode, TextFieldNode
from copilotj.plugin.awt.container import ContainerNode, TypedComponentNode
from copilotj.plugin.awt.window._componment import Buttons, CanvasWithLabel, ChoiceWithLabel, ScrollbarWithLabel
from copilotj.plugin.awt.window.awt_window import AwtWindowBase

__all__ = ["IjThresholdAdjuster"]


class IjThresholdAdjuster(AwtWindowBase[Literal["ij.plugin.frame.ThresholdAdjuster"]]):
    """Window of Image > Adjust > Threshold...

    Original description:

    ```
    - dialog0: id=1, type=ij.plugin.frame.ThresholdAdjuster
      ├── Canvas
      ├── Label: text="below: 0.00 %,  above: 8.71 %"
      ├── Scrollbar: value=0, orientation=horizontal
      ├── TextField: text="0"
      ├── Scrollbar: value=48, orientation=horizontal
      ├── TextField: text="48"
      ├── java.awt.Panel
      │   ├── Choice: selected="Huang", items=["Default", "Huang", "Intermodes", "IsoData", "IJ_IsoData", "Li",
    "MaxEntropy", "Mean", "MinError", "Minimum", "Moments", "Otsu", "Percentile", "RenyiEntropy", "Shanbhag",
    "Triangle", "Yen"]
      │   └── Choice: selected="Over/Under", items=["Red", "B&W", "Over/Under"]
      ├── java.awt.Panel
      │   ├── Checkbox: label="Dark background", state=False
      │   ├── Checkbox: label="Stack histogram", state=False
      │   ├── Checkbox: label="Don't reset range", state=False
      │   ├── Checkbox: label="Raw values", state=False
      │   └── Checkbox: label="16-bit histogram", state=False
      └── java.awt.Panel
          ├── Button: label="Auto"
          ├── Button: label="Apply"
          ├── Button: label="Reset"
          └── Button: label="Set"
    ```

    New description:
    ```console
    - dialog1: id=1, type=ij.plugin.frame.ThresholdAdjuster
      ├── Canvas: label="Histogram Canvas"
      ├── Label: text="99.33 %"
      ├── Scrollbar: label="Lower threshold", value=0, orientation=horizontal
      ├── Scrollbar: label="Upper threshold", value=98, orientation=horizontal
      ├── Choice: label="Method", selected="RenyiEntropy", items=["Default", "Huang", "Intermodes", "IsoData",
    "IJ_IsoData", "Li", "MaxEntropy", "Mean", "MinError", "Minimum", "Moments", "Otsu", "Percentile", "RenyiEntropy",
    "Shanbhag", "Triangle", "Yen"]
      ├── Choice: label="Preview mode", selected="Red", items=["Red", "B&W", "Over/Under"]
      ├── Checkbox: label="Dark background", state=False
      ├── Checkbox: label="Stack histogram", state=False
      ├── Checkbox: label="Don't reset range", state=False
      ├── Checkbox: label="Raw values", state=False
      ├── Checkbox: label="16-bit histogram", state=False
      └── Buttons: "Auto", "Apply", "Reset", "Set"
    ````
    """

    @override
    @classmethod
    def _describe_children(
        cls, children: list[TypedComponentNode] | None, *, level: int, verbosity: Verbosity
    ) -> list[str]:
        try:
            new_children = cls._convert_children(children)
            return super()._describe_children(new_children, level=level, verbosity=verbosity)
        except (AssertionError, IndexError):
            return super()._describe_children(children, level=level, verbosity=verbosity)

    @classmethod
    def _convert_children(cls, children: list[TypedComponentNode] | None) -> list[TypedComponentNode]:
        assert children is not None and len(children) == 9

        new_children = []

        # canvas
        canvas = children[0]
        assert isinstance(canvas, CanvasNode)
        new_children.append(CanvasWithLabel(label="Histogram Canvas", **canvas.model_dump()))

        # label
        new_children.append(children[1])

        # scrollbars
        # The text fields next to the scrollbars are redundant, so we'll discard them
        # and give the scrollbars descriptive label.
        # TODO: remove action of text field
        scrollbar1 = children[2]
        textfield1 = children[3]
        assert isinstance(scrollbar1, ScrollbarNode)
        assert isinstance(textfield1, TextFieldNode)
        new_children.append(ScrollbarWithLabel(label="Lower threshold", **scrollbar1.model_dump()))

        scrollbar2 = children[4]
        textfield2 = children[5]
        assert isinstance(scrollbar2, ScrollbarNode)
        assert isinstance(textfield2, TextFieldNode)
        new_children.append(ScrollbarWithLabel(label="Upper threshold", **scrollbar2.model_dump()))

        # Panel with choices
        choices = children[6]
        assert (
            isinstance(choices, ContainerNode)
            and choices.children is not None
            and len(choices.children) == 2
            and all(isinstance(c, ChoiceNode) for c in choices.children)
        )
        new_children.append(ChoiceWithLabel(label="Method", **choices.children[0].model_dump()))
        new_children.append(ChoiceWithLabel(label="Preview mode", **choices.children[1].model_dump()))

        # Panel with checkboxes
        checkboxes = children[7]
        assert (
            isinstance(checkboxes, ContainerNode)
            and checkboxes.children is not None
            and all(isinstance(c, CheckboxNode) for c in checkboxes.children)
        )
        new_children.extend(checkboxes.children)

        # Panel with buttons
        buttons = children[8]
        assert (
            isinstance(buttons, ContainerNode)
            and buttons.children is not None
            and all(isinstance(c, ButtonNode) for c in buttons.children)
        )
        new_children.append(Buttons(*cast(list[ButtonNode], buttons.children)))
        return new_children
