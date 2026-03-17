# plot_three_hinged_frame.py
"""Small example script for plotting a three-hinged frame with matplotlib."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt


# Allow running this example directly from the repository root without
# requiring an editable installation of the package first.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from structural_geometry_2d.generators import generate_three_hinged_frame  # noqa: E402
from structural_geometry_2d.visualization import plot_geometry_2d  # noqa: E402


def main() -> None:
    """Generate, validate, plot, and display a three-hinged frame."""
    # The example uses explicit dimensions so the plotted geometry stays
    # deterministic and easy to compare while learning the API.
    frame = generate_three_hinged_frame(
        span=20.0,
        eaves_height=5.0,
        ridge_height=8.0,
        structure_id="ExampleFrame",
    )

    # Explicit validation keeps the example aligned with normal package usage.
    frame.validate()

    # The plotting helper already enforces equal x-z scaling. The title and
    # member labels make the resulting figure easier to read when opened.
    figure, axes = plot_geometry_2d(frame, show_member_names=True)
    axes.set_title("Three-Hinged Frame")
    figure.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
