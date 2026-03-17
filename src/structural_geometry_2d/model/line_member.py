# line_member.py
"""Explicit line member model used by the v0.1 structural geometry package."""

from __future__ import annotations

import re
from typing import Any

from structural_geometry_2d.exceptions import InvalidGeometryError, InvalidIdentifierError


_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class LineMember:
    """Represents a straight member defined by name and node names."""

    def __init__(
        self,
        name: str,
        start_node: str,
        end_node: str,
        member_type: str,
    ) -> None:
        # Members now follow the same public naming pattern as nodes. The name
        # is still validated like an identifier because it is also the stable
        # token used by validation, plotting labels, and serialization.
        self.name = self._validate_name(name)
        self.start_node = self._validate_id("Start node name", start_node)
        self.end_node = self._validate_id("End node name", end_node)
        self.member_type = self._validate_member_type(member_type)

        if self.start_node == self.end_node:
            raise InvalidGeometryError("Member start and end node names must differ.")

    def __repr__(self) -> str:
        return (
            "LineMember("
            f"name={self.name!r}, "
            f"start_node={self.start_node!r}, "
            f"end_node={self.end_node!r}, "
            f"member_type={self.member_type!r})"
        )

    @property
    def id(self) -> str:
        """Provide a backward-compatible alias while the API moves to name."""
        return self.name

    @property
    def type(self) -> str:
        """Expose the public member category using the short field name from the scope."""
        return self.member_type

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dictionary for debugging and JSON serialization."""
        return {
            "name": self.name,
            "start_node": self.start_node,
            "end_node": self.end_node,
            "type": self.member_type,
        }

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            raise InvalidIdentifierError("Member name must be a string.")
        if not name:
            raise InvalidIdentifierError("Member name must not be empty.")
        if _NAME_PATTERN.fullmatch(name) is None:
            raise InvalidIdentifierError(
                f"Member name {name!r} must start with a letter and contain only letters, digits, or underscores."
            )
        return name

    @staticmethod
    def _validate_id(label: str, value: str) -> str:
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
    def _validate_member_type(member_type: str) -> str:
        if not isinstance(member_type, str):
            raise TypeError("Member type must be a string.")
        cleaned_value = member_type.strip()
        if not cleaned_value:
            raise ValueError("Member type must not be empty.")
        return cleaned_value
