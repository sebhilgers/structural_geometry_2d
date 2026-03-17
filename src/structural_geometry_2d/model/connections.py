# connections.py
"""Explicit member-connection model for local member release conditions."""

from __future__ import annotations

import re
from typing import Any

from structural_geometry_2d.exceptions import InvalidIdentifierError, InvalidRestraintError


_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_ALLOWED_POSITIONS = {"start", "end", "both"}
_ALLOWED_CONNECTION_STATES = {"free", "rigid", "flexible"}


class Member_connection:
    """Represents local release conditions between a member and a connection object."""

    def __init__(
        self,
        name: str,
        member: str,
        position: str,
        ux: str,
        uy: str,
        uz: str,
        rx: str,
        ry: str,
        rz: str,
    ) -> None:
        # Connection objects stay ID-based like the rest of the package. The
        # referenced member is stored only by its public identifier.
        self.name = self._validate_name("Connection name", name)
        self.member = self._validate_name("Member name", member)

        # Release states are defined in the member's local 1D coordinate system,
        # so the stored position token identifies which member end they apply to.
        self.position = self._validate_position(position)
        self.ux = self._validate_condition("ux", ux)
        self.uy = self._validate_condition("uy", uy)
        self.uz = self._validate_condition("uz", uz)
        self.rx = self._validate_condition("rx", rx)
        self.ry = self._validate_condition("ry", ry)
        self.rz = self._validate_condition("rz", rz)

    def __repr__(self) -> str:
        return (
            "Member_connection("
            f"name={self.name!r}, "
            f"member={self.member!r}, "
            f"position={self.position!r}, "
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
            "member": self.member,
            "position": self.position,
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
        if _NAME_PATTERN.fullmatch(value) is None:
            raise InvalidIdentifierError(
                f"{label} {value!r} must start with a letter and contain only letters, digits, or underscores."
            )
        return value

    @staticmethod
    def _validate_position(value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Connection position must be a string.")
        cleaned_value = value.strip().lower()
        if cleaned_value not in _ALLOWED_POSITIONS:
            raise ValueError(
                f"Connection position must be one of {sorted(_ALLOWED_POSITIONS)}."
            )
        return cleaned_value

    @staticmethod
    def _validate_condition(label: str, value: str) -> str:
        if not isinstance(value, str):
            raise InvalidRestraintError(f"Connection condition {label!r} must be a string.")
        cleaned_value = value.strip().lower()
        if cleaned_value not in _ALLOWED_CONNECTION_STATES:
            raise InvalidRestraintError(
                f"Connection condition {label!r} must be one of {sorted(_ALLOWED_CONNECTION_STATES)}."
            )
        return cleaned_value
