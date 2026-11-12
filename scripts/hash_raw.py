"""Print the sha256 and size of every file in raw/.

Usage:
    python scripts/hash_raw.py            # hashes <repo>/raw
    python scripts/hash_raw.py PATH       # hashes another directory

Read-only: files are opened in binary read mode and never modified.
.gitkeep files are skipped. Paths are printed relative to the scanned
directory, with forward slashes, sorted alphabetically.
"""

import hashlib
import os
import sys

CHUNK_SIZE = 1024 * 1024  # read 1 MiB at a time so large files are fine


def sha256_of(path):
    """Return the hex sha256 digest of a file, read in binary chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def collect_files(root):
    """Return sorted relative paths (forward slashes) of all files under root."""
    found = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name == ".gitkeep":
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            found.append(rel)
    return sorted(found)


def main():
    # Print UTF-8 so Chinese file names survive pipes and redirects.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) > 2:
        print("Usage: python scripts/hash_raw.py [DIRECTORY]", file=sys.stderr)
        return 2

    if len(sys.argv) == 2:
        root = sys.argv[1]
    else:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        root = os.path.join(repo_root, "raw")

    if not os.path.isdir(root):
        print(f"ERROR: directory not found: {root}", file=sys.stderr)
        return 2

    files = collect_files(root)
    if not files:
        print(f"No files found in {root} (.gitkeep is skipped).")
        return 0

    rows = []
    for rel in files:
        full = os.path.join(root, *rel.split("/"))
        rows.append((rel, sha256_of(full), os.path.getsize(full)))

    path_width = max(len("path"), max(len(r[0]) for r in rows))
    header = f"{'path':<{path_width}}  {'sha256':<64}  {'size_bytes':>10}"
    print(header)
    print("-" * len(header))
    for rel, digest, size in rows:
        print(f"{rel:<{path_width}}  {digest}  {size:>10}")
    print(f"\n{len(rows)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
