# support.py
"""Explicit support model used by the v0.1 structural geometry package."""

from __future__ import annotations

import re
from typing import Any

from structural_geometry_2d.exceptions import InvalidIdentifierError, InvalidRestraintError


_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_ALLOWED_RESTRAINTS = {"fixed", "free"}


class Support:
    """Represents support restraints attached to a node by ID."""

    def __init__(self, support_id: str, node_id: str, ux: str, uz: str, ry: str) -> None:
        # Support objects are intentionally simple: one ID, one node reference,
        # and explicit restraint states for the x translation, z translation,
        # and y rotation degrees of freedom used by the x-z plane convention.
        self.id = self._validate_id("Support ID", support_id)
        self.node_id = self._validate_id("Node ID", node_id)
        self.ux = self._validate_restraint("ux", ux)
        self.uz = self._validate_restraint("uz", uz)
        self.ry = self._validate_restraint("ry", ry)

    def __repr__(self) -> str:
        return (
            "Support("
            f"id={self.id!r}, "
            f"node_id={self.node_id!r}, "
            f"ux={self.ux!r}, "
            f"uz={self.uz!r}, "
            f"ry={self.ry!r})"
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dictionary for debugging and JSON serialization."""
        return {
            "id": self.id,
            "node_id": self.node_id,
            "ux": self.ux,
            "uz": self.uz,
            "ry": self.ry,
        }

    @staticmethod
    def _validate_id(label: str, value: str) -> str:
        if not isinstance(value, str):
            raise InvalidIdentifierError(f"{label} must be a string.")
        if not value:
            raise InvalidIdentifierError(f"{label} must not be empty.")
        if _ID_PATTERN.fullmatch(value) is None:
            raise InvalidIdentifierError(
                f"{label} {value!r} must start with a letter and contain only letters, digits, or underscores."
            )
        return value

    @staticmethod
    def _validate_restraint(label: str, value: str) -> str:
        if not isinstance(value, str):
            raise InvalidRestraintError(f"Support restraint {label!r} must be a string.")
        cleaned_value = value.strip().lower()
        if cleaned_value not in _ALLOWED_RESTRAINTS:
            raise InvalidRestraintError(
                f"Support restraint {label!r} must be one of {sorted(_ALLOWED_RESTRAINTS)}."
            )
        return cleaned_value
