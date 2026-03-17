# three_hinged_frame.py
"""Generate a fixed three-hinged frame in the global XZ plane."""

from __future__ import annotations

import math

from structural_geometry_2d.exceptions import InvalidGeometryError
from structural_geometry_2d.model.line_member import LineMember
from structural_geometry_2d.model.node import Node
from structural_geometry_2d.model.structural_geometry_2d import StructuralGeometry2D
from structural_geometry_2d.model.support import Support


def generate_three_hinged_frame(
    span: float,
    eaves_height: float,
    ridge_height: float,
    structure_id: str = "ThreeHingedFrame",
) -> StructuralGeometry2D:
    """Return a deterministic three-hinged frame model with fixed IDs."""
    # The generator is intentionally explicit so its output is easy to inspect
    # and compare in tests and debug JSON dumps.
    validated_span = _validate_positive_parameter("span", span)
    validated_eaves_height = _validate_positive_parameter("eaves_height", eaves_height)
    validated_ridge_height = _validate_positive_parameter("ridge_height", ridge_height)

    if validated_ridge_height <= validated_eaves_height:
        raise InvalidGeometryError("ridge_height must be greater than eaves_height.")

    nodes = [
        Node("N1", 0.0, 0.0),
        Node("N2", 0.0, validated_eaves_height),
        Node("N3", validated_span / 2.0, validated_ridge_height),
        Node("N4", validated_span, validated_eaves_height),
        Node("N5", validated_span, 0.0),
    ]

    members = [
        LineMember("M1", "N1", "N2", "column"),
        LineMember("M2", "N2", "N3", "rafter"),
        LineMember("M3", "N3", "N4", "rafter"),
        LineMember("M4", "N4", "N5", "column"),
    ]

    supports = [
        Support("S1", "N1", "fixed", "fixed", "free"),
        Support("S2", "N5", "free", "fixed", "free"),
    ]

    model = StructuralGeometry2D(
        structure_name=structure_id,
        nodes=nodes,
        members=members,
        supports=supports,
    )
    model.validate()
    return model


def _validate_positive_parameter(name: str, value: float) -> float:
    """Validate one geometric generator parameter and return it as float."""
    # Generator inputs are geometric dimensions, so invalid values should map
    # to the package's geometry validation error instead of generic built-ins.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InvalidGeometryError(f"{name} must be a numeric value.")

    numeric_value = float(value)
    if not math.isfinite(numeric_value):
        raise InvalidGeometryError(f"{name} must be finite.")
    if numeric_value <= 0.0:
        raise InvalidGeometryError(f"{name} must be greater than zero.")
    return numeric_value
