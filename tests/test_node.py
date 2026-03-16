# test_node.py
"""Tests for the explicit Node model."""

from __future__ import annotations

import pytest

from structural_geometry_2d.exceptions import InvalidIdentifierError
from structural_geometry_2d.model.node import Node


def test_node_creation_and_serialization() -> None:
    # Coordinates are normalized to float so serialized output stays stable,
    # while the node name becomes the fallback reference when id is blank.
    node = Node("N_1", 1, 2.5)

    assert node.name == "N_1"
    assert node.id == ""
    assert node.reference_id == "N_1"
    assert node.x == 1.0
    assert node.y == 0.0
    assert node.z == 2.5
    assert node.to_dict() == {
        "name": "N_1",
        "id": "",
        "x": 1.0,
        "y": 0.0,
        "z": 2.5,
    }
    assert repr(node) == "Node(name='N_1', id='', x=1.0, y=0.0, z=2.5)"


def test_node_accepts_explicit_id_and_y_coordinate() -> None:
    node = Node("LeftBase", 1.0, 2.0, y=-3.5, id="N1")

    assert node.name == "LeftBase"
    assert node.id == "N1"
    assert node.reference_id == "N1"
    assert node.x == 1.0
    assert node.y == -3.5
    assert node.z == 2.0


@pytest.mark.parametrize("name", [None, 1, "", "1N", "N-1"])
def test_node_rejects_invalid_name(name: object) -> None:
    with pytest.raises(InvalidIdentifierError):
        Node(name, 0.0, 0.0)


@pytest.mark.parametrize("id", [None, 1, "1N", "N-1"])
def test_node_rejects_invalid_explicit_id(id: object) -> None:
    with pytest.raises(InvalidIdentifierError):
        Node("N1", 0.0, 0.0, id=id)
