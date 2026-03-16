# node.py
"""Explicit node model used by the v0.1 structural geometry package."""

from __future__ import annotations

import re
from typing import Any

from structural_geometry_2d.exceptions import InvalidIdentifierError


_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class Node:
    """Represents a 2D node in global XZ coordinates."""

    def __init__(self, node_id: str, x: float, z: float) -> None:
        # The package uses IDs to wire objects together, so the ID format is
        # validated at construction time and not deferred to container logic.
        self.id = self._validate_id(node_id)

        # Coordinates are stored as floats to keep serialization predictable
        # and to avoid int/float branching in downstream code and tests.
        self.x = self._validate_coordinate("x", x)
        self.z = self._validate_coordinate("z", z)

    def __repr__(self) -> str:
        return f"Node(id={self.id!r}, x={self.x!r}, z={self.z!r})"

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dictionary that is easy to inspect or serialize."""
        return {
            "id": self.id,
            "x": self.x,
            "z": self.z,
        }

    @staticmethod
    def _validate_id(node_id: str) -> str:
        if not isinstance(node_id, str):
            raise InvalidIdentifierError("Node ID must be a string.")
        if not node_id:
            raise InvalidIdentifierError("Node ID must not be empty.")
        if _ID_PATTERN.fullmatch(node_id) is None:
            raise InvalidIdentifierError(
                f"Node ID {node_id!r} must start with a letter and contain only letters, digits, or underscores."
            )
        return node_id

    @staticmethod
    def _validate_coordinate(name: str, value: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Node coordinate {name!r} must be numeric.")
        return float(value)
