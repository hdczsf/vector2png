"""Basic AI to PNG usage example."""

from __future__ import annotations

from pathlib import Path

from vector2png import AIOptions, ai_to_png


def main() -> None:
    """Example: convert an AI file into a PNG preview."""
    # Use script directory for consistent path handling
    script_dir = Path(__file__).parent
    input_file = script_dir / "files" / "example.ai"
    output_file = script_dir / "generated" / "example_ai.png"

    # Ensure output directory exists
    output_file.parent.mkdir(exist_ok=True)

    if not input_file.exists():
        print(f"Please place your AI file at {input_file.resolve()}")
        return

    options = AIOptions(dpi=200, transparent=False)
    ai_to_png(input_file, output_file, options)
    print(f"Saved PNG to {output_file.resolve()}")


if __name__ == "__main__":
    main()