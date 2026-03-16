# create_three_hinged_frame.py
"""Small example script for generating and inspecting a three-hinged frame."""

from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint


# Allow running this example directly from the repository root without
# requiring an editable installation of the package first.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from structural_geometry_2d.generators import generate_three_hinged_frame


def main() -> None:
    """Generate, validate, and print a small three-hinged frame model."""
    # The example uses explicit dimensions so the output stays deterministic and
    # easy to compare while learning the package structure.
    frame = generate_three_hinged_frame(
        span=20.0,
        eaves_height=5.0,
        ridge_height=8.0,
        structure_id="ExampleFrame",
    )

    # Explicit validation keeps the example aligned with normal package usage.
    frame.validate()

    print("Three-hinged frame as dict:")
    pprint(frame.to_dict(), sort_dicts=False)


if __name__ == "__main__":
    main()
