# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal, cast, override

from copilotj.plugin._base import Verbosity
from copilotj.plugin.awt.component import ButtonNode, CanvasNode, LabelNode, ScrollbarNode
from copilotj.plugin.awt.container import ContainerNode, TypedComponentNode
from copilotj.plugin.awt.window._componment import Buttons, CanvasWithLabel, ScrollbarWithLabel
from copilotj.plugin.awt.window.awt_window import AwtWindowBase

__all__ = ["IjContrastAdjuster"]


class IjContrastAdjuster(AwtWindowBase[Literal["ij.plugin.frame.ContrastAdjuster"]]):
    """Window of Image > Adjust > Brightness/Contrast

    Original description:

    ```
    - dialog1: id=1, type=ij.plugin.frame.ContrastAdjuster
      ├── Canvas
      ├── java.awt.Panel
      │   ├── Label: text="0"
      │   └── Label: text="255"
      ├── Scrollbar: value=0, orientation=horizontal
      ├── java.awt.Panel
      │   └── Label: text="Minimum"
      ├── Scrollbar: value=255, orientation=horizontal
      ├── java.awt.Panel
      │   └── Label: text="Maximum"
      ├── Scrollbar: value=128, orientation=horizontal
      ├── java.awt.Panel
      │   └── Label: text="Brightness"
      ├── Scrollbar: value=128, orientation=horizontal
      ├── java.awt.Panel
      │   └── Label: text="Contrast"
      └── java.awt.Panel
          ├── Button: label="Auto"
          ├── Button: label="Reset"
          ├── Button: label="Set"
          └── Button: label="Apply"
    ```

    New description:

    ```console
    - dialog1: id=1, type=ij.plugin.frame.ContrastAdjuster
      ├── Canvas
      ├── Label: text="Min: 0, Max: 255"
      ├── Scrollbar: label="Minimum", value=0, orientation=horizontal
      ├── Scrollbar: label="Maximum", value=255, orientation=horizontal
      ├── Scrollbar: label="Brightness", value=128, orientation=horizontal
      ├── Scrollbar: label="Contrast", value=128, orientation=horizontal
      └── Buttons: "Auto", "Reset", "Set", "Apply"
    ```
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
        assert children is not None and len(children) == 11

        new_children = []

        # canvas
        canvas = children[0]
        assert isinstance(canvas, CanvasNode)
        new_children.append(CanvasWithLabel(label="Histogram Canvas", **canvas.model_dump()))

        # minmax label
        panel1 = children[1]
        assert isinstance(panel1, ContainerNode) and panel1.children is not None and len(panel1.children) == 2
        panel1a, panel1b = panel1.children
        assert isinstance(panel1a, LabelNode) and isinstance(panel1b, LabelNode)
        new_children.append(
            LabelNode(type="java.awt.Label", name="minmax", text=f"Min: {panel1a.text}, Max: {panel1b.text}")
        )

        # scrollbars
        for i in range(2, 10, 2):
            scrollbar = children[i]
            panel = children[i + 1]

            assert isinstance(scrollbar, ScrollbarNode)
            assert isinstance(panel, ContainerNode) and panel.children is not None and len(panel.children) == 1

            label_node = panel.children[0]
            assert isinstance(label_node, LabelNode)

            new_children.append(ScrollbarWithLabel(label=label_node.text, **scrollbar.model_dump()))

        # button panel
        buttons = children[10]
        assert (
            isinstance(buttons, ContainerNode)
            and buttons.children is not None
            and all(isinstance(c, ButtonNode) for c in buttons.children)
        )
        new_children.append(Buttons(*cast(list[ButtonNode], buttons.children)))

        return new_children
