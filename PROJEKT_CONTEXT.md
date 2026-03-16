# Project Context

This repository contains the Python package `structural_geometry_2d`.

The goal of the project is to create a minimal structural geometry model for
2D structural systems used in structural engineering.

The package is intentionally narrow and focuses on geometry only.

---

# Coordinate System

Global coordinate system:

x : horizontal to the right  
z : vertical upwards  
y : horizontal to the back

All 2D structural models currently lie in the **x-z plane**.

---

# Scope of Version 0.1

The package supports:

- nodes
- line members
- supports
- structural geometry container
- model validation
- generator for a three hinged frame

The package does NOT support:

- loads
- materials
- cross sections
- surface elements
- finite element analysis
- 3D modelling
- SAF export

---

# Core Classes

Main classes:

Node  
LineMember  
Support  
StructuralGeometry2D

All references between objects are **ID based**, not object references.

---

# Geometry Conventions

Nodes use:

x coordinate  
z coordinate

Members connect nodes via node IDs.

Supports constrain DOF:

ux  
uz  
ry

---

# Development Philosophy

The code should remain:

- simple
- explicit
- testable
- small

Avoid:

- frameworks
- heavy abstractions
- dataclasses
- hidden side effects