# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import cast, override

from copilotj.plugin._base import Verbosity
from copilotj.plugin.awt._base import str_or_empty
from copilotj.plugin.awt.component.button_node import ButtonNode
from copilotj.plugin.awt.component.canvas_node import CanvasNode
from copilotj.plugin.awt.component.choice_node import ChoiceNode
from copilotj.plugin.awt.component.scrollbar_node import ScrollbarNode
from copilotj.plugin.awt.component.text_area_node import TextAreaNode
from copilotj.plugin.awt.component.text_field_node import TextFieldNode
from copilotj.plugin.awt.container.container_node import ContainerNodeBase, TypedComponentNode

__all__ = [
    "Buttons",
    "CanvasWithLabel",
    "ChoiceWithLabel",
    "ScrollbarWithLabel",
    "TextAreaWithLabel",
    "TextFieldWithLabel",
]


class Buttons(ContainerNodeBase[str]):
    def __init__(self, *children: ButtonNode):
        assert all(isinstance(a, ButtonNode) for a in children), "All children must be ButtonNode instances"
        super().__init__(type="copilotj.Buttons", name="Buttons", is_container=True, children=list(children))

    @override
    def _describe_one_line(self) -> str:
        buttons = cast(list[ButtonNode], self.children or [])
        return f"Buttons: {', '.join([str_or_empty(button.label) for button in buttons])}"

    @override
    @classmethod
    def _describe_children(
        cls, children: list[TypedComponentNode] | None, *, level: int, verbosity: Verbosity
    ) -> list[str]:
        return []


class CanvasWithLabel(CanvasNode):
    label: str

    @override
    def _describe_one_line(self) -> str:
        return f"Canvas: label={str_or_empty(self.label)}"


class ChoiceWithLabel(ChoiceNode):
    label: str

    @override
    def _describe_one_line(self) -> str:
        items_str = ", ".join([str_or_empty(item) for item in self.items])
        return f"Choice: label={str_or_empty(self.label)}, selected={str_or_empty(self.selected_item)}, items=[{items_str}]"


class ScrollbarWithLabel(ScrollbarNode):
    label: str

    @override
    def _describe_one_line(self) -> str:
        return f"Scrollbar: label={str_or_empty(self.label)}, value={self.value}, orientation={self.orientation}"


class TextAreaWithLabel(TextAreaNode):
    label: str

    @override
    def _describe_one_line(self) -> str:
        return f"TextArea: label={str_or_empty(self.label)}, text={str_or_empty(self.text)}"


class TextFieldWithLabel(TextFieldNode):
    label: str

    @override
    def _describe_one_line(self) -> str:
        return f"TextField: label={str_or_empty(self.label)}, text={str_or_empty(self.text)}"
