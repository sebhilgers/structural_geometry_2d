# structural_geometry_2d

`structural_geometry_2d` is a Python package for creating, validating, and serializing simple 2D structural geometry models.

## Scope of v0.1

This package is intentionally narrow.

It supports:
- 2D nodes
- 2D line members
- 2D supports
- a structural geometry container
- validation of IDs and references
- generation of a simple three-hinged frame
- debug serialization to Python dictionaries / JSON

It does not support:
- finite element analysis
- loads
- materials or sections
- surface elements
- SAF export
- 3D geometry
- Shapely or PyNite integration

## Coordinate system

The package uses a global 2D XZ coordinate system:
- x = horizontal
- z = vertical

## Design principles

- explicit, small classes
- no dataclasses
- object references by ID, not by embedded objects
- validation is explicit
- simple and testable API

## Public API

Main public classes:
- `Node`
- `LineMember`
- `Support`
- `StructuralGeometry2D`

Main public generator:
- `generate_three_hinged_frame(...)`

## Development

Run tests with:

```bash
pytest