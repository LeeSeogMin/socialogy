#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

import nbformat


_RE_LIST = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+)")
_RE_HEADING = re.compile(r"^\s*#{1,6}\s+")
_RE_HR = re.compile(r"^\s*(?:---|___|\*\*\*)\s*$")
_RE_FENCE = re.compile(r"^\s*```")
_RE_BLOCKQUOTE = re.compile(r"^\s*>")
_RE_TABLE = re.compile(r"^\s*\|")
_RE_IMAGE = re.compile(r"^\s*!\[")
_RE_BOLD_LABEL = re.compile(r"^\s*\*\*[^*]+\*\*\s*:?\s*$")
_RE_CHECKBOX = re.compile(r"^\s*-\s+\[[ xX]\]\s+")


def _is_structural_line(line: str) -> bool:
    stripped = line.rstrip("\n")
    return bool(
        _RE_HEADING.match(stripped)
        or _RE_LIST.match(stripped)
        or _RE_HR.match(stripped)
        or _RE_FENCE.match(stripped)
        or _RE_BLOCKQUOTE.match(stripped)
        or _RE_TABLE.match(stripped)
        or _RE_IMAGE.match(stripped)
        or stripped.lstrip().startswith("<")
    )


def _looks_like_table_block(lines: list[str]) -> bool:
    # Conservative: if a block starts with "|" or contains the typical separator row, treat as a table.
    if any(_RE_TABLE.match(ln) for ln in lines):
        return True
    if any(re.match(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$", ln) for ln in lines):
        return True
    return False


def _keep_bold_label_block(lines: list[str]) -> bool:
    if not lines:
        return False
    first = next((ln for ln in lines if ln.strip()), "")
    if not first:
        return True
    if not _RE_BOLD_LABEL.match(first):
        return False
    # If the label is followed by a list/checklist, keep as-is (common in notebooks).
    tail = [ln for ln in lines[1:] if ln.strip()]
    if not tail:
        return True
    if any(_RE_LIST.match(ln) or _RE_CHECKBOX.match(ln) for ln in tail):
        return True
    return False


def outline_paragraph_blocks(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    buf: list[str] = []
    in_fence = False

    def flush_buf() -> None:
        nonlocal buf
        if not buf:
            return

        # If the block is empty/whitespace, emit as-is.
        if not any(ln.strip() for ln in buf):
            out.extend(buf)
            buf = []
            return

        first_nonempty = next((ln for ln in buf if ln.strip()), "")
        if (
            _is_structural_line(first_nonempty)
            or _looks_like_table_block(buf)
            or _keep_bold_label_block(buf)
        ):
            out.extend(buf)
            buf = []
            return

        # Convert a paragraph-like block into a single bullet with wrapped continuation lines.
        for i, ln in enumerate(buf):
            content = ln.strip()
            if not content:
                continue
            if i == 0:
                out.append(f"- {content}")
            else:
                out.append(f"  {content}")
        buf = []

    for ln in lines:
        if _RE_FENCE.match(ln):
            flush_buf()
            in_fence = not in_fence
            out.append(ln)
            continue

        if in_fence:
            out.append(ln)
            continue

        if not ln.strip():
            flush_buf()
            out.append(ln)
            continue

        buf.append(ln)

    flush_buf()
    return "\n".join(out) + ("\n" if markdown.endswith("\n") else "")


def process_notebook(path: Path) -> tuple[int, int]:
    nb = nbformat.read(path, as_version=4)
    changed_cells = 0
    total_md_cells = 0
    for cell in nb.cells:
        if cell.get("cell_type") != "markdown":
            continue
        total_md_cells += 1
        before = cell.get("source", "")
        after = outline_paragraph_blocks(before)
        if after != before:
            cell["source"] = after
            changed_cells += 1

    if changed_cells:
        nbformat.write(nb, path)
    return changed_cells, total_md_cells


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert paragraph-style markdown cells in Jupyter notebooks into 개조식 bullet blocks."
    )
    parser.add_argument("notebooks", nargs="+", type=Path)
    args = parser.parse_args()

    any_changes = False
    for p in args.notebooks:
        changed, total = process_notebook(p)
        any_changes = any_changes or changed > 0
        print(f"{p}: changed_markdown_cells={changed}/{total}")
    return 0 if any_changes else 0


if __name__ == "__main__":
    raise SystemExit(main())

