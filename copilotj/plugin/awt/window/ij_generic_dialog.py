# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal, override

from copilotj.plugin._base import Verbosity
from copilotj.plugin.awt.component import CheckboxNode, ChoiceNode, LabelNode, TextAreaNode, TextFieldNode
from copilotj.plugin.awt.container import TypedComponentNode
from copilotj.plugin.awt.window._componment import ChoiceWithLabel, TextAreaWithLabel, TextFieldWithLabel
from copilotj.plugin.awt.window.awt_window import AwtWindowBase

__all__ = ["IjGenericDialog"]


class IjGenericDialog(AwtWindowBase[Literal["ij.gui.GenericDialog"]]):
    @override
    @classmethod
    def _describe_children(
        cls, children: list[TypedComponentNode] | None, *, level: int, verbosity: Verbosity
    ) -> list[str]:
        if children is None:
            return super()._describe_children(children, level=level, verbosity=verbosity)

        # Generic Dialog has a special case where LabelNode is used to describe the label of the next node
        new_children = []
        i = 0
        while i < len(children):
            node = children[i]
            if isinstance(node, LabelNode) and i + 1 < len(children):
                # If the next child is known node, merge them
                next = children[i + 1]
                if isinstance(next, ChoiceNode):
                    node = ChoiceWithLabel(label=node.text, **next.model_dump())
                    i += 1

                elif isinstance(next, CheckboxNode):
                    if next.label is None:
                        next.label = node.text
                        i += 1

                elif isinstance(next, TextAreaNode):
                    node = TextAreaWithLabel(label=node.text, **next.model_dump())
                    i += 1

                elif isinstance(next, TextFieldNode):
                    node = TextFieldWithLabel(label=node.text, **next.model_dump())
                    i += 1

            new_children.append(node)
            i += 1

        return super()._describe_children(new_children, level=level, verbosity=verbosity)
