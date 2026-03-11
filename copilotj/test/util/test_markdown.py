# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from copilotj.util.markdown import extract_code_block


@pytest.mark.parametrize(
    "text, excepted",
    [
        ("```\nHello, world!\n```", "Hello, world!"),
        ("```\nHello, world!\n```\n", "Hello, world!"),
        ("```\nHello, \nworld!\n```\n", "Hello, \nworld!"),
        ("```python\nHello, world!\n```", "Hello, world!"),
        ("```python\n#Hello, \nworld!\n```\n", "#Hello, \nworld!"),
        ("```javascript\n//Hello, \nworld!\n```\n", "//Hello, \nworld!"),
        ("Hello```\n\n\n```\nWorld", "\n"),
        ("Hello```\n\n```\nWorld", ""),
        ("Hello```\n```\nWorld", None),
        ("Hello```\n``\n```World", "``"),
        ("````\nHello, world!\n````", "Hello, world!"),
        ("Hello, world!", None),
        (
            """\
Thoughts: In ImageJ, you can check the number of currently opened windows using \
the `getNumberOfWindows` function. This function returns the count of open image \
windows, which can be useful for various purposes in macros.

Code:
```macro
// Macro to count the number of open windows in ImageJ
numWindows = getNumberOfWindows();
print("Number of open windows: " + numWindows);
```
""",
            """\
// Macro to count the number of open windows in ImageJ
numWindows = getNumberOfWindows();
print("Number of open windows: " + numWindows);\
""",
        ),
    ],
)
def test_extract_code_block(text: str, excepted: str | None):
    assert extract_code_block(text) == excepted
