# test_support.py
"""Tests for the explicit Support model."""

from __future__ import annotations

import pytest

from structural_geometry_2d.exceptions import InvalidIdentifierError, InvalidRestraintError
from structural_geometry_2d.model.support import Support


def test_support_creation_and_serialization() -> None:
    # Restraints are normalized to lower-case tokens so callers can provide
    # readable input without changing the stored public state.
    support = Support("S1", "N1", " Fixed ", "FIXED", " free ")

    assert support.id == "S1"
    assert support.node_id == "N1"
    assert support.ux == "fixed"
    assert support.uz == "fixed"
    assert support.ry == "free"
    assert support.to_dict() == {
        "id": "S1",
        "node_id": "N1",
        "ux": "fixed",
        "uz": "fixed",
        "ry": "free",
    }
    assert repr(support) == "Support(id='S1', node_id='N1', ux='fixed', uz='fixed', ry='free')"


@pytest.mark.parametrize(
    ("support_id", "node_id"),
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
def test_support_rejects_invalid_identifiers(support_id: object, node_id: object) -> None:
    # Support IDs and node references use the same validation contract because
    # support connectivity is expressed only through string identifiers.
    with pytest.raises(InvalidIdentifierError):
        Support(support_id, node_id, "fixed", "fixed", "free")


@pytest.mark.parametrize(
    ("ux", "uz", "ry"),
    [
        (None, "fixed", "free"),
        ("locked", "fixed", "free"),
        ("fixed", "", "free"),
        ("fixed", "roller", "free"),
        ("fixed", "free", "pin"),
    ],
)
def test_support_rejects_invalid_restraint_values(ux: object, uz: object, ry: object) -> None:
    with pytest.raises(InvalidRestraintError):
        Support("S1", "N1", ux, uz, ry)
