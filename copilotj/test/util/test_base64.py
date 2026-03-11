# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from copilotj.util.base64 import Base64ImageTruncator, extract_base64_image, truncated_base64_image


@pytest.mark.parametrize(
    "data, max_length, expected",
    [
        # No truncation needed: valid base64 image but content is short
        ("data:image/png;base64,abc123", 32, "data:image/png;base64,abc123"),
        # Non-base64 image content – should return original string
        ("some random string", 16, "some random string"),
        # Random short text – should return original string even if max_length is small
        ("hello world", 5, "hello world"),
        # Base64 image with long content – should be truncated
        ("data:image/png;base64,abcdefghijklmnopqrstuvwxyz", 16, "data:image/png;base64,abcdefghijklm..."),
        # Base64 image with even longer content – verify truncation
        ("data:image/jpeg;base64," + "a" * 100, 20, "data:image/jpeg;base64," + "a" * 17 + "..."),
        # Base64 image with no content – nothing to truncate
        ("data:image/png;base64,", 10, "data:image/png;base64,"),
    ],
)
def test_truncated_base64_image(data, max_length, expected):
    assert truncated_base64_image(data, max_length=max_length) == expected


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        # Standard base64 image string – should return only the base64 content
        ("data:image/png;base64,abcdef1234567890", "abcdef1234567890"),
        # Non-image base64 string – should return the original string (no match)
        ("data:application/pdf;base64,abcdef1234567890", "data:application/pdf;base64,abcdef1234567890"),
        # Random text – should return the original string
        ("hello world", "hello world"),
        # Empty string – should return empty string
        ("", ""),
        # Only base64 prefix with no actual content – should return empty string
        ("data:image/png;base64,", ""),
        # Valid base64 image string with very short content – should extract it
        ("data:image/jpeg;base64,abc", "abc"),
    ],
)
def test_extract_base64_image(input_data, expected_output):
    assert extract_base64_image(input_data) == expected_output


def test_truncated_base64_image_field_no_truncation():
    json_str = '{"image": "data:image/jpeg;base64,abc123"}'
    field = Base64ImageTruncator(json_str, max_length=32)
    assert str(field) == json_str


def test_truncated_base64_image_field_truncation():
    base64_data = "data:image/jpeg;base64," + "a" * 100
    json_str = '{"image": "' + base64_data + '"}'
    field = Base64ImageTruncator(json_str, max_length=16)
    result = str(field)
    assert "..." in result
    assert "data:image/jpeg;base64," in result
    assert len(result) < len(json_str)


def test_truncated_base64_image_field_other_fields_untouched():
    json_str = '{"name": "avatar", "image": "data:image/jpeg;base64,abc"}'
    field = Base64ImageTruncator(json_str, max_length=8)
    result = str(field)
    assert '"name": "avatar"' in result
    assert '"image": "data:image/jpeg;base64,abc"' in result
