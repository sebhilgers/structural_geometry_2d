# structural_geometry_2d.py
"""Container model for nodes, members, supports, and connections in v0.1."""

from __future__ import annotations

import json
import re
from typing import Any, Callable, Iterable

from structural_geometry_2d.exceptions import (
    DuplicateIdentifierError,
    InvalidGeometryError,
    InvalidIdentifierError,
    MissingReferenceError,
)
from structural_geometry_2d.model.connections import Member_connection
from structural_geometry_2d.model.line_member import LineMember
from structural_geometry_2d.model.node import Node
from structural_geometry_2d.model.support import Support


_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class StructuralGeometry2D:
    """Stores the explicit 2D structural geometry model."""

    def __init__(
        self,
        structure_name: str = "SG2D",
        nodes: Iterable[Node] | None = None,
        members: Iterable[LineMember] | None = None,
        supports: Iterable[Support] | None = None,
        connections: Iterable[Member_connection] | None = None,
    ) -> None:
        # The container also has an ID so that a serialized model has a stable
        # top-level name without needing extra wrapper objects.
        self.name = self._validate_name(structure_name)

        # Incoming iterables are copied into plain lists to keep the container
        # predictable and free from hidden aliasing side effects.
        self.nodes = list(nodes) if nodes is not None else []
        self.members = list(members) if members is not None else []
        self.supports = list(supports) if supports is not None else []
        self.connections = list(connections) if connections is not None else []

    def __repr__(self) -> str:
        return (
            "StructuralGeometry2D("
            f"id={self.name!r}, "
            f"nodes={len(self.nodes)}, "
            f"members={len(self.members)}, "
            f"supports={len(self.supports)}, "
            f"connections={len(self.connections)})"
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

    def add_connection(self, connection: Member_connection) -> None:
        """Append a member connection without mutating any other model state."""
        if not isinstance(connection, Member_connection):
            raise TypeError("connection must be an instance of Member_connection.")
        self.connections.append(connection)

    def validate(self) -> None:
        """Validate container-level uniqueness and name-based reference integrity."""
        self._raise_if_duplicates(
            self.nodes,
            "node",
            identifier_getter=lambda node: node.name,
        )
        self._raise_if_duplicates(
            self.members,
            "member",
            identifier_getter=lambda member: member.name,
        )
        self._raise_if_duplicates(self.supports, "support")
        self._raise_if_duplicates(self.connections, "connection")

        # Members and supports reference nodes only by node name in v0.1.
        node_names = {node.name for node in self.nodes}
        member_names = {member.name for member in self.members}

        for member in self.members:
            if member.start_node == member.end_node:
                raise InvalidGeometryError(
                    f"Member {member.name!r} must not use the same start and end node name."
                )
            self._raise_if_missing_reference(
                member.name,
                "start_node",
                member.start_node,
                node_names,
            )
            self._raise_if_missing_reference(
                member.name,
                "end_node",
                member.end_node,
                node_names,
            )

        for support in self.supports:
            self._raise_if_missing_reference(
                support.name,
                "node_name",
                support.node_name,
                node_names,
            )

        for connection in self.connections:
            self._raise_if_missing_reference(
                connection.name,
                "member",
                connection.member,
                member_names,
            )

    def to_dict(self) -> dict[str, Any]:
        """Return a fully serializable representation of the container."""
        return {
            "id": self.name,
            "nodes": [node.to_dict() for node in self.nodes],
            "members": [member.to_dict() for member in self.members],
            "supports": [support.to_dict() for support in self.supports],
            "connections": [connection.to_dict() for connection in self.connections],
        }

    def to_json(self, *, indent: int = 2) -> str:
        """Return stable JSON primarily for debugging and snapshot-style checks."""
        return json.dumps(self.to_dict(), indent=indent)

    @property
    def line_members(self) -> list[LineMember]:
        """Provide an alias that matches the domain term used in the README and tests."""
        return self.members

    @staticmethod
    def _validate_name(structure_name: str) -> str:
        if not isinstance(structure_name, str):
            raise InvalidIdentifierError("Structure name must be a string.")
        if not structure_name:
            raise InvalidIdentifierError("Structure name must not be empty.")
        if _NAME_PATTERN.fullmatch(structure_name) is None:
            raise InvalidIdentifierError(
                f"Structure name {structure_name!r} must start with a letter and contain only letters, digits, or underscores."
            )
        return structure_name

    @staticmethod
    def _raise_if_duplicates(
        items: Iterable[Any],
        item_label: str,
        identifier_getter: Callable[[Any], str] | None = None,
    ) -> None:
        seen_names: set[str] = set()
        get_identifier = identifier_getter or (lambda item: item.name)
        for item in items:
            item_name = get_identifier(item)
            if item_name in seen_names:
                duplicate_field = "name" if item_label in {"node", "member", "connection"} else "ID"
                raise DuplicateIdentifierError(
                    f"Duplicate {item_label} {duplicate_field} detected: {item_name!r}."
                )
            seen_names.add(item_name)

    @staticmethod
    def _raise_if_missing_reference(
        owner_name: str,
        field_name: str,
        referenced_name: str,
        valid_names: set[str],
    ) -> None:
        if referenced_name not in valid_names:
            raise MissingReferenceError(
                f"Object {owner_name!r} references missing {field_name} {referenced_name!r}."
            )
