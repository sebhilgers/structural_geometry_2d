# plot_2d.py
"""Matplotlib helpers for sketching explicit 2D structural geometry."""

from __future__ import annotations

from math import hypot

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Polygon

from structural_geometry_2d.model.connections import Member_connection
from structural_geometry_2d.model.line_member import LineMember
from structural_geometry_2d.model.node import Node
from structural_geometry_2d.model.structural_geometry_2d import StructuralGeometry2D
from structural_geometry_2d.model.support import Support
from structural_geometry_2d.visualization.projections import get_plot_coordinates_xz


def plot_geometry_2d(
    geometry: StructuralGeometry2D,
    show_node_names: bool = True,
    show_member_names: bool = False,
    show_supports: bool = True,
) -> tuple[Figure, Axes]:
    """Draw a simple x-z sketch of the structural geometry with matplotlib."""
    # The plotting helper is intentionally strict about input type so that
    # downstream failures become explicit and easy to debug.
    if not isinstance(geometry, StructuralGeometry2D):
        raise TypeError("geometry must be an instance of StructuralGeometry2D.")

    # Plotting depends on valid node references, so validation happens up front
    # instead of allowing a later KeyError deep in the drawing code.
    geometry.validate()

    figure, axes = plt.subplots()
    # Member, support, and member-connection relationships are resolved directly
    # from the model's explicit name-based references.
    node_by_name = {node.name: node for node in geometry.nodes}
    member_by_name = {member.name: member for member in geometry.members}

    reference_length = _get_reference_length(geometry.nodes)
    label_offset = max(reference_length * 0.02, 0.1)
    support_offset = max(reference_length * 0.04, 0.2)
    connection_radius = max(reference_length * 0.015, 0.12)

    for member in geometry.members:
        start_node = node_by_name[member.start_node]
        end_node = node_by_name[member.end_node]
        axes.plot(
            [start_node.x, end_node.x],
            [start_node.z, end_node.z],
            color="black",
            linewidth=1.5,
        )

        if show_member_names:
            midpoint_x = (start_node.x + end_node.x) / 2.0
            midpoint_z = (start_node.z + end_node.z) / 2.0
            axes.text(
                midpoint_x,
                midpoint_z + (label_offset * 0.5),
                member.name,
                color="black",
                ha="center",
                va="bottom",
            )

    _plot_nodes(axes, geometry.nodes)

    if show_node_names:
        for node in geometry.nodes:
            axes.text(
                node.x + label_offset,
                node.z + label_offset,
                node.name,
                color="black",
                ha="left",
                va="bottom",
            )

    if show_supports:
        for support in geometry.supports:
            supported_node = node_by_name[support.node_name]
            _draw_support_symbol(axes, supported_node, support, support_offset)

    _draw_member_connection_symbols(
        axes,
        geometry.connections,
        member_by_name,
        node_by_name,
        connection_radius,
    )

    _configure_axes(
        axes,
        geometry.nodes,
        reference_length,
        show_supports,
        geometry.supports,
    )
    return figure, axes


def _plot_nodes(axes: Axes, nodes: list[Node]) -> None:
    """Draw all nodes in one artist so the node set is easy to inspect in tests."""
    if not nodes:
        return

    axes.plot(
        [node.x for node in nodes],
        [node.z for node in nodes],
        linestyle="None",
        marker="o",
        color="black",
        markersize=5,
    )


def _draw_support_symbol(
    axes: Axes,
    node: Node,
    support: Support,
    support_offset: float,
) -> None:
    """Draw a minimal hollow support marker below a node."""
    # The current x-z projection only visualizes the in-plane translational
    # restraints. The stored out-of-plane translation and all rotations are
    # preserved on ``Support`` but are not drawn in this v0.1 sketch.
    if support.uz != "fixed":
        return

    triangle_height = support_offset
    triangle_half_width = max(support_offset * 0.9, 0.25)
    triangle = Polygon(
        [
            (node.x, node.z),
            (node.x - triangle_half_width, node.z - triangle_height),
            (node.x + triangle_half_width, node.z - triangle_height),
        ],
        closed=True,
        fill=False,
        edgecolor="black",
        linewidth=1.0,
    )
    axes.add_patch(triangle)

    if support.ux == "free":
        line_z = node.z - triangle_height - (support_offset * 0.35)
        line_half_width = max(triangle_half_width * 0.95, 0.25)
        axes.plot(
            [node.x - line_half_width, node.x + line_half_width],
            [line_z, line_z],
            color="black",
            linewidth=1.0,
        )


def _draw_member_connection_symbols(
    axes: Axes,
    connections: list[Member_connection],
    member_by_name: dict[str, LineMember],
    node_by_name: dict[str, Node],
    connection_radius: float,
) -> None:
    """Draw a hollow circle at each member-end connection location."""
    for connection in connections:
        member = member_by_name[connection.member]
        start_node = node_by_name[member.start_node]
        end_node = node_by_name[member.end_node]
        for center_x, center_z in _get_connection_symbol_centers(
            start_node,
            end_node,
            connection.position,
            connection_radius,
        ):
            circle = Circle(
                (center_x, center_z),
                radius=connection_radius,
                fill=False,
                edgecolor="black",
                linewidth=1.0,
            )
            axes.add_patch(circle)


def _get_connection_symbol_centers(
    start_node: Node,
    end_node: Node,
    position: str,
    connection_radius: float,
) -> list[tuple[float, float]]:
    """Return inward-shifted connection centers along the member axis."""
    start_x, start_z = get_plot_coordinates_xz(start_node)
    end_x, end_z = get_plot_coordinates_xz(end_node)
    delta_x = end_x - start_x
    delta_z = end_z - start_z
    member_length = hypot(delta_x, delta_z)

    if member_length == 0.0:
        if position == "start":
            return [(start_x, start_z)]
        if position == "end":
            return [(end_x, end_z)]
        return [(start_x, start_z), (end_x, end_z)]

    # Move the circle slightly inward so the node marker stays visible and the
    # connection reads as belonging to the member end rather than covering it.
    inward_offset = min(connection_radius * 2.0, member_length * 0.35)
    unit_x = delta_x / member_length
    unit_z = delta_z / member_length

    start_center = (start_x + (unit_x * inward_offset), start_z + (unit_z * inward_offset))
    end_center = (end_x - (unit_x * inward_offset), end_z - (unit_z * inward_offset))

    if position == "start":
        return [start_center]
    if position == "end":
        return [end_center]
    return [start_center, end_center]


def _configure_axes(
    axes: Axes,
    nodes: list[Node],
    reference_length: float,
    show_supports: bool,
    supports: list[Support],
) -> None:
    """Apply consistent axis labels, aspect ratio, and margins."""
    axes.set_xlabel("x")
    axes.set_ylabel("z")
    # Equal x-z scaling keeps members visually true to the underlying geometry
    # so lengths and angles are not distorted by the plot.
    axes.set_aspect("equal")
    axes.grid(False)

    if not nodes:
        axes.set_xlim(-1.0, 1.0)
        axes.set_ylim(-1.0, 1.0)
        return

    x_values = [node.x for node in nodes]
    z_values = [node.z for node in nodes]

    padding = max(reference_length * 0.1, 0.5)
    support_padding = 0.0
    if show_supports and supports:
        support_padding = max(reference_length * 0.12, 0.6)

    axes.set_xlim(min(x_values) - padding, max(x_values) + padding)
    axes.set_ylim(
        min(z_values) - padding - support_padding,
        max(z_values) + padding,
    )


def _get_reference_length(nodes: list[Node]) -> float:
    """Return a stable plotting scale based on the geometry extents."""
    if not nodes:
        return 1.0

    x_values = [node.x for node in nodes]
    z_values = [node.z for node in nodes]
    width = max(x_values) - min(x_values)
    height = max(z_values) - min(z_values)
    return max(width, height, 1.0)
