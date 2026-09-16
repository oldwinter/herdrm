"""Lock the mobile attach empty / ended / reconnect path."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TERMINAL = ROOT / "Sources" / "HerdrMobile" / "MobileTerminalView.swift"
ROOT_VIEW = ROOT / "Sources" / "HerdrMobile" / "MobileRootView.swift"
FILES = ROOT / "Sources" / "HerdrM" / "DeviceFilesView.swift"
CATALOG = ROOT / "Resources" / "Localizable.xcstrings"


class TestIPhoneSessionEnded(unittest.TestCase):
    def test_connecting_is_not_a_blank_terminal(self) -> None:
        source = TERMINAL.read_text(encoding="utf-8")
        self.assertIn('String(localized: "Attaching…")', source)
        self.assertIn("ProgressView()", source)
        self.assertIn("case .connecting:", source)
        self.assertIn("statusOverlay", source)

    def test_ended_copy_reuses_mac_reasons(self) -> None:
        source = TERMINAL.read_text(encoding="utf-8")
        self.assertNotIn('String(localized: "Session ended")', source)
        self.assertIn('String(localized: "Couldn\'t attach")', source)
        self.assertIn('String(localized: "Terminal session ended")', source)
        self.assertIn(
            'String(localized: "The SSH connection behind this terminal went away.")',
            source,
        )
        self.assertIn(
            'String(localized: "Another client took this pane over, or the attach closed.")',
            source,
        )
        self.assertNotIn("exitStatus(", source)

    def test_reconnect_uses_last_grid_not_80x24(self) -> None:
        source = TERMINAL.read_text(encoding="utf-8")
        self.assertIn("func reconnect()", source)
        self.assertIn("start(columns: lastColumns, rows: lastRows)", source)
        self.assertNotIn("start(columns: 80, rows: 24)", source)
        self.assertIn("lastColumns = columns", source)
        self.assertIn("lastRows = rows", source)

    def test_composer_disabled_when_not_running(self) -> None:
        source = TERMINAL.read_text(encoding="utf-8")
        self.assertIn(".disabled(!isLive)", source)
        self.assertIn("if case .running = session.status", source)

    def test_catalog_covers_new_attach_copy(self) -> None:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        strings = catalog["strings"]
        self.assertEqual(
            strings["Attaching…"]["localizations"]["zh-Hans"]["stringUnit"]["value"],
            "正在接入…",
        )
        self.assertEqual(
            strings["Couldn't attach"]["localizations"]["zh-Hans"]["stringUnit"]["value"],
            "未能接入终端",
        )
        self.assertNotIn("Session ended", strings)

    def test_does_not_retouch_files_or_empty_agents(self) -> None:
        root = ROOT_VIEW.read_text(encoding="utf-8")
        files = FILES.read_text(encoding="utf-8")
        self.assertIn('String(localized: "No agents")', root)
        self.assertIn(
            'String(localized: "Pick an agent to attach to its terminal.")',
            root,
        )
        self.assertIn('"Empty Folder"', files)
        self.assertIn("This folder contains no visible items.", files)


if __name__ == "__main__":
    unittest.main()
