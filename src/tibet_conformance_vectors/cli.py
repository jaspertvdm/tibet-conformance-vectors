"""
tibet-vectors CLI — runner for conformance vectors.

Provides a simple command-line entrypoint for external evaluators:

  $ tibet-vectors list
  $ tibet-vectors show trusted-001
  $ tibet-vectors check <audit.jsonl>

v0.1.1 — peer-feedback Richard Barron 12 mei 2026:
the pyproject.toml declared `tibet-vectors = "tibet_conformance_vectors.cli:main"`
but the module didn't exist. This file fills that gap.
"""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__, load_vectors, get_vector, iter_categories


def _cmd_list(args: argparse.Namespace) -> int:
    """List all vectors in a vector set."""
    vectors = load_vectors(args.version)
    if args.json:
        print(json.dumps(
            [{
                "vector_id": v.get("vector_id"),
                "category": v.get("category"),
                "scope": v.get("scope"),
            } for v in vectors],
            indent=2,
        ))
        return 0
    print(f"tibet-conformance-vectors {args.version} ({len(vectors)} vectors)")
    print()
    for v in vectors:
        print(
            f"  {v.get('vector_id'):<20} {v.get('category'):<12} "
            f"scope={v.get('scope')}"
        )
    print()
    cats = list(iter_categories(args.version))
    print(f"Categories: {', '.join(cats)}")
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    """Show a single vector's full content."""
    v = get_vector(args.vector_id, version=args.version)
    if not v:
        print(f"ERROR: no vector with id '{args.vector_id}'", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(v, indent=2, sort_keys=True))
        return 0
    print(f"Vector: {v.get('vector_id')}")
    print(f"  category:        {v.get('category')}")
    print(f"  scope:           {v.get('scope')}")
    print(f"  vector_version:  {v.get('vector_version')}")
    print(f"  filename:        {v.get('filename')}")
    if "expected_audit" in v:
        ea = v["expected_audit"]
        print(f"  expected disposition: {ea.get('disposition_hint')}")
        print(f"  expected intake_class: {ea.get('intake_class')}")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    """Read an audit JSONL and compare against expected vectors."""
    vectors = load_vectors(args.version)
    expected = {v["vector_id"]: v for v in vectors}
    seen: dict = {}
    try:
        with open(args.audit_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                name = rec.get("name", "")
                for vid, v in expected.items():
                    if v.get("filename") == name:
                        seen.setdefault(vid, []).append(rec)
    except OSError as e:
        print(f"ERROR: cannot read audit file: {e}", file=sys.stderr)
        return 2

    passes = 0
    fails = 0
    for vid, v in expected.items():
        records = seen.get(vid, [])
        if not records:
            print(f"  ✗ {vid:<20} no audit records found")
            fails += 1
            continue
        ea = v.get("expected_audit", {})
        expected_disp = ea.get("disposition_hint")
        actual_disps = [r.get("disposition_hint") for r in records]
        if expected_disp in actual_disps:
            print(f"  ✓ {vid:<20} disposition={expected_disp}")
            passes += 1
        else:
            print(
                f"  ✗ {vid:<20} expected={expected_disp} got={actual_disps}"
            )
            fails += 1

    print()
    print(f"Total: {passes} pass / {fails} fail / {len(expected)} vectors")
    return 0 if fails == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tibet-vectors",
        description="Run TIBET conformance vectors and check audit output.",
    )
    parser.add_argument(
        "-V", "--version", action="version",
        version=f"tibet-vectors {__version__}",
    )
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="List all vectors")
    p_list.add_argument("--version", dest="version", default="v1")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=_cmd_list)

    p_show = sub.add_parser("show", help="Show a single vector")
    p_show.add_argument("vector_id")
    p_show.add_argument("--version", dest="version", default="v1")
    p_show.add_argument("--json", action="store_true")
    p_show.set_defaults(func=_cmd_show)

    p_check = sub.add_parser(
        "check",
        help="Check an audit JSONL against expected vectors",
    )
    p_check.add_argument("audit_path", help="Path to audit JSONL")
    p_check.add_argument("--version", dest="version", default="v1")
    p_check.set_defaults(func=_cmd_check)

    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
