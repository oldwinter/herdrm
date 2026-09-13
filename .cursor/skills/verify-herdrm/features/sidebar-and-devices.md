# Sidebar and devices

The sidebar is how a user sees every Space, Agent, and Terminal on the filtered device set, and how they switch or add SSH machines from the bottom-left footer.

## Sub-features

- `sidebar-visible` shows the 260pt sidebar with New Agent, New Terminal, Files, Search, and the Spaces group.
- `sidebar-toggle` hides and shows the sidebar with ⌘B.
- `spaces-all` selects All Spaces and updates the titlebar placeholder when nothing is attached.
- `agents-empty` distinguishes Connecting…, a connection failure, and No agents.
- `device-footer` shows All Devices or the filtered device name plus a connection dot.
- `device-popover` opens the DEVICES panel with All Devices, Local, and Add Device….
- `add-device-cancel` opens the Add Device sheet and leaves without writing a device.

## How to get to it (user POV)

- Launch herdrm; the sidebar is visible on every cold start (collapse is not persisted).
- Press ⌘B or use the titlebar sidebar button (`Hide Sidebar (⌘B)` / `Show Sidebar (⌘B)`).
- Choose All Spaces under Spaces.
- Choose the footer chip (`All Devices` or a device name) to open the device panel.
- Choose Add Device… in that panel, or add from the same panel after filtering.

## Driving it with control-herdrm

Preconditions:

- `control-herdrm doctor` reports `worth-driving`.
- No sheet or Search is open. Run `control-herdrm reset-ui` if needed.

- **Sidebar chrome.** Read the tree. Run `control-herdrm snapshot --path "$EVIDENCE/sidebar/baseline.ax.txt"`. The snapshot contains `New Agent`, `New Terminal`, `Files`, `Search`, and `Spaces`.
- **Screenshot identity.** Capture the window. Run `control-herdrm screenshot --path "$EVIDENCE/sidebar/baseline.png"`. The image shows the herdrm sidebar and the right-hand placeholder or terminal.
- **Collapse.** Hide the sidebar. Run `control-herdrm key --chord cmd+b`. `New Agent` is absent from a new snapshot and the titlebar still reads `No terminal selected` or an attached title.
- **Reveal.** Show the sidebar again. Run `control-herdrm key --chord cmd+b`. `New Agent` is present again.
- **All Spaces.** Choose All Spaces. Run `control-herdrm click --name "All Spaces"`. The control stays selected; the right pane does not open a sheet.
- **Empty agents.** Read the Agents group. If doctor `herdr_socket` is not `accepting`, the Agents area or placeholder may show `Connecting…` or a failure string — record that string; do not treat it as `No agents`.
- **Device footer.** Open the switcher. Run `control-herdrm click --name "All Devices"` (or `Local` if a filter is already on). `wait --name "DEVICES"` succeeds and `Add Device…` is present.
- **Add Device sheet.** Choose Add Device…. Run `control-herdrm click --name "Add Device…"`. `wait --name "Add Device"` succeeds. The sheet subtitle mentions OpenSSH / Tailscale / password.
- **Cancel add.** Leave without saving. Run `control-herdrm click --name "Cancel"`. `Add Device` is gone from the snapshot and `devices.json` was not the thing we edited — prove it by the footer still listing the same names as the baseline snapshot (still `Local` / `All Devices`, no extra chip).
- **Proof.** Keep `$EVIDENCE/sidebar/baseline.ax.txt` and `$EVIDENCE/sidebar/baseline.png`. They identify herdrm, the sidebar actions, and Spaces.

## Gotchas

- Collapse is in-memory only. A relaunch always shows the sidebar; do not expect ⌘B to persist.
- The footer button's name is the current filter (`All Devices` or `Local` or an SSH device name), not a fixed `Device switcher` label.
- `All Devices` appears both as the footer chip and as a row inside the popover. After opening the popover, prefer `Add Device…` or a specific device name rather than clicking `All Devices` again unless the recipe is closing the aggregate row.
- Clicking a space or agent selects it and may attach a PTY (`--takeover`). Stay on All Spaces and chrome for this feature unless you are also running the Terminal map.
- Language: zh-Hans users will see translated chrome unless this run used `control-herdrm launch` (which forces English and restores it on cleanup).
- Do not add a real SSH device in the default recipe. `Add Device` stays disabled until SSH TARGET is non-empty; filling it and confirming writes `~/Library/Application Support/HerdrM/devices.json`.
