# test_projections.py
"""Tests for the x-z projection helper used by 2D visualization code."""

from __future__ import annotations

from structural_geometry_2d.model.node import Node
from structural_geometry_2d.visualization.projections import get_plot_coordinates_xz


def test_get_plot_coordinates_xz_returns_node_x_and_z() -> None:
    # The helper must project onto the global x-z plane, so y is ignored.
    node = Node("N1", 3.5, 7.25, y=-4.0)

    assert get_plot_coordinates_xz(node) == (3.5, 7.25)
