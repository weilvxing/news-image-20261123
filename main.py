"""news-image-20261123 -- make.fun entry.

Builds the entry image: copies the newspaper front page (entry.png,
1024x1024, summing up 23 November 2026's world news) into the output
directory and verifies the copy with SHA-256.

Usage:
    python3 main.py [--output PATH]

The default output is /output/entry.png. The run is deterministic:
no timestamps, no randomness, no network access. Running it twice
produces a byte-identical file.
"""

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

ENTRY_NAME = "entry.png"
DEFAULT_OUTPUT = Path("/output") / ENTRY_NAME


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Where to write the entry image (default: /output/entry.png)",
    )
    args = parser.parse_args(argv)

    source = Path(__file__).resolve().parent / ENTRY_NAME
    if not source.is_file():
        print(f"error: {ENTRY_NAME} not found next to main.py", file=sys.stderr)
        return 1

    destination = args.output
    if destination.resolve() == source.resolve():
        print(f"error: output path is the same file as {ENTRY_NAME}",
              file=sys.stderr)
        return 1
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)

    source_hash = sha256_of(source)
    dest_hash = sha256_of(destination)
    print(f"source:      {source} ({source_hash})")
    print(f"destination: {destination} ({dest_hash}, "
          f"{destination.stat().st_size} bytes)")
    if source_hash != dest_hash:
        print("error: SHA-256 mismatch after copy", file=sys.stderr)
        return 1
    print("OK: entry image copied and verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
