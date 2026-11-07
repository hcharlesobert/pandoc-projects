#!/usr/bin/env python3
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

source = Path.home() / "OneDrive/Documents/HelenZilwicki"
repo = Path.cwd()

# Find ISO dates anywhere in a filename, such as draft-2023-12-06-final.docx.
date_pattern = re.compile(r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)")
extensions = {".docx", ".odt"}

files = sorted(
    (p for p in source.rglob("*") if p.is_file() and p.suffix.lower() in extensions),
    key=lambda p: (
        date_pattern.search(p.name).group(1)
        if date_pattern.search(p.name)
        else "9999-99-99",
        p.stat().st_mtime,
        str(p).casefold(),
    ),
)

if not files:
    sys.exit(f"No DOCX or ODT files found under {source}")

print("Order: filename date, then modification time; files without a date come last.")
for p in files:
    match = date_pattern.search(p.name)
    # Validate dates rather than accepting malformed date-like strings.
    try:
        label = date.fromisoformat(match.group(1)).isoformat() if match else "NO-DATE"
    except ValueError:
        label = "INVALID-DATE"
    print(f"{label:12} {p.stat().st_mtime_ns}  {p.relative_to(source)}")

if "--convert" not in sys.argv:
    print("\nPreview only. Run again with --convert to convert these files.")
    sys.exit(0)

for p in files:
    # Mirror the source folder structure and keep the original extension in
    # the output name, so same-named DOCX and ODT files don't collide.
    relative = p.relative_to(source)
    output = repo / "imported" / relative.parent / f"{p.name}.md"
    output.parent.mkdir(parents=True, exist_ok=True)

    if output.exists():
        print(f"SKIP (already exists): {output.relative_to(repo)}", file=sys.stderr)
        continue

    subprocess.run(["pandoc", str(p), "-o", str(output)], check=True)
    print(f"Created {output.relative_to(repo)}")
