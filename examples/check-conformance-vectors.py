#!/usr/bin/env python3
"""
Decode transport-canonical continuityd vectors and validate expected sniff results.

This does not require the live daemon; it validates vectors directly against
the current sniff implementation for deterministic local checks.
"""
from __future__ import annotations

import argparse
import base64
import json
import tempfile
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--vectors", type=Path, required=True)
    p.add_argument("--continuityd-src", type=Path,
                   default=Path("/srv/jtel-stack/packages/tibet-continuityd/src"))
    args = p.parse_args()

    import sys

    sys.path.insert(0, str(args.continuityd_src))
    from tibet_continuityd.sniff import sniff_payload  # type: ignore

    records = []
    for line in args.vectors.read_text().splitlines():
        if line.strip():
            records.append(json.loads(line))

    failures = 0
    with tempfile.TemporaryDirectory(prefix="cont-vectors-") as td:
        base = Path(td)
        for rec in records:
            target = base / rec["filename"]
            target.write_bytes(base64.b64decode(rec["content_base64"]))
            actual = sniff_payload(target).to_dict()
            actual["name"] = rec["filename"]
            actual["stage"] = "sniff"
            actual["coalesced"] = False
            expected = rec["expected_audit"]

            # current v1 vectors only assert the semantic subset
            vector_failures = 0
            for key, exp in expected.items():
                act = actual.get(key)
                if act != exp:
                    failures += 1
                    vector_failures += 1
                    print(
                        f"FAIL vector={rec['vector_id']} key={key} "
                        f"expected={exp!r} actual={act!r}"
                    )
            if vector_failures == 0:
                print(f"OK   vector={rec['vector_id']} file={rec['filename']}")

    if failures:
        print(f"failures={failures}")
        return 1
    print("all vectors passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
