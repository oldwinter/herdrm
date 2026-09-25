"""Lock mobile empty-Agents next steps."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOBILE = ROOT / "Sources" / "HerdrMobile" / "MobileRootView.swift"
MODEL = ROOT / "Sources" / "HerdrMobile" / "MobileAppModel.swift"
FILES = ROOT / "Sources" / "HerdrM" / "DeviceFilesView.swift"
SEARCH = ROOT / "Sources" / "HerdrM" / "SearchView.swift"
CATALOG = ROOT / "Resources" / "Localizable.xcstrings"


class TestEmptyAgentsNext(unittest.TestCase):
    def test_space_empty_offers_all_spaces(self) -> None:
        source = MOBILE.read_text(encoding="utf-8")
        self.assertIn('String(localized: "No agents in this space")', source)
        self.assertIn(
            'String(localized: "Look in All Spaces, or start one on the Mac running herdr.")',
            source,
        )
        self.assertIn('Button(String(localized: "All Spaces"))', source)
        self.assertIn("model.selectedSpaceID = nil", source)
        self.assertIn("selectedSpaceID != nil && !model.deviceAgents.isEmpty", source)

    def test_device_empty_points_at_mac_herdr(self) -> None:
        source = MOBILE.read_text(encoding="utf-8")
        model = MODEL.read_text(encoding="utf-8")
        self.assertIn(
            'String(localized: "Start an agent on the Mac running herdr.")',
            source,
        )
        self.assertIn("var deviceAgents:", model)
        self.assertNotIn('String(localized: "New Agent")', source)
        self.assertNotIn('Button("New Agent")', source)

    def test_detail_does_not_say_pick_when_empty(self) -> None:
        source = MOBILE.read_text(encoding="utf-8")
        self.assertIn("isConnectedEmptyAgents(model)", source)
        self.assertIn("EmptyAgentsGuidance(model: model, compact: false)", source)
        self.assertIn(
            'String(localized: "Pick an agent to attach to its terminal.")',
            source,
        )

    def test_catalog_covers_empty_copy(self) -> None:
        strings = json.loads(CATALOG.read_text(encoding="utf-8"))["strings"]
        self.assertEqual(
            strings["No agents in this space"]["localizations"]["zh-Hans"]["stringUnit"]["value"],
            "此空间暂无 Agent",
        )
        self.assertEqual(
            strings["Start an agent on the Mac running herdr."]["localizations"]["zh-Hans"]["stringUnit"]["value"],
            "到 Mac 上的 herdr 里启动 Agent。",
        )

    def test_does_not_retouch_search_or_files(self) -> None:
        files = FILES.read_text(encoding="utf-8")
        search = SEARCH.read_text(encoding="utf-8")
        self.assertIn('Text("No matches")', search)
        self.assertIn('"Empty Folder"', files)
        self.assertIn("This folder contains no visible items.", files)
        self.assertNotIn('Button("Show hidden files")', files)


if __name__ == "__main__":
    unittest.main()
