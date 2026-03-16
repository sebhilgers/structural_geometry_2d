# test_three_hinged_frame.py
"""Tests for the fixed three-hinged frame generator."""

from __future__ import annotations

import pytest

from structural_geometry_2d.exceptions import InvalidGeometryError
from structural_geometry_2d.generators import generate_three_hinged_frame


def test_generate_three_hinged_frame_creates_expected_node_coordinates() -> None:
    model = generate_three_hinged_frame(span=20.0, eaves_height=5.0, ridge_height=8.0)

    assert [node.to_dict() for node in model.nodes] == [
        {"id": "N1", "x": 0.0, "z": 0.0},
        {"id": "N2", "x": 0.0, "z": 5.0},
        {"id": "N3", "x": 10.0, "z": 8.0},
        {"id": "N4", "x": 20.0, "z": 5.0},
        {"id": "N5", "x": 20.0, "z": 0.0},
    ]


def test_generate_three_hinged_frame_creates_expected_member_types() -> None:
    model = generate_three_hinged_frame(span=20.0, eaves_height=5.0, ridge_height=8.0)

    assert [member.to_dict() for member in model.members] == [
        {"id": "M1", "start_node_id": "N1", "end_node_id": "N2", "type": "column"},
        {"id": "M2", "start_node_id": "N2", "end_node_id": "N3", "type": "rafter"},
        {"id": "M3", "start_node_id": "N3", "end_node_id": "N4", "type": "rafter"},
        {"id": "M4", "start_node_id": "N4", "end_node_id": "N5", "type": "column"},
    ]


def test_generate_three_hinged_frame_creates_expected_support_conditions() -> None:
    model = generate_three_hinged_frame(span=20.0, eaves_height=5.0, ridge_height=8.0)

    assert [support.to_dict() for support in model.supports] == [
        {"id": "S1", "node_id": "N1", "ux": "fixed", "uz": "fixed", "ry": "free"},
        {"id": "S2", "node_id": "N5", "ux": "free", "uz": "fixed", "ry": "free"},
    ]


def test_generate_three_hinged_frame_returns_valid_model() -> None:
    model = generate_three_hinged_frame(span=24.0, eaves_height=6.0, ridge_height=9.0)

    model.validate()


@pytest.mark.parametrize(
    ("span", "eaves_height", "ridge_height"),
    [
        (0.0, 5.0, 8.0),
        (-1.0, 5.0, 8.0),
        (20.0, 0.0, 8.0),
        (20.0, -5.0, 8.0),
        (20.0, 5.0, 5.0),
        (20.0, 5.0, 4.0),
        (None, 5.0, 8.0),
        (20.0, "5.0", 8.0),
    ],
)
def test_generate_three_hinged_frame_rejects_invalid_geometry_parameters(
    span: object,
    eaves_height: object,
    ridge_height: object,
) -> None:
    with pytest.raises(InvalidGeometryError):
        generate_three_hinged_frame(
            span=span,
            eaves_height=eaves_height,
            ridge_height=ridge_height,
        )
