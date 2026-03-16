# AGENTS.md

This repository contains a deliberately narrow Python package named `structural_geometry_2d`.

## Mission

Implement a small, explicit, testable package for 2D structural geometry.

## Scope constraints

Allowed in v0.1:
- nodes
- line members
- supports
- one structural container class
- validation of IDs and references
- one generator: `generate_three_hinged_frame`
- dictionary / JSON serialization for debugging

Not allowed in v0.1:
- finite element analysis
- loads
- sections or materials
- surface elements
- SAF export
- 3D abstractions
- Shapely as a core dependency
- PyNite integration
- dataclasses

## Design rules

- Use simple explicit classes.
- Do not use `@dataclass`.
- Prefer readable code over abstraction.
- Keep object relationships ID-based.
- Raise explicit custom exceptions where appropriate.
- Add tests for every public behavior.

## Validation rules

`StructuralGeometry2D.validate()` must check:
- duplicate node IDs
- duplicate member IDs
- duplicate support IDs
- missing node references in members
- missing node references in supports
- member start and end node IDs must differ

## Three-hinged frame generator rules

Use global XZ coordinates:
- x horizontal
- z vertical
- y horizontal backwards

Generate:
- N1: left base `(0.0, 0.0)`
- N2: left eaves `(0.0, eaves_height)`
- N3: ridge `(span / 2.0, ridge_height)`
- N4: right eaves `(span, eaves_height)`
- N5: right base `(span, 0.0)`

Generate line members:
- M1: N1 -> N2, type `column`
- M2: N2 -> N3, type `rafter`
- M3: N3 -> N4, type `rafter`
- M4: N4 -> N5, type `column`

Generate supports:
- S1 at N1: ux fixed, uz fixed, ry free
- S2 at N5: ux free, uz fixed, ry free

Parameter validation:
- `span > 0`
- `eaves_height > 0`
- `ridge_height > eaves_height`

## Testing rules

Write pytest tests for:
- valid object creation
- invalid IDs / references
- duplicate IDs
- generator output geometry
- generator support conditions
- `to_dict()` output shape

## Code style

- Python 3.12+
- type hints required
- small methods
- no hidden side effects
- state the filename at the top of each file (e.g. # filename.py)
- use detailed comments in the code