# support.py
"""Explicit support model used by the v0.1 structural geometry package."""

from __future__ import annotations

import re
from typing import Any

from structural_geometry_2d.exceptions import InvalidIdentifierError, InvalidRestraintError


_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_ALLOWED_RESTRAINTS = {"fixed", "free"}


class Support:
    """Represents support restraints attached to a node by name."""

    def __init__(
        self,
        name: str,
        node_name: str,
        ux: str,
        uy: str,
        uz: str,
        rx: str,
        ry: str,
        rz: str,
    ) -> None:
        # Support objects are intentionally simple: one support identifier, one
        # node-name reference, and explicit restraint states for all six global
        # translational and rotational degrees of freedom.
        self.name = self._validate_name("Support name", name)
        self.node_name = self._validate_name("Node name", node_name)
        self.ux = self._validate_restraint("ux", ux)
        self.uy = self._validate_restraint("uy", uy)
        self.uz = self._validate_restraint("uz", uz)
        self.rx = self._validate_restraint("rx", rx)
        self.ry = self._validate_restraint("ry", ry)
        self.rz = self._validate_restraint("rz", rz)

    def __repr__(self) -> str:
        return (
            "Support("
            f"support_name={self.name!r}, "
            f"node_name={self.node_name!r}, "
            f"ux={self.ux!r}, "
            f"uy={self.uy!r}, "
            f"uz={self.uz!r}, "
            f"rx={self.rx!r}, "
            f"ry={self.ry!r}, "
            f"rz={self.rz!r})"
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dictionary for debugging and JSON serialization."""
        return {
            "name": self.name,
            "node_name": self.node_name,
            "ux": self.ux,
            "uy": self.uy,
            "uz": self.uz,
            "rx": self.rx,
            "ry": self.ry,
            "rz": self.rz,
        }

    @staticmethod
    def _validate_name(label: str, value: str) -> str:
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
