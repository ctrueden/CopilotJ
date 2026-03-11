# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import os
from typing import TypeAliasType, cast, override

from copilotj.plugin._base import Request, Response, Verbosity

__all__ = ["EnvironmentSummary", "SummariseEnvironmentRequest"]

Plugins = TypeAliasType("Plugins", dict[str, "Plugins | None"])


class EnvironmentSummary(Response):
    imagej_home: str
    java_home: str
    java_version: int
    plugins: Plugins

    @override
    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        heading = "#" * level

        lines = []
        lines.append(f"{heading} Environment Summary")
        lines.append(f"ImageJ home: {self.imagej_home}")
        lines.append(f"Java home: {self.java_home}")
        lines.append(f"Java version: {self.java_version}")
        if verbosity <= Verbosity.LOW:
            types = len(self.plugins)
            total = sum(len(plugins) for plugins in self.plugins.values() if plugins is not None)
            lines.append(f"Plugins: found {total} plugins {types} types")
            return lines

        if verbosity <= Verbosity.NORMAL:
            types = len(self.plugins)
            total = sum(len(plugins) for plugins in self.plugins.values() if plugins is not None)
            lines.append(f"Plugins: found {total} plugins in {types} types:")
            for plugin_type, _ in self.plugins.items():
                lines.append(f"- {plugin_type}")
            return lines

        lines.append(f"{heading}# Plugins")
        if self.plugins and any(len(ps) > 0 for ps in self.plugins.values() if ps is not None):
            flag = False
            for plugin_type, plugins in self.plugins.items():
                for prefix in (
                    "net.imagej.ops.Ops$Math",
                    "net.imagej.display",
                    "net.imagej.ui",
                    "net.imagej.legacy",
                    "org.scijava.ui",
                    "org.scijava.text",
                    "org.scijava.widget",
                    "io.scif",
                ):
                    if plugin_type.startswith(prefix):
                        flag = True
                        break
                else:
                    if plugins:
                        lines.append(f"{heading}## {plugin_type}")
                        lines += self._describe_plugins(plugins)

            if flag:
                lines.append(
                    "Some plugins for basic math, IJ1 compatibility and display/UI "
                    "were found but are hidden to reduce the length of the list."
                )
        else:
            lines.append("No plugins found")

        return lines

    def describe_plugins(self):
        return self._describe_plugins(self.plugins)

    def _describe_plugins(self, plugins: Plugins, prefix: str = ""):
        # TODO: Still possible to group similar plugins together with same prefix
        for name, children in plugins.items():
            if children is None:
                yield f"- {prefix}{name}"
                continue

            # Try to group similar plugins together
            filtered = {k: v for k, v in children.items() if v is None}
            if len(filtered) > 1 and (len(filtered) == len(children) or len(filtered) >= (len(plugins)) // 2):
                keys = list(filtered.keys())
                p, s = _find_common_pre_suffix(keys)
                ks = ", ".join(k[len(p) : len(k) - len(s)] for k in keys)
                yield "- %s%s%s{%s}%s" % (prefix, name, p, ks, s)

                children = cast(Plugins, {k: v for k, v in children.items() if v is not None})

            yield from self._describe_plugins(children, prefix + name)


class SummariseEnvironmentRequest(
    Request[EnvironmentSummary], event="summarise_environment", response_type=EnvironmentSummary
):
    pass


def _find_common_pre_suffix(strings: list[str]) -> tuple[str, str]:
    prefix = os.path.commonprefix(strings)
    suffix = os.path.commonprefix([s[::-1] for s in strings])[::-1]
    return prefix, suffix
