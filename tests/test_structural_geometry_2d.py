# test_structural_geometry_2d.py
"""Tests for the explicit StructuralGeometry2D container."""

from __future__ import annotations

import json

import pytest

from structural_geometry_2d.exceptions import (
    DuplicateIdentifierError,
    InvalidGeometryError,
    InvalidIdentifierError,
    MissingReferenceError,
)
from structural_geometry_2d.model.line_member import LineMember
from structural_geometry_2d.model.node import Node
from structural_geometry_2d.model.structural_geometry_2d import StructuralGeometry2D
from structural_geometry_2d.model.support import Support


def build_valid_model() -> StructuralGeometry2D:
    # A small valid frame keeps all container tests anchored to the same
    # reference geometry and support conditions.
    return StructuralGeometry2D(
        "Frame1",
        nodes=[
            Node("N1", 0.0, 0.0),
            Node("N2", 0.0, 5.0),
        ],
        members=[LineMember("M1", "N1", "N2", "column")],
        supports=[Support("S1", "N1", "fixed", "fixed", "free")],
    )


def test_structural_geometry_2d_to_dict_repr_and_json() -> None:
    model = build_valid_model()

    assert model.to_dict() == {
        "id": "Frame1",
        "nodes": [
            {"name": "N1", "x": 0.0, "y": 0.0, "z": 0.0},
            {"name": "N2", "x": 0.0, "y": 0.0, "z": 5.0},
        ],
        "members": [
            {"name": "M1", "start_node": "N1", "end_node": "N2", "type": "column"}
        ],
        "supports": [
            {"id": "S1", "node_name": "N1", "ux": "fixed", "uz": "fixed", "ry": "free"}
        ],
    }
    assert json.loads(model.to_json()) == model.to_dict()
    assert repr(model) == "StructuralGeometry2D(id='Frame1', nodes=2, members=1, supports=1)"


def test_structural_geometry_2d_add_methods_and_line_member_alias() -> None:
    model = StructuralGeometry2D("Frame1")
    node_1 = Node("N1", 0.0, 0.0)
    node_2 = Node("N2", 0.0, 5.0)
    member = LineMember("M1", "N1", "N2", "column")
    support = Support("S1", "N1", "fixed", "fixed", "free")

    model.add_node(node_1)
    model.add_node(node_2)
    model.add_member(member)
    model.add_support(support)

    assert model.nodes == [node_1, node_2]
    assert model.members == [member]
    assert model.line_members is model.members
    assert model.supports == [support]


@pytest.mark.parametrize("structure_id", [None, 1, "", "1Frame", "Frame-1"])
def test_structural_geometry_2d_rejects_invalid_structure_identifier(structure_id: object) -> None:
    with pytest.raises(InvalidIdentifierError):
        StructuralGeometry2D(structure_id)


def test_structural_geometry_2d_validate_accepts_valid_model() -> None:
    model = build_valid_model()

    model.validate()


def test_structural_geometry_2d_validate_accepts_node_name_references() -> None:
    model = StructuralGeometry2D(
        "Frame1",
        nodes=[Node("N1", 0.0, 0.0), Node("N2", 0.0, 5.0)],
        members=[LineMember("M1", "N1", "N2", "column")],
        supports=[Support("S1", "N1", "fixed", "fixed", "free")],
    )

    model.validate()


def test_structural_geometry_2d_validate_rejects_duplicate_node_names() -> None:
    model = StructuralGeometry2D(
        "Frame1",
        nodes=[Node("N1", 0.0, 0.0), Node("N1", 1.0, 1.0)],
    )

    with pytest.raises(DuplicateIdentifierError):
        model.validate()


def test_structural_geometry_2d_validate_rejects_duplicate_member_names() -> None:
    model = StructuralGeometry2D(
        "Frame1",
        nodes=[Node("N1", 0.0, 0.0), Node("N2", 0.0, 5.0), Node("N3", 1.0, 5.0)],
        members=[
            LineMember("M1", "N1", "N2", "column"),
            LineMember("M1", "N2", "N3", "rafter"),
        ],
    )

    with pytest.raises(DuplicateIdentifierError):
        model.validate()


def test_structural_geometry_2d_validate_rejects_duplicate_support_ids() -> None:
    model = StructuralGeometry2D(
        "Frame1",
        nodes=[Node("N1", 0.0, 0.0), Node("N2", 0.0, 5.0)],
        supports=[
            Support("S1", "N1", "fixed", "fixed", "free"),
            Support("S1", "N2", "free", "fixed", "free"),
        ],
    )

    with pytest.raises(DuplicateIdentifierError):
        model.validate()


def test_structural_geometry_2d_validate_rejects_missing_start_node_reference_in_member() -> None:
    model = StructuralGeometry2D(
        "Frame1",
        nodes=[Node("N1", 0.0, 0.0)],
        members=[LineMember("M1", "N2", "N1", "column")],
    )

    with pytest.raises(MissingReferenceError):
        model.validate()


def test_structural_geometry_2d_validate_rejects_missing_end_node_reference_in_member() -> None:
    model = StructuralGeometry2D(
        "Frame1",
        nodes=[Node("N1", 0.0, 0.0)],
        members=[LineMember("M1", "N1", "N2", "column")],
    )

    with pytest.raises(MissingReferenceError):
        model.validate()


def test_structural_geometry_2d_validate_rejects_missing_node_reference_in_support() -> None:
    model = StructuralGeometry2D(
        "Frame1",
        nodes=[Node("NodeOne", 0.0, 0.0)],
        supports=[Support("S1", "N2", "fixed", "fixed", "free")],
    )

    with pytest.raises(MissingReferenceError):
        model.validate()


def test_structural_geometry_2d_validate_rejects_same_member_endpoints_after_mutation() -> None:
    # Container validation still guards geometry consistency even if a public
    # member object is modified after construction.
    member = LineMember("M1", "N1", "N2", "column")
    member.end_node = "N1"
    model = StructuralGeometry2D(
        "Frame1",
        nodes=[Node("N1", 0.0, 0.0), Node("N2", 0.0, 5.0)],
        members=[member],
    )

    with pytest.raises(InvalidGeometryError):
        model.validate()
