"""
tibet-conformance-vectors — canonical conformance vectors for the
TIBET continuity ecosystem.

Reference inputs that external evaluators and implementers use to
validate any tibet-* implementation against the documented spec.
Independent of any specific implementation; ships alongside the
IETF drafts it traces against.

Quick API:

    from tibet_conformance_vectors import load_vectors, get_vector

    vectors = load_vectors("v1")        # all vectors in the v1 set
    trusted = get_vector("trusted-001") # one specific vector
"""
from __future__ import annotations

import json
from importlib import resources
from typing import Iterator, Optional


__version__ = "0.1.1"
__author__ = "Jasper van de Meent, Root AI, Codex"


def _parse_pretty_jsonl(text: str) -> list[dict]:
    """Parse JSONL files that may be pretty-printed across lines.

    Conformance vector files in this package are formatted with
    indented JSON for readability; the standard json.loads(line) loop
    breaks on them. This walks the brace-depth so we can ingest both
    flat and pretty-printed forms.
    """
    objects: list[dict] = []
    buf = ""
    depth = 0
    for ch in text:
        buf += ch
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                stripped = buf.strip()
                if stripped:
                    objects.append(json.loads(stripped))
                buf = ""
    return objects


def load_vectors(version: str = "v1") -> list[dict]:
    """Load all conformance vectors for the given version.

    Args:
        version: Vector set version (e.g. "v1"). Maps to data/v1.jsonl.

    Returns:
        List of vector dicts. Each carries: vector_id, category,
        scope, vector_version, filename, content_base64, expected_audit.
    """
    filename = f"{version}.jsonl"
    text = (
        resources.files("tibet_conformance_vectors.data")
        .joinpath(filename)
        .read_text(encoding="utf-8")
    )
    return _parse_pretty_jsonl(text)


def get_vector(
    vector_id: str, version: str = "v1"
) -> Optional[dict]:
    """Fetch a single vector by id."""
    for v in load_vectors(version):
        if v.get("vector_id") == vector_id:
            return v
    return None


def iter_categories(version: str = "v1") -> Iterator[str]:
    """Yield the distinct category labels present in a vector set."""
    seen = set()
    for v in load_vectors(version):
        c = v.get("category")
        if c and c not in seen:
            seen.add(c)
            yield c


__all__ = [
    "__version__",
    "load_vectors",
    "get_vector",
    "iter_categories",
]


def drafts_path():
    """Return Path to bundled IETF drafts directory (v0.1.1+)."""
    from importlib import resources
    return resources.files("tibet_conformance_vectors").joinpath("drafts")


def list_drafts() -> list[str]:
    """List IETF draft files bundled with this package (v0.1.1+)."""
    return sorted(
        p.name for p in drafts_path().iterdir()
        if p.is_file() and not p.name.startswith("__")
    )
