# structural_geometry_2d.py
"""Container model for nodes, members, and supports in v0.1."""

from __future__ import annotations

import json
import re
from typing import Any, Iterable

from structural_geometry_2d.exceptions import (
    DuplicateIdentifierError,
    InvalidGeometryError,
    InvalidIdentifierError,
    MissingReferenceError,
)
from structural_geometry_2d.model.line_member import LineMember
from structural_geometry_2d.model.node import Node
from structural_geometry_2d.model.support import Support


_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class StructuralGeometry2D:
    """Stores the explicit 2D structural geometry model."""

    def __init__(
        self,
        structure_id: str = "SG2D",
        nodes: Iterable[Node] | None = None,
        members: Iterable[LineMember] | None = None,
        supports: Iterable[Support] | None = None,
    ) -> None:
        # The container also has an ID so that a serialized model has a stable
        # top-level name without needing extra wrapper objects.
        self.id = self._validate_id(structure_id)

        # Incoming iterables are copied into plain lists to keep the container
        # predictable and free from hidden aliasing side effects.
        self.nodes = list(nodes) if nodes is not None else []
        self.members = list(members) if members is not None else []
        self.supports = list(supports) if supports is not None else []

    def __repr__(self) -> str:
        return (
            "StructuralGeometry2D("
            f"id={self.id!r}, "
            f"nodes={len(self.nodes)}, "
            f"members={len(self.members)}, "
            f"supports={len(self.supports)})"
        )

    def add_node(self, node: Node) -> None:
        """Append a node without mutating any other model state."""
        if not isinstance(node, Node):
            raise TypeError("node must be an instance of Node.")
        self.nodes.append(node)

    def add_member(self, member: LineMember) -> None:
        """Append a member without mutating any other model state."""
        if not isinstance(member, LineMember):
            raise TypeError("member must be an instance of LineMember.")
        self.members.append(member)

    def add_support(self, support: Support) -> None:
        """Append a support without mutating any other model state."""
        if not isinstance(support, Support):
            raise TypeError("support must be an instance of Support.")
        self.supports.append(support)

    def validate(self) -> None:
        """Validate container-level ID uniqueness and reference integrity."""
        self._raise_if_duplicates(self.nodes, "node")
        self._raise_if_duplicates(self.members, "member")
        self._raise_if_duplicates(self.supports, "support")

        node_ids = {node.id for node in self.nodes}

        for member in self.members:
            if member.start_node_id == member.end_node_id:
                raise InvalidGeometryError(
                    f"Member {member.id!r} must not use the same start and end node ID."
                )
            self._raise_if_missing_reference(member.id, "start_node_id", member.start_node_id, node_ids)
            self._raise_if_missing_reference(member.id, "end_node_id", member.end_node_id, node_ids)

        for support in self.supports:
            self._raise_if_missing_reference(support.id, "node_id", support.node_id, node_ids)

    def to_dict(self) -> dict[str, Any]:
        """Return a fully serializable representation of the container."""
        return {
            "id": self.id,
            "nodes": [node.to_dict() for node in self.nodes],
            "members": [member.to_dict() for member in self.members],
            "supports": [support.to_dict() for support in self.supports],
        }

    def to_json(self, *, indent: int = 2) -> str:
        """Return stable JSON primarily for debugging and snapshot-style checks."""
        return json.dumps(self.to_dict(), indent=indent)

    @property
    def line_members(self) -> list[LineMember]:
        """Provide an alias that matches the domain term used in the README and tests."""
        return self.members

    @staticmethod
    def _validate_id(structure_id: str) -> str:
        if not isinstance(structure_id, str):
            raise InvalidIdentifierError("Structure ID must be a string.")
        if not structure_id:
            raise InvalidIdentifierError("Structure ID must not be empty.")
        if _ID_PATTERN.fullmatch(structure_id) is None:
            raise InvalidIdentifierError(
                f"Structure ID {structure_id!r} must start with a letter and contain only letters, digits, or underscores."
            )
        return structure_id

    @staticmethod
    def _raise_if_duplicates(items: Iterable[Any], item_label: str) -> None:
        seen_ids: set[str] = set()
        for item in items:
            item_id = item.id
            if item_id in seen_ids:
                raise DuplicateIdentifierError(
                    f"Duplicate {item_label} ID detected: {item_id!r}."
                )
            seen_ids.add(item_id)

    @staticmethod
    def _raise_if_missing_reference(
        owner_id: str,
        field_name: str,
        referenced_id: str,
        valid_ids: set[str],
    ) -> None:
        if referenced_id not in valid_ids:
            raise MissingReferenceError(
                f"Object {owner_id!r} references missing {field_name} {referenced_id!r}."
            )
