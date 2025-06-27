import argparse
import subprocess
import sys
from pathlib import Path


def compile_ui(src: Path, dst: Path) -> bool:
    """Run `pyside6-uic` to convert *src* → *dst*.  Returns True on success."""
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Capture the generated Python and write it straight to the output file.
        with dst.open("w", encoding="utf-8") as outfile:
            subprocess.run(
                ["pyside6-uic", str(src)],
                check=True,
                stdout=outfile,
                stderr=subprocess.PIPE,
                text=True,
            )
        return True
    except subprocess.CalledProcessError as exc:
        # Forward any uic errors to stderr so the user can see them.
        sys.stderr.write(f"Failed: {src}\n{exc.stderr}\n")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recursively compile Qt Designer .ui files with pyside6-uic"
    )
    parser.add_argument(
        "--input-dir",
        default="view/ui/source/",
        help="Root directory to search",
    )
    parser.add_argument(
        "--output-dir",
        default="view/ui/compiled/",
        help="Root directory to place compiled",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    if not input_dir.exists():
        sys.exit(f"Directory not found: {input_dir}")
    if not output_dir.exists():
        sys.exit(f"Directory not found: {output_dir}")

    ui_files = list(input_dir.rglob("*.ui"))
    if not ui_files:
        print("No .ui files found. Nothing to do.")
        return

    compiled = 0
    for ui_path in ui_files:
        rel_path = ui_path.relative_to(input_dir).with_suffix(".py")
        out_path = output_dir / rel_path

        if compile_ui(ui_path, out_path):
            print(f"Compiled: {ui_path} → {out_path}")
            compiled += 1

    print(f"\nDone. {compiled} total files compiled.")


if __name__ == "__main__":
    main()
