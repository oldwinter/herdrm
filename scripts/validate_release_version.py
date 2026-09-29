#!/usr/bin/env python3
"""Validate a release tag and print its MARKETING_VERSION assignment."""

from __future__ import annotations

import re
import sys

SEMVER_TAG = re.compile(
    r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def version_from_tag(tag: str) -> str:
    if not SEMVER_TAG.fullmatch(tag):
        raise ValueError(f"release tag must be semantic version vMAJOR.MINOR.PATCH: {tag}")
    return tag[1:]


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_release_version.py vMAJOR.MINOR.PATCH", file=sys.stderr)
        return 2
    try:
        version = version_from_tag(argv[1])
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    print(f"VERSION={version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
