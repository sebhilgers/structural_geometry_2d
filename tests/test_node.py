# test_node.py
"""Tests for the explicit Node model."""

from __future__ import annotations

import pytest

from structural_geometry_2d.exceptions import InvalidIdentifierError
from structural_geometry_2d.model.node import Node


def test_node_creation_and_serialization() -> None:
    # Coordinates are normalized to float so serialized output stays stable.
    node = Node("N_1", 1, 2.5)

    assert node.id == "N_1"
    assert node.x == 1.0
    assert node.z == 2.5
    assert node.to_dict() == {"id": "N_1", "x": 1.0, "z": 2.5}
    assert repr(node) == "Node(id='N_1', x=1.0, z=2.5)"


@pytest.mark.parametrize("node_id", [None, 1, "", "1N", "N-1"])
def test_node_rejects_invalid_identifier(node_id: object) -> None:
    # IDs must fail fast because all higher-level relationships are ID-based.
    with pytest.raises(InvalidIdentifierError):
        Node(node_id, 0.0, 0.0)
