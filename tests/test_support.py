# test_support.py
"""Tests for the explicit Support model."""

from __future__ import annotations

import pytest

from structural_geometry_2d.exceptions import InvalidIdentifierError, InvalidRestraintError
from structural_geometry_2d.model.support import Support


def test_support_creation_and_serialization() -> None:
    # Restraints are normalized to lower-case tokens so callers can provide
    # readable input without changing the stored public state.
    support = Support("S1", "N1", " Fixed ", " fixed ", "FIXED", " free ", " FREE ", "free ")

    assert support.name == "S1"
    assert support.node_name == "N1"
    assert support.ux == "fixed"
    assert support.uy == "fixed"
    assert support.uz == "fixed"
    assert support.rx == "free"
    assert support.ry == "free"
    assert support.rz == "free"
    assert support.to_dict() == {
        "name": "S1",
        "node_name": "N1",
        "ux": "fixed",
        "uy": "fixed",
        "uz": "fixed",
        "rx": "free",
        "ry": "free",
        "rz": "free",
    }
    assert repr(support) == (
        "Support(support_name='S1', node_name='N1', ux='fixed', uy='fixed', "
        "uz='fixed', rx='free', ry='free', rz='free')"
    )


@pytest.mark.parametrize(
    ("support_id", "node_name"),
    [
        (None, "N1"),
        ("", "N1"),
        ("1S", "N1"),
        ("S-1", "N1"),
        ("S1", None),
        ("S1", ""),
        ("S1", "1N"),
        ("S1", "N-1"),
    ],
)
def test_support_rejects_invalid_identifiers(support_id: object, node_name: object) -> None:
    # Support IDs and node-name references use the same validation contract
    # because support connectivity is expressed only through explicit strings.
    with pytest.raises(InvalidIdentifierError):
        Support(support_id, node_name, "fixed", "fixed", "fixed", "free", "free", "free")


@pytest.mark.parametrize(
    ("ux", "uy", "uz", "rx", "ry", "rz"),
    [
        (None, "fixed", "fixed", "free", "free", "free"),
        ("fixed", "locked", "fixed", "free", "free", "free"),
        ("fixed", "fixed", "", "free", "free", "free"),
        ("fixed", "fixed", "fixed", "roller", "free", "free"),
        ("fixed", "fixed", "fixed", "free", "pin", "free"),
        ("fixed", "fixed", "fixed", "free", "free", "locked"),
    ],
)
def test_support_rejects_invalid_restraint_values(
    ux: object,
    uy: object,
    uz: object,
    rx: object,
    ry: object,
    rz: object,
) -> None:
    with pytest.raises(InvalidRestraintError):
        Support("S1", "N1", ux, uy, uz, rx, ry, rz)
