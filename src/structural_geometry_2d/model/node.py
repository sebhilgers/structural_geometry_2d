# node.py
"""Explicit node model used by the v0.1 structural geometry package."""

from __future__ import annotations

import re
from typing import Any

from structural_geometry_2d.exceptions import InvalidIdentifierError


_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class Node:
    """Represents a 2D node with explicit name and optional ID."""

    def __init__(
        self,
        name: str,
        x: float,
        z: float,
        y: float = 0.0,
        id: str = "",
    ) -> None:
        # Names are required and intentionally follow the same restricted
        # format as other identifiers so they can act as a stable fallback
        # reference key while optional node IDs are introduced gradually.
        self.name = self._validate_name(name)
        self.id = self._validate_optional_id(id)

        # Coordinates are stored as floats to keep serialization predictable
        # and to avoid int/float branching in downstream code and tests.
        self.x = self._validate_coordinate("x", x)
        self.y = self._validate_coordinate("y", y)
        self.z = self._validate_coordinate("z", z)

    @property
    def reference_id(self) -> str:
        """Return the ID used by members and supports to reference this node."""
        # The explicit node ID is preferred when present. Otherwise the name
        # acts as the stable reference token so legacy ID-based relations keep
        # working while the public constructor moves from node_id to name.
        return self.id or self.name

    def __repr__(self) -> str:
        return (
            "Node("
            f"name={self.name!r}, "
            f"id={self.id!r}, "
            f"x={self.x!r}, "
            f"y={self.y!r}, "
            f"z={self.z!r})"
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dictionary that is easy to inspect or serialize."""
        return {
            "name": self.name,
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            raise InvalidIdentifierError("Node name must be a string.")
        if not name:
            raise InvalidIdentifierError("Node name must not be empty.")
        if _ID_PATTERN.fullmatch(name) is None:
            raise InvalidIdentifierError(
                f"Node name {name!r} must start with a letter and contain only letters, digits, or underscores."
            )
        return name

    @staticmethod
    def _validate_optional_id(id: str) -> str:
        if not isinstance(id, str):
            raise InvalidIdentifierError("Node ID must be a string.")
        if id == "":
            return id
        if _ID_PATTERN.fullmatch(id) is None:
            raise InvalidIdentifierError(
                f"Node ID {id!r} must start with a letter and contain only letters, digits, or underscores."
            )
        return id

    @staticmethod
    def _validate_coordinate(name: str, value: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Node coordinate {name!r} must be numeric.")
        return float(value)
