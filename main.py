#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261123.

Copies the bundled newspaper front-page image (entry.png, summarising
23 November 2026 world news) to the output location the competition
expects, verifying its SHA-256 digest first so a damaged or swapped
image can never be submitted by accident.

Output location, in order of priority:
  1. --output <path> on the command line
  2. $MAKEFUN_OUTPUT_DIR/entry.png when that variable is set
  3. /output/entry.png (the grader's default)

Pass --verify-only to check the image's digest without writing
anything: useful as a quick sanity check before submitting.

Standard library only. The copy is a plain byte copy, so the output
is byte-identical on every run.
"""

import argparse
import hashlib
import os
import shutil
import sys
from pathlib import Path

# SHA-256 of the entry.png shipped in this repository.
EXPECTED_SHA256 = "966ef30203a96555a838fbdb2b4b043e7b4065f3f4296a14ed515b9fc4f76ce6"

SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT = Path("/output/entry.png")


def sha256_of(path):
    """Return the hex SHA-256 digest of the file at *path*."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_path():
    """Locate entry.png next to this script."""
    here = Path(__file__).resolve().parent
    return here / SOURCE_NAME


def default_output_path():
    """Work out the default output path from the environment."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return Path(out_dir) / "entry.png"
    return DEFAULT_OUTPUT


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Copy entry.png to the competition output location."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="destination path for the image (default: "
        "$MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png)",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="source image to copy (default: entry.png next to main.py)",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="only verify entry.png against its expected SHA-256 digest "
        "and exit, without writing any output file",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    source = args.source if args.source is not None else source_path()
    destination = args.output if args.output is not None else default_output_path()

    if not source.is_file():
        print(f"error: source image not found: {source}", file=sys.stderr)
        print("expected entry.png next to main.py, or pass --source", file=sys.stderr)
        return 1

    actual = sha256_of(source)
    if actual != EXPECTED_SHA256:
        size = source.stat().st_size if source.exists() else None
        print("error: source image failed SHA-256 verification", file=sys.stderr)
        print(f"  file:     {source}", file=sys.stderr)
        if size is not None:
            print(f"  size:     {size} bytes", file=sys.stderr)
        print(f"  expected: {EXPECTED_SHA256}", file=sys.stderr)
        print(f"  actual:   {actual}", file=sys.stderr)
        print(
            "the bundled entry.png does not match the digest this program "
            "was written for: it may be damaged, truncated, or a different "
            "image. Restore the original entry.png and try again; "
            "nothing was copied.",
            file=sys.stderr,
        )
        return 1

    if args.verify_only:
        size = source.stat().st_size
        print(f"verified {source} ({size} bytes, sha256 {actual})")
        return 0

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    except OSError as exc:
        print(f"error: could not write output file {destination}: {exc}", file=sys.stderr)
        return 1

    written = sha256_of(destination)
    if written != EXPECTED_SHA256:
        print("error: output file failed SHA-256 verification after copy", file=sys.stderr)
        print(f"  file:     {destination}", file=sys.stderr)
        print(f"  expected: {EXPECTED_SHA256}", file=sys.stderr)
        print(f"  actual:   {written}", file=sys.stderr)
        return 1

    size = destination.stat().st_size
    print(f"wrote {destination} ({size} bytes, sha256 {written})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
