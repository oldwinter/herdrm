"""Static release and pull-request workflow safety contracts."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CI = ROOT / ".github" / "workflows" / "ci.yml"
RELEASE = ROOT / ".github" / "workflows" / "release.yml"
PROJECT = ROOT / "project.yml"


class TestWorkflowContract(unittest.TestCase):
    def test_pull_requests_run_all_repository_test_surfaces(self) -> None:
        source = CI.read_text(encoding="utf-8")
        self.assertIn("pull_request:", source)
        self.assertIn("python3 -m unittest discover -s Tests", source)
        self.assertIn("python3 -m unittest discover -s scripts", source)
        self.assertIn("cd Packages/HerdrKit && swift test", source)
        self.assertIn("CODE_SIGNING_ALLOWED=NO", source)
        self.assertIn("-scheme HerdrM", source)
        self.assertIn("-scheme HerdrMobile", source)

    def test_release_validates_tag_before_signing(self) -> None:
        source = RELEASE.read_text(encoding="utf-8")
        validation = source.index("Validate release tag")
        certificate = source.index("Import Developer ID certificate")
        self.assertLess(validation, certificate)
        self.assertIn('python3 scripts/validate_release_version.py "$GITHUB_REF_NAME"', source)

    def test_sparkle_archive_is_digest_verified(self) -> None:
        source = RELEASE.read_text(encoding="utf-8")
        self.assertIn(
            "SPARKLE_SHA256: 52bf9e88cdd972fc0c81501377a880e90d47031bd8ca5462488f843e2609e192",
            source,
        )
        self.assertIn("curl --fail --location --silent --show-error", source)
        self.assertIn('echo "$SPARKLE_SHA256  sparkle.tar.xz" | shasum -a 256 -c -', source)

    def test_maintainer_team_is_release_only(self) -> None:
        source = PROJECT.read_text(encoding="utf-8")
        self.assertEqual(source.count("DEVELOPMENT_TEAM: NCFNX3LJ83"), 2)
        self.assertNotIn("# real identity so UserNotifications", source)
        self.assertIn('CODE_SIGN_IDENTITY: "-"', source)


if __name__ == "__main__":
    unittest.main()
