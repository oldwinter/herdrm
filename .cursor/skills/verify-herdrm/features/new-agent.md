# New Agent

New Agent opens a sheet to pick a device, an advertised agent CLI, a space, and optional bypass-permissions, then starts that agent attached to its live terminal. The default verification opens every entry point and cancels so no CLI is spawned.

## Sub-features

- `new-agent-sidebar` opens the sheet from the sidebar New Agent row.
- `new-agent-menu` opens the sheet from File → New Agent.
- `new-agent-key` opens the sheet with ⌘N.
- `new-agent-placeholder` opens the sheet from the connected empty-state New Agent… button.
- `new-agent-fields` shows AGENT (and DEVICE when more than one device exists), SPACE, and Cancel / Start Agent.
- `new-agent-cancel` dismisses the sheet without starting an agent.
- `new-agent-catalog` shows Checking agents…, a Retry failure, an empty-CLI message, or the kind grid.

## How to get to it (user POV)

- Choose New Agent in the sidebar.
- Choose File → New Agent.
- Press ⌘N while herdrm is focused (this app has no New Window; ⌘N is New Agent).
- When Local is connected and nothing is selected, choose New Agent… in the right-hand placeholder.

## Driving it with control-herdrm

Preconditions:

- `control-herdrm doctor` reports `worth-driving`.
- No sheet is open.
- Do **not** press Start Agent unless a later mutation recipe (not this default) names a disposable kind and a close-the-row cleanup.

- **Sidebar entry.** Choose New Agent. Run `control-herdrm click --name "New Agent"`. `wait --name "New Agent"` succeeds and `Start Agent` is present.
- **Cancel.** Leave the sheet. Run `control-herdrm click --name "Cancel"`. A snapshot no longer contains `Start Agent`.
- **Menu entry.** Open from the menu. Run `control-herdrm menu --path "File>New Agent"`. `wait --name "Start Agent"` succeeds.
- **Cancel again.** Run `control-herdrm key --chord escape`. `Start Agent` is gone.
- **Keyboard entry.** Open with ⌘N. Run `control-herdrm key --chord cmd+n`. `wait --name "New Agent"` and `wait --name "Start Agent"` succeed.
- **Catalog state.** Read the AGENT section. If doctor `herdr_socket` is `accepting` and the footer is connected, expect either a kind grid or `No supported agent CLI was found on this Mac. Install one, or set a binary path in Settings → Agents.` If the socket is down, expect `Checking agents on Local…` or `Couldn’t check installed agent CLIs.` plus `Retry`. Record which of those strings is present; do not require a kind grid on a machine without advertised CLIs.
- **Start Agent disabled.** When no kind is selected / the catalog is empty, `Start Agent` stays disabled. Do not treat a no-op click as a start.
- **Placeholder entry (connected + empty only).** Dismiss the sheet, then if the snapshot contains `New Agent…`, run `control-herdrm click --name "New Agent…"`. The same `New Agent` sheet appears. Cancel.
- **Proof.** Run `control-herdrm snapshot --path "$EVIDENCE/new-agent/sheet.ax.txt"` and `control-herdrm screenshot --path "$EVIDENCE/new-agent/sheet.png"` while the sheet is open on the keyboard entry. Both identify the `New Agent` title and `Start Agent` / `Cancel`. Then cancel so the run ends with no new sidebar agent.

## Gotchas

- ⌘N is New Agent, not New Window. A second window is intentionally not offered.
- `New Agent` (sidebar / menu) and `New Agent…` (placeholder) are different names. The ellipsis variant exists only when Local's connection is `.connected` and nothing is selected.
- Start Agent talks to herdr and attaches with takeover. A green Start Agent click is a mutation of the user's session. The default recipe stops at Cancel.
- Bypass permissions is on by default in the UI when the kind has a known flag; it appears under OPTIONS as the toggle `Bypass permissions`.
- DEVICE is shown only when the app is showing device badges (more than one device, or a non-local filter). A Local-only install may omit that picker.
- After a failed catalog load, Retry calls the server again; wait for the AGENT section to change before asserting empty vs loaded.
