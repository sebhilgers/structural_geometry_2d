# node.py
"""Explicit node model used by the v0.1 structural geometry package."""

from __future__ import annotations

import re
from typing import Any

from structural_geometry_2d.exceptions import InvalidIdentifierError


_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class Node:
    """Represents a 2D node referenced only by its explicit name."""

    def __init__(
        self,
        name: str,
        x: float,
        z: float,
        y: float = 0.0,
    ) -> None:
        # Node names are the only public reference token in v0.1, so the name
        # uses the same explicit identifier validation as the other models.
        self.name = self._validate_name(name)

        # Coordinates are stored as floats to keep serialization predictable
        # and to avoid int/float branching in downstream code and tests.
        self.x = self._validate_coordinate("x", x)
        self.y = self._validate_coordinate("y", y)
        self.z = self._validate_coordinate("z", z)

    def __repr__(self) -> str:
        return (
            "Node("
            f"name={self.name!r}, "
            f"x={self.x!r}, "
            f"y={self.y!r}, "
            f"z={self.z!r})"
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dictionary that is easy to inspect or serialize."""
        return {
            "name": self.name,
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
        if _NAME_PATTERN.fullmatch(name) is None:
            raise InvalidIdentifierError(
                f"Node name {name!r} must start with a letter and contain only letters, digits, or underscores."
            )
        return name

    @staticmethod
    def _validate_coordinate(name: str, value: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Node coordinate {name!r} must be numeric.")
        return float(value)
