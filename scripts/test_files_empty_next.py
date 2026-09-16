"""Lock Files empty-folder and listing-error next steps."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ROOT / "Sources" / "HerdrM" / "DeviceFilesView.swift"
SEARCH = ROOT / "Sources" / "HerdrM" / "SearchView.swift"
MOBILE = ROOT / "Sources" / "HerdrMobile" / "MobileRootView.swift"


class TestFilesEmptyNext(unittest.TestCase):
    def test_empty_folder_offers_hidden_and_home(self) -> None:
        source = FILES.read_text(encoding="utf-8")
        self.assertIn('Label("Empty Folder", systemImage: "folder")', source)
        self.assertIn('Text("This folder contains no visible items.")', source)
        self.assertIn('if !browser.includesHidden', source)
        self.assertIn('Button("Show hidden files")', source)
        self.assertIn("browser.toggleHidden()", source)
        self.assertIn('Button("Home folder")', source)
        self.assertIn("browser.goHome()", source)

    def test_listing_error_is_in_the_main_pane(self) -> None:
        source = FILES.read_text(encoding="utf-8")
        self.assertIn("if !browser.isLoading, let error = browser.error", source)
        self.assertIn('Label(error, systemImage: "exclamationmark.triangle")', source)
        self.assertIn('Button("Retry")', source)
        self.assertIn("browser.refresh()", source)
        self.assertIn('Button("Parent folder")', source)
        self.assertIn("browser.goUp()", source)
        self.assertGreater(source.find("let error = browser.error"), source.find("var listing"))

    def test_does_not_retouch_search_or_empty_agents(self) -> None:
        search = SEARCH.read_text(encoding="utf-8")
        mobile = MOBILE.read_text(encoding="utf-8")
        self.assertIn('Text("No matches")', search)
        self.assertIn('String(localized: "No agents")', mobile)
        self.assertIn(
            'String(localized: "Pick an agent to attach to its terminal.")',
            mobile,
        )


if __name__ == "__main__":
    unittest.main()
