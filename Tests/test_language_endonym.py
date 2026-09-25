"""Lock the language-picker fallback to the catalog endonym."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_LANGUAGE = ROOT / "Sources" / "HerdrM" / "AppLanguage.swift"


class TestLanguageEndonym(unittest.TestCase):
    def test_simplified_chinese_fallback_is_endonym(self):
        source = APP_LANGUAGE.read_text(encoding="utf-8")
        self.assertIn(
            'String(localized: "language.name.zh-Hans", defaultValue: "简体中文")',
            source,
        )
        self.assertNotIn('defaultValue: "Chinese"', source)


if __name__ == "__main__":
    unittest.main()
