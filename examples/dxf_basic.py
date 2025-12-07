"""Create a sample DXF drawing and export a PNG preview."""

from __future__ import annotations

from pathlib import Path

from vector2png import DXFOptions, dxf_to_png


def main() -> None:
    # Use script directory for consistent path handling
    script_dir = Path(__file__).parent
    input_file = script_dir / "files" / "example.dxf"
    output_file = script_dir / "generated" / "example_dxf.png"

    # Ensure output directory exists
    output_file.parent.mkdir(exist_ok=True)

    if not input_file.exists():
        print(f"Please place your DXF file at {input_file.resolve()}")
        return

    options = DXFOptions(background="white", color_policy="color", dpi=200)
    dxf_to_png(input_file, output_file, options)
    print(f"DXF preview exported to {output_file.resolve()}")


if __name__ == "__main__":
    main()