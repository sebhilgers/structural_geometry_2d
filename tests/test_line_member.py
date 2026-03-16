# test_line_member.py
"""Tests for the explicit LineMember model."""

from __future__ import annotations

import pytest

from structural_geometry_2d.exceptions import InvalidGeometryError, InvalidIdentifierError
from structural_geometry_2d.model.line_member import LineMember


def test_line_member_creation_and_serialization() -> None:
    # Member types are stripped so callers can pass readable input without
    # affecting the normalized value stored in the model.
    member = LineMember("M1", "N1", "N2", "  column  ")

    assert member.id == "M1"
    assert member.start_node_id == "N1"
    assert member.end_node_id == "N2"
    assert member.member_type == "column"
    assert member.type == "column"
    assert member.to_dict() == {
        "id": "M1",
        "start_node_id": "N1",
        "end_node_id": "N2",
        "type": "column",
    }
    assert (
        repr(member)
        == "LineMember(id='M1', start_node_id='N1', end_node_id='N2', member_type='column')"
    )


@pytest.mark.parametrize(
    ("member_id", "start_node_id", "end_node_id"),
    [
        (None, "N1", "N2"),
        ("", "N1", "N2"),
        ("1M", "N1", "N2"),
        ("M-1", "N1", "N2"),
        ("M1", None, "N2"),
        ("M1", "", "N2"),
        ("M1", "1N", "N2"),
        ("M1", "N-1", "N2"),
        ("M1", "N1", None),
        ("M1", "N1", ""),
        ("M1", "N1", "2N"),
        ("M1", "N1", "N-2"),
    ],
)
def test_line_member_rejects_invalid_identifiers(
    member_id: object,
    start_node_id: object,
    end_node_id: object,
) -> None:
    # The constructor validates every identifier because container validation
    # assumes member and reference IDs already have a supported format.
    with pytest.raises(InvalidIdentifierError):
        LineMember(member_id, start_node_id, end_node_id, "column")


def test_line_member_rejects_same_start_and_end_node() -> None:
    with pytest.raises(InvalidGeometryError):
        LineMember("M1", "N1", "N1", "column")
