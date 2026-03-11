# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from copilotj.util.json import IndentedJson, IndentedRawJson


# --- Tests for IndentedJson ---
def test_indented_json_basic():
    """Test IndentedJson with a simple dictionary and default indent."""
    data = {"a": 1, "b": "hello"}
    formatter = IndentedJson(data)
    expected_output = """{
  "a": 1,
  "b": "hello"
}"""
    assert str(formatter) == expected_output


def test_indented_json_custom_indent():
    """Test IndentedJson with a list and custom indent."""
    data = [1, 2, {"c": True}]
    formatter = IndentedJson(data, indent=4)
    expected_output = """[
    1,
    2,
    {
        "c": true
    }
]"""
    assert str(formatter) == expected_output


def test_indented_json_empty():
    """Test IndentedJson with empty data."""
    data = {}
    formatter = IndentedJson(data)
    expected_output = "{}"
    assert str(formatter) == expected_output

    data = []
    formatter = IndentedJson(data)
    expected_output = "[]"
    assert str(formatter) == expected_output


# --- Tests for IndentedRawJson ---
class _StrLikeObject:
    def __init__(self, json_string: str):
        self._json_string = json_string

    def __str__(self) -> str:
        return self._json_string


def test_indented_raw_json_string():
    """Test IndentedRawJson with a valid JSON string."""
    raw_json = '{"x": [1, 2], "y": "test"}'
    formatter = IndentedRawJson(raw_json)
    expected_output = """{
  "x": [
    1,
    2
  ],
  "y": "test"
}"""
    assert str(formatter) == expected_output


def test_indented_raw_json_str_like():
    """Test IndentedRawJson with an object having __str__."""
    raw_json_obj = _StrLikeObject('{"z": null, "w": 123}')
    formatter = IndentedRawJson(raw_json_obj)
    expected_output = """{
  "z": null,
  "w": 123
}"""
    assert str(formatter) == expected_output


def test_indented_raw_json_custom_indent():
    """Test IndentedRawJson with custom indent."""
    raw_json = '["a", "b", {"key": "value"}]'
    formatter = IndentedRawJson(raw_json, indent=0)
    expected_output = """["a","b",{"key":"value"}]"""
    assert str(formatter) == expected_output


def test_indented_raw_json_invalid_json():
    """Test IndentedRawJson with invalid JSON input."""
    raw_json = '{"x": [1, 2], "y": "test"'  # Missing closing brace
    formatter = IndentedRawJson(raw_json)
    with pytest.raises(ValueError, match="Unexpected character in found when decoding object value"):
        str(formatter)

    raw_json_obj = _StrLikeObject("invalid json")
    formatter = IndentedRawJson(raw_json_obj)
    with pytest.raises(ValueError, match="Expected object or value"):
        str(formatter)
