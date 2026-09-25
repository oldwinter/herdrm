"""Lock the mobile event-pump failure to the catalogued drop copy."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOBILE_MODEL = ROOT / "Sources" / "HerdrMobile" / "MobileAppModel.swift"
MOBILE_TERMINAL = ROOT / "Sources" / "HerdrMobile" / "MobileTerminalView.swift"
CATALOG = ROOT / "Resources" / "Localizable.xcstrings"


class TestConnectionLostCopy(unittest.TestCase):
    def test_event_pump_reuses_mac_drop_copy(self) -> None:
        source = MOBILE_MODEL.read_text(encoding="utf-8")
        self.assertIn(
            'String(localized: "Connection to \\(self.device.name) dropped")',
            source,
        )
        self.assertNotIn('String(localized: "Connection lost")', source)

    def test_catalog_already_has_drop_copy(self) -> None:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        strings = catalog["strings"]
        self.assertNotIn("Connection lost", strings)
        entry = strings["Connection to %@ dropped"]
        self.assertEqual(
            entry["localizations"]["zh-Hans"]["stringUnit"]["value"],
            "与 %@ 的连接已断开",
        )

    def test_pty_session_ended_path_untouched(self) -> None:
        source = MOBILE_TERMINAL.read_text(encoding="utf-8")
        self.assertIn(
            'self.status = .ended(String(localized: "Session ended"))',
            source,
        )


if __name__ == "__main__":
    unittest.main()
