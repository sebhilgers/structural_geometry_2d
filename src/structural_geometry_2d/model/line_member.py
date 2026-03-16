# line_member.py
"""Explicit line member model used by the v0.1 structural geometry package."""

from __future__ import annotations

import re
from typing import Any

from structural_geometry_2d.exceptions import InvalidGeometryError, InvalidIdentifierError


_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class LineMember:
    """Represents a straight member defined by start and end node IDs."""

    def __init__(
        self,
        member_id: str,
        start_node_id: str,
        end_node_id: str,
        member_type: str,
    ) -> None:
        # Member IDs and node references are all explicit strings because the
        # package keeps relationships ID-based instead of object-linked.
        self.id = self._validate_id("Member ID", member_id)
        self.start_node_id = self._validate_id("Start node ID", start_node_id)
        self.end_node_id = self._validate_id("End node ID", end_node_id)
        self.member_type = self._validate_member_type(member_type)

        if self.start_node_id == self.end_node_id:
            raise InvalidGeometryError("Member start and end node IDs must differ.")

    def __repr__(self) -> str:
        return (
            "LineMember("
            f"id={self.id!r}, "
            f"start_node_id={self.start_node_id!r}, "
            f"end_node_id={self.end_node_id!r}, "
            f"member_type={self.member_type!r})"
        )

    @property
    def type(self) -> str:
        """Expose the public member category using the short field name from the scope."""
        return self.member_type

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dictionary for debugging and JSON serialization."""
        return {
            "id": self.id,
            "start_node_id": self.start_node_id,
            "end_node_id": self.end_node_id,
            "type": self.member_type,
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
    def _validate_member_type(member_type: str) -> str:
        if not isinstance(member_type, str):
            raise TypeError("Member type must be a string.")
        cleaned_value = member_type.strip()
        if not cleaned_value:
            raise ValueError("Member type must not be empty.")
        return cleaned_value
