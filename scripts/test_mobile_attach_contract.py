"""Regression contracts for mobile attach lifecycle and bootstrap boundaries."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TERMINAL = ROOT / "Sources" / "HerdrMobile" / "MobileTerminalView.swift"
TRANSPORT = ROOT / "Sources" / "HerdrMobile" / "MobileTransport.swift"


class TestMobileAttachContract(unittest.TestCase):
    def test_open_task_is_owned_and_cancelled(self) -> None:
        source = TERMINAL.read_text(encoding="utf-8")
        self.assertIn("private var startTask: Task<Void, Never>?", source)
        self.assertIn("startTask?.cancel()", source)
        self.assertIn("attachGeneration", source)
        self.assertIn("generation == attachGeneration", source)
        self.assertIn("await channel.close", source)

    def test_bootstrap_gate_flushes_at_the_limit(self) -> None:
        source = TERMINAL.read_text(encoding="utf-8")
        self.assertIn("bootstrapBuffer.count >= 8192", source)
        self.assertNotIn("bootstrapBuffer.count > 8192", source)

    def test_event_stream_validates_ack_events_and_line_size(self) -> None:
        source = TRANSPORT.read_text(encoding="utf-8")
        self.assertIn("SocketRPC.decodeResponse(Data(line))", source)
        self.assertIn("SocketRPC.decodeEvent(Data(line))", source)
        self.assertIn("buffer.count > SocketRPC.maximumLineBytes", source)
        self.assertNotIn("try? JSONDecoder().decode(JSONValue.self, from: line)", source)


if __name__ == "__main__":
    unittest.main()
