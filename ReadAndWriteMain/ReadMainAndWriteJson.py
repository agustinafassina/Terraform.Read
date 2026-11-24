"""Read a Terraform .tf file and write its content as JSON."""

import argparse
import json
import sys
from pathlib import Path

import hcl2

SERIALIZATION_OPTIONS = hcl2.SerializationOptions(
    with_comments=False,
    explicit_blocks=False,
    strip_string_quotes=True,
)


def load_tf_file(filename):
    """Parse a .tf file and return its content as a dictionary."""
    with open(filename, "r", encoding="utf-8") as f:
        return hcl2.load(f, serialization_options=SERIALIZATION_OPTIONS)


def save_to_json(data, output_file):
    """Save a dictionary to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Convert a Terraform .tf file to JSON.")
    parser.add_argument("input", nargs="?", default="main.tf", help="Path to the .tf file (default: main.tf)")
    parser.add_argument("-o", "--output", help="Path to the output JSON file (default: input name with .json)")
    args = parser.parse_args(argv)

    output = args.output or str(Path(args.input).with_suffix(".json"))

    try:
        data = load_tf_file(args.input)
    except FileNotFoundError:
        print(f"File '{args.input}' not found.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error reading file '{args.input}': {e}", file=sys.stderr)
        return 1

    try:
        save_to_json(data, output)
    except OSError as e:
        print(f"Error writing JSON file '{output}': {e}", file=sys.stderr)
        return 1

    print(f"File JSON saved in '{output}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
