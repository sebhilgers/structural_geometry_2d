# test_plot_2d.py
"""Tests for the matplotlib-based 2D plotting helper."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Polygon

from structural_geometry_2d.generators import generate_three_hinged_frame
from structural_geometry_2d.model.connections import Member_connection
from structural_geometry_2d.model.line_member import LineMember
from structural_geometry_2d.model.node import Node
from structural_geometry_2d.model.structural_geometry_2d import StructuralGeometry2D
from structural_geometry_2d.visualization import plot_geometry_2d


def build_frame() -> StructuralGeometry2D:
    """Return the package's canonical frame geometry for plotting checks."""
    return generate_three_hinged_frame(span=20.0, eaves_height=5.0, ridge_height=8.0)


def test_plot_geometry_2d_runs_without_error_for_valid_frame() -> None:
    model = build_frame()

    figure, axes = plot_geometry_2d(model)

    try:
        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)
    finally:
        plt.close(figure)


def test_plot_geometry_2d_draws_members_nodes_and_default_node_labels() -> None:
    model = build_frame()

    figure, axes = plot_geometry_2d(model, show_supports=False)

    try:
        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)
        assert axes.get_xlabel() == "x"
        assert axes.get_ylabel() == "z"

        member_lines = [line for line in axes.lines if line.get_linestyle() == "-"]
        node_lines = [line for line in axes.lines if line.get_marker() == "o"]
        connection_circles = [patch for patch in axes.patches if isinstance(patch, Circle)]

        assert len(member_lines) == len(model.members)
        assert len(node_lines) == 1
        assert list(node_lines[0].get_xdata()) == [node.x for node in model.nodes]
        assert list(node_lines[0].get_ydata()) == [node.z for node in model.nodes]
        assert {text.get_text() for text in axes.texts} == {node.name for node in model.nodes}
        assert len(connection_circles) == len(model.connections)
    finally:
        plt.close(figure)


def test_plot_geometry_2d_optionally_draws_member_names_and_support_symbols() -> None:
    model = build_frame()

    figure, axes = plot_geometry_2d(model, show_member_names=True)

    try:
        plotted_labels = {text.get_text() for text in axes.texts}
        support_triangles = [patch for patch in axes.patches if isinstance(patch, Polygon)]
        connection_circles = [patch for patch in axes.patches if isinstance(patch, Circle)]
        support_base_lines = [
            line
            for line in axes.lines
            if len(line.get_xdata()) == 2
            and max(float(value) for value in line.get_ydata())
            < min(node.z for node in model.nodes)
        ]

        assert {node.name for node in model.nodes}.issubset(plotted_labels)
        assert {member.name for member in model.members}.issubset(plotted_labels)
        assert len(support_triangles) == len(model.supports)
        assert len(connection_circles) == len(model.connections)
        assert len(support_base_lines) == 1
    finally:
        plt.close(figure)


def test_plot_geometry_2d_can_hide_node_and_member_identifiers() -> None:
    model = build_frame()

    figure, axes = plot_geometry_2d(
        model,
        show_node_names=False,
        show_member_names=False,
        show_supports=False,
    )

    try:
        assert len(axes.texts) == 0
    finally:
        plt.close(figure)


def test_plot_geometry_2d_sets_equal_aspect_and_pads_geometry_limits() -> None:
    model = build_frame()

    figure, axes = plot_geometry_2d(model, show_supports=False)

    try:
        x_values = [node.x for node in model.nodes]
        z_values = [node.z for node in model.nodes]
        x_limits = axes.get_xlim()
        z_limits = axes.get_ylim()

        assert axes.get_aspect() == 1.0
        assert x_limits[0] < min(x_values)
        assert x_limits[1] > max(x_values)
        assert z_limits[0] < min(z_values)
        assert z_limits[1] > max(z_values)
    finally:
        plt.close(figure)


def test_plot_geometry_2d_returns_figure_for_empty_geometry() -> None:
    model = StructuralGeometry2D("EmptyFrame")

    figure, axes = plot_geometry_2d(model)

    try:
        assert isinstance(figure, Figure)
        assert isinstance(axes, Axes)
        assert axes.get_xlim() == (-1.0, 1.0)
        assert axes.get_ylim() == (-1.0, 1.0)
        assert len(axes.lines) == 0
        assert len(axes.patches) == 0
        assert len(axes.texts) == 0
    finally:
        plt.close(figure)


def test_plot_geometry_2d_draws_connection_circles_slightly_inward_from_generated_ridge() -> None:
    model = build_frame()

    figure, axes = plot_geometry_2d(model, show_node_names=False, show_member_names=False)

    try:
        connection_circles = [patch for patch in axes.patches if isinstance(patch, Circle)]
        plotted_centers = sorted(
            (round(float(circle.center[0]), 6), round(float(circle.center[1]), 6))
            for circle in connection_circles
        )

        assert plotted_centers == [(9.425304, 7.827591), (10.574696, 7.827591)]
    finally:
        plt.close(figure)


def test_plot_geometry_2d_does_not_draw_connection_circle_without_connections() -> None:
    model = StructuralGeometry2D(
        "SimpleFrame",
        nodes=[Node("N1", 0.0, 0.0), Node("N2", 5.0, 0.0)],
        members=[LineMember("M1", "N1", "N2", "beam")],
    )

    figure, axes = plot_geometry_2d(model, show_supports=False)

    try:
        connection_circles = [patch for patch in axes.patches if isinstance(patch, Circle)]
        assert len(connection_circles) == 0
    finally:
        plt.close(figure)


def test_plot_geometry_2d_draws_connection_circle_for_both_member_positions() -> None:
    model = StructuralGeometry2D(
        "SimpleFrame",
        nodes=[Node("N1", 0.0, 0.0), Node("N2", 5.0, 0.0)],
        members=[LineMember("M1", "N1", "N2", "beam")],
        connections=[
            Member_connection(
                "C1",
                "M1",
                "both",
                "rigid",
                "rigid",
                "rigid",
                "rigid",
                "free",
                "rigid",
            )
        ],
    )

    figure, axes = plot_geometry_2d(
        model,
        show_node_names=False,
        show_member_names=False,
        show_supports=False,
    )

    try:
        connection_circles = [patch for patch in axes.patches if isinstance(patch, Circle)]
        plotted_centers = {
            (round(float(circle.center[0]), 6), round(float(circle.center[1]), 6))
            for circle in connection_circles
        }

        assert plotted_centers == {(0.24, 0.0), (4.76, 0.0)}
    finally:
        plt.close(figure)


def test_plot_geometry_2d_draws_members_correctly_in_arbitrary_order() -> None:
    # Members are intentionally added out of geometric order to verify that the
    # plotting code resolves node coordinates by name rather than by list position.
    model = StructuralGeometry2D(
        "Frame1",
        nodes=[
            Node("N1", 0.0, 0.0),
            Node("N2", 0.0, 5.0),
            Node("N3", 10.0, 8.0),
            Node("N4", 20.0, 5.0),
            Node("N5", 20.0, 0.0),
        ],
        members=[
            LineMember("M3", "N3", "N4", "rafter"),
            LineMember("M1", "N1", "N2", "column"),
            LineMember("M4", "N4", "N5", "column"),
            LineMember("M2", "N2", "N3", "rafter"),
        ],
    )

    figure, axes = plot_geometry_2d(model, show_supports=False)

    try:
        member_lines = [line for line in axes.lines if line.get_linestyle() == "-"]
        plotted_segments = {
            (
                tuple(float(value) for value in line.get_xdata()),
                tuple(float(value) for value in line.get_ydata()),
            )
            for line in member_lines
        }

        assert plotted_segments == {
            ((10.0, 20.0), (8.0, 5.0)),
            ((0.0, 0.0), (0.0, 5.0)),
            ((20.0, 20.0), (5.0, 0.0)),
            ((0.0, 10.0), (5.0, 8.0)),
        }
    finally:
        plt.close(figure)


def test_plot_geometry_2d_places_support_triangle_apex_at_node() -> None:
    model = build_frame()

    figure, axes = plot_geometry_2d(model, show_node_names=False, show_member_names=False)

    try:
        support_triangles = [patch for patch in axes.patches if isinstance(patch, Polygon)]
        support_nodes = {
            support.node_name: next(
                node for node in model.nodes if node.name == support.node_name
            )
            for support in model.supports
        }
        apex_points = {
            (round(float(patch.get_xy()[0][0]), 6), round(float(patch.get_xy()[0][1]), 6))
            for patch in support_triangles
        }

        expected_apex_points = {
            (round(node.x, 6), round(node.z, 6))
            for node in support_nodes.values()
        }

        assert apex_points == expected_apex_points
    finally:
        plt.close(figure)
