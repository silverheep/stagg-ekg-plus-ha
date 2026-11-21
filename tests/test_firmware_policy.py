"""Firmware allowlist helpers in const.py, tested without Home Assistant.

const.py has no Home Assistant imports, but importing it as part of the package
would run the package __init__ (which needs Home Assistant), so it is loaded by
file path instead.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_CONST = Path(__file__).resolve().parents[1] / "custom_components" / "fellow_stagg" / "const.py"
_spec = importlib.util.spec_from_file_location("fellow_stagg_const", _CONST)
const = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(const)


@pytest.mark.parametrize(
    ("version", "base", "supported"),
    [
        ("1.2.26", "1.2.26", True),
        ("1.2.28", "1.2.28", True),
        ("1.2.26 C", "1.2.26", True),
        ("1.2.28 C", "1.2.28", True),
        ("  1.2.26  ", "1.2.26", True),
        ("\t1.2.28 C\n", "1.2.28", True),
        (None, None, False),
        ("", None, False),
        ("   ", None, False),
        ("1.2.27", "1.2.27", False),
        ("1.2.260", "1.2.260", False),
        ("1.2.2", "1.2.2", False),
        ("11.2.26", "11.2.26", False),
        ("1.2.28SSP", "1.2.28SSP", False),
        ("1.1.76SSP", "1.1.76SSP", False),
        ("1.2.24", "1.2.24", False),
    ],
)
def test_firmware_policy(version, base, supported):
    assert const.firmware_base_version(version) == base
    assert const.is_supported_control_firmware(version) is supported


def test_non_string_never_raises():
    for value in (b"1.2.26", 1.226, 0, [], {}):
        assert const.firmware_base_version(value) is None
        assert const.is_supported_control_firmware(value) is False


def test_allowlist_and_message_text():
    assert const.SUPPORTED_CONTROL_FIRMWARE == frozenset({"1.2.26", "1.2.28"})
    assert const.SUPPORTED_CONTROL_FIRMWARE_TEXT == "1.2.26 and 1.2.28"
