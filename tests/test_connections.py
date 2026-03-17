# test_connections.py
"""Tests for local member connection release conditions."""

from __future__ import annotations

import pytest

from structural_geometry_2d.exceptions import InvalidIdentifierError, InvalidRestraintError
from structural_geometry_2d.model.connections import Member_connection


def test_member_connection_creation_and_serialization() -> None:
    # Connection states are normalized to lower-case tokens so callers can use
    # readable mixed-case input without changing the stored public state.
    connection = Member_connection(
        "C1",
        "M1",
        " Both ",
        " Rigid ",
        "Flexible",
        "FREE",
        " rigid ",
        " FLEXIBLE ",
        " free ",
    )

    assert connection.name == "C1"
    assert connection.member == "M1"
    assert connection.position == "both"
    assert connection.ux == "rigid"
    assert connection.uy == "flexible"
    assert connection.uz == "free"
    assert connection.rx == "rigid"
    assert connection.ry == "flexible"
    assert connection.rz == "free"
    assert connection.to_dict() == {
        "name": "C1",
        "member": "M1",
        "position": "both",
        "ux": "rigid",
        "uy": "flexible",
        "uz": "free",
        "rx": "rigid",
        "ry": "flexible",
        "rz": "free",
    }
    assert repr(connection) == (
        "Member_connection(name='C1', member='M1', position='both', ux='rigid', "
        "uy='flexible', uz='free', rx='rigid', ry='flexible', rz='free')"
    )


@pytest.mark.parametrize(
    ("connection_name", "member_name"),
    [
        (None, "M1"),
        ("", "M1"),
        ("1C", "M1"),
        ("C-1", "M1"),
        ("C1", None),
        ("C1", ""),
        ("C1", "1M"),
        ("C1", "M-1"),
    ],
)
def test_member_connection_rejects_invalid_identifiers(
    connection_name: object,
    member_name: object,
) -> None:
    with pytest.raises(InvalidIdentifierError):
        Member_connection(
            connection_name,
            member_name,
            "start",
            "rigid",
            "rigid",
            "rigid",
            "rigid",
            "rigid",
            "rigid",
        )


@pytest.mark.parametrize("position", [None, "", "middle", "left"])
def test_member_connection_rejects_invalid_position(position: object) -> None:
    with pytest.raises(ValueError):
        Member_connection(
            "C1",
            "M1",
            position,
            "rigid",
            "rigid",
            "rigid",
            "rigid",
            "rigid",
            "rigid",
        )


@pytest.mark.parametrize(
    ("ux", "uy", "uz", "rx", "ry", "rz"),
    [
        (None, "rigid", "rigid", "rigid", "rigid", "rigid"),
        ("locked", "rigid", "rigid", "rigid", "rigid", "rigid"),
        ("rigid", "", "rigid", "rigid", "rigid", "rigid"),
        ("rigid", "rigid", "spring", "rigid", "rigid", "rigid"),
        ("rigid", "rigid", "rigid", "released", "rigid", "rigid"),
        ("rigid", "rigid", "rigid", "rigid", "semi", "rigid"),
        ("rigid", "rigid", "rigid", "rigid", "rigid", "fixed"),
    ],
)
def test_member_connection_rejects_invalid_condition_values(
    ux: object,
    uy: object,
    uz: object,
    rx: object,
    ry: object,
    rz: object,
) -> None:
    with pytest.raises(InvalidRestraintError):
        Member_connection("C1", "M1", "end", ux, uy, uz, rx, ry, rz)
