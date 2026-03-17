# projections.py
"""Helpers for projecting structural geometry into the current 2D view."""

from __future__ import annotations

from structural_geometry_2d.model.node import Node


def get_plot_coordinates_xz(node: Node) -> tuple[float, float]:
    """Return the current 2D view as a projection onto the global x-z plane."""
    # The current 2D visualization ignores the global y coordinate on purpose.
    return (node.x, node.z)
