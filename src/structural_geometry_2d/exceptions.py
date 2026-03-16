# exceptions.py
"""Custom exceptions for the structural_geometry_2d package."""

from __future__ import annotations


class StructuralGeometryError(Exception):
    """Base class for all package-specific errors."""


class ValidationError(StructuralGeometryError):
    """Raised when an object or a model violates validation rules."""


class InvalidIdentifierError(ValidationError):
    """Raised when an identifier is missing or uses an unsupported format."""


class DuplicateIdentifierError(ValidationError):
    """Raised when a container contains the same identifier more than once."""


class MissingReferenceError(ValidationError):
    """Raised when an ID-based relationship points to a missing object."""


class InvalidGeometryError(ValidationError):
    """Raised when a geometric definition is internally inconsistent."""


class InvalidRestraintError(ValidationError):
    """Raised when a support restraint uses a value outside the allowed set."""


# Keep a second base-name alias so calling code can use either package-style name.
StructuralGeometry2DError = StructuralGeometryError


__all__ = [
    "StructuralGeometryError",
    "StructuralGeometry2DError",
    "ValidationError",
    "InvalidIdentifierError",
    "DuplicateIdentifierError",
    "MissingReferenceError",
    "InvalidGeometryError",
    "InvalidRestraintError",
]
