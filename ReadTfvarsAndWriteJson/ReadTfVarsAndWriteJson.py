"""Read a Terraform .tfvars file and write its variables as JSON."""

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


def load_tfvars_file(filename):
    """Parse a .tfvars file and return its variables as a dictionary.

    Keeps value types: lists, maps, numbers and booleans are preserved.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return hcl2.load(f, serialization_options=SERIALIZATION_OPTIONS)


def save_to_json(data, output_file):
    """Save a dictionary to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Convert a Terraform .tfvars file to JSON.")
    parser.add_argument("input", nargs="?", default="dev.tfvars", help="Path to the .tfvars file (default: dev.tfvars)")
    parser.add_argument("-o", "--output", help="Path to the output JSON file (default: input name with .json)")
    args = parser.parse_args(argv)

    output = args.output or str(Path(args.input).with_suffix(".json"))

    try:
        data = load_tfvars_file(args.input)
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

    print(f"File .tfvars converted to '{output}' successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
