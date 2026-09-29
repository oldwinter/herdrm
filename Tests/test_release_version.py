from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate_release_version import version_from_tag


class TestReleaseVersion(unittest.TestCase):
    def test_accepts_semantic_versions(self) -> None:
        self.assertEqual(version_from_tag("v1.2.3"), "1.2.3")
        self.assertEqual(version_from_tag("v2.0.0-rc.1"), "2.0.0-rc.1")
        self.assertEqual(version_from_tag("v2.0.0+build.7"), "2.0.0+build.7")

    def test_rejects_non_semantic_release_tags(self) -> None:
        for tag in ("vfoo", "v1", "v1.2", "1.2.3", "v01.2.3", "v1.02.3"):
            with self.subTest(tag=tag):
                with self.assertRaises(ValueError):
                    version_from_tag(tag)


if __name__ == "__main__":
    unittest.main()
