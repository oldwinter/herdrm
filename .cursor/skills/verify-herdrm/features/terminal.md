# Terminal

The right-hand pane attaches a real PTY (`herdr agent attach` / `herdr terminal attach --takeover`) or hosts an app-owned standalone shell. With nothing selected, it shows a placeholder. A dropped attach shows Reconnect instead of freezing on the last frame.

## Sub-features

- `terminal-placeholder` shows No terminal selected plus a body string that depends on connection and space filter.
- `terminal-new-agent-cta` shows New Agent… when Local is connected and the pane is empty.
- `terminal-reconnect-device` shows Reconnect when a device is in a failed, reconnectable state.
- `terminal-attach` (mutation) opens a live PTY after choosing an agent or herdr terminal in the sidebar.
- `terminal-ended` shows Terminal session ended or Connection to <device> dropped with Reconnect.
- `terminal-split` offers Terminal → Split Vertically (⌘D) / Split Horizontally (⇧⌘D) only while a pane is attached.
- `new-terminal-sheet` opens New Terminal (⌘T) with Standalone (not in a space) and Cancel / Open Terminal.

## How to get to it (user POV)

- Launch herdrm and look at the right-hand pane without selecting a row.
- Choose an agent or a Terminals row in the sidebar.
- Choose New Terminal in the sidebar, File → New Terminal, or ⌘T.
- After a takeover or a dropped SSH attach, choose Reconnect.
- With a pane attached, use the Terminal menu to split or focus panes.

## Driving it with control-herdrm

Preconditions:

- `control-herdrm doctor` reports `worth-driving`.
- Default recipe stays on the placeholder and the New Terminal sheet. Attaching or Open Terminal is a mutation.

- **Placeholder chrome.** Read the titlebar. Run `control-herdrm snapshot --path "$EVIDENCE/terminal/placeholder.ax.txt"`. The dump contains `No terminal selected` or an attached title — on a fresh launch with no selection it is `No terminal selected`.
- **Placeholder body.** The body is exactly one of: `Connecting…`, a connection-failure sentence, `No agents or terminals in this space yet` (a space is selected and that space is empty), or `Select an agent or terminal, or start a new one`. Record which. If the footer is connected, `New Agent…` may also be present.
- **Screenshot.** Run `control-herdrm screenshot --path "$EVIDENCE/terminal/placeholder.png"`. The image shows the sidebar and the empty or live right pane.
- **New Terminal sheet.** Open the sheet. Run `control-herdrm key --chord cmd+t`. `wait --name "New Terminal"` and `wait --name "Open Terminal"` succeed. The SPACE picker includes `Standalone (not in a space)`. Standalone subtitle is `Start a login shell on this Mac` (Local) or `Connect to <device> over SSH`, plus `Runs in this app only; closing herdrm ends the shell.`
- **Cancel New Terminal.** Run `control-herdrm click --name "Cancel"`. `Open Terminal` is gone. No new TERMINALS row and no standalone shell title appear.
- **Split menu disabled (no attach).** With nothing attached, `control-herdrm menu --path "Terminal>Split Vertically"` should fail or no-op because the item is disabled. Do not treat a missing split as a live split. Record that the placeholder is still showing.
- **Attach (only when the map run is explicitly proving attach).** Choose a sidebar agent by its AX label (`"<title>"` or `"<title>, Working"` / `", Needs input"` / `", Unread"`). The titlebar then shows that title (and Working / Needs input / Done when those apply) instead of `No terminal selected`. This takeovers the pane. Prefer a disposable pane. After proof, do not leave a split open; ⌘W closes a split first.
- **Ended overlay (only if the attach already ended).** Expect `Terminal session ended` (non-255) or `Connection to <device> dropped` (ssh exit 255) and button `Reconnect`.
- **Proof.** Keep the placeholder snapshot/screenshot. They show herdrm identity and `No terminal selected`. The cancelled New Terminal sheet must not leave a new row.

## Gotchas

- `Open Terminal` on a herdr space creates a persistent server-owned pane. Standalone creates an app-owned shell that dies when herdrm quits. Both are mutations; cancel is the default.
- Attach is `--takeover`. Driving this against the user's daily session steals their TUI. Refuse if doctor `owned` is not `yes`.
- ⌘W closes split, then a selected standalone shell, then the window. Do not press it to "go back" from the placeholder — it can quit the app you are verifying.
- Split Vertically / Horizontally stay disabled while the placeholder is on screen. A disabled menu item will not fire its key equivalent.
- ⌘D with an attach opens a local shell beside the agent; the next ⌘W closes that split, not the window.
- `Reconnect` on the ended overlay remounts the attach view. `Reconnect` on the empty placeholder retries failed device sessions. They are different buttons in different states.
- Selecting a Files-active window's agent is a different feature; if the titlebar says `Files`, click an agent or press Escape / choose a row to leave Files before asserting terminal chrome.
- Do not run `control-herdrm snapshot` against a busy attached TUI. The harness walks `entire contents` of window 1 and SwiftTerm can stall that.
