---
name: verify-herdrm
description: "Drive the herdrm macOS console (SwiftUI sidebar + embedded terminal) through Accessibility. Use when proving user-visible behavior, after changing Sources/HerdrM or the session/UI flow in HerdrKit, or when asked to verify herdrm in the running app."
---

# Verify herdrm

herdrm is a native macOS 14+ SwiftUI console for [herdr](https://herdr.dev). The user-facing surface is one window: a 260pt sidebar (Spaces / Agents / Terminals + a bottom-left device switcher) and a right-hand pane that is either an attached PTY or the two-pane Files workspace. There is no web UI, no `herdrmctl` (that CLI is still a design in `docs/AI_AGENT_CONTROL_PLANE.md`), and no XCUITest target.

Secondary surfaces this skill does **not** drive:

- **HerdrMobile** (`Sources/HerdrMobile`, iOS 18) — SSH-only, no local herdr. Needs a simulator/device harness that this repo does not ship.
- **HerdrKit / HerdrSSH unit tests** (`make kit-test`) — library tests, not the user path. Useful as a complement; never a substitute for a GUI proof.
- **Installed Homebrew / Sparkle builds** — only use `/Applications/herdrm.app` when the user explicitly asks to verify a release. Default is the repo Debug bundle.

The next agent reading this has never seen the app. Follow the sections below literally.

## Launch

Harness (from the repository root):

```sh
.cursor/skills/verify-herdrm/scripts/control-herdrm launch
.cursor/skills/verify-herdrm/scripts/control-herdrm doctor
```

`launch` builds `build/Build/Products/Debug/herdrm.app` when it is missing (`xcodegen` + `xcodebuild`; if the Developer ID identity is absent it retries ad-hoc unsigned), forces English via `defaults` for the `dev.bybee.herdrm` domain so Accessibility names match this map, then `open`s that bundle.

Ready when `control-herdrm doctor` prints `verdict: worth-driving`: the process `herdrm` is running, its argv path is the Debug bundle this run opened, System Events can see window 1, and the recorded PID is the only `herdrm` PID.

Teardown:

```sh
.cursor/skills/verify-herdrm/scripts/control-herdrm cleanup
```

`cleanup` Apple-Event-quits **only** the PID `launch` recorded, restores the previous `app.language` / `AppleLanguages` values, and deletes `/tmp/herdrm-verify/state.env`. It never stops `herdr server` and never deletes proof files.

Override the bundle with `HERDRM_APP=/Applications/herdrm.app` only for an explicit release check. Evidence directory override: `HERDRM_VERIFY_EVIDENCE=/absolute/path`.

There is no long-lived HTTP port. herdrm is a desktop app. Local herdr, if missing, is started by the app itself (`LocalHerdrServer` → `herdr server`) against `~/.config/herdr/herdr.sock`.

## Doctor

Run this first, and again whenever the window does something surprising:

```sh
.cursor/skills/verify-herdrm/scripts/control-herdrm doctor
.cursor/skills/verify-herdrm/scripts/control-herdrm doctor --json
```

Worth driving only when **all** of these are true:

| Check | Pass |
| --- | --- |
| Host | `uname` is Darwin |
| Process | exactly one `herdrm` PID, equal to the PID in `/tmp/herdrm-verify/state.env` |
| Bundle | that PID's executable path contains `build/Build/Products/Debug/herdrm.app` (or `$HERDRM_APP`) |
| Window | System Events reports at least one window |
| AX | `System Events` can list processes (Accessibility granted to the driving terminal / Cursor) |

`herdr_socket: accepting` means `~/.config/herdr/herdr.sock` accepts a Unix-socket connection. Sidebar chrome, Search, and sheet **open/cancel** work without it. Features that list agents, attach a PTY, or create a herdr-owned pane require `accepting` **and** a green connection (sidebar footer "Local" + green dot, or the placeholder is not a connection failure string).

Refuse to drive when:

- the host is not macOS — report `verified-unreachable` with prerequisite `macOS 14+, Xcode / xcodegen, Accessibility permission`
- `herdrm` is already running and this run did not launch it — a second instance shares `~/Library/Application Support/HerdrM/devices.json` and the default herdr socket; `herdr agent attach --takeover` steals the user's pane
- doctor `owned` is `foreign` or `unknown`

Do not start a second copy with `open -n`.

## Drive

All driving goes through `control-herdrm`. Prefer the named handles below over coordinates.

```sh
H=.cursor/skills/verify-herdrm/scripts/control-herdrm
$H click --name "New Agent"
$H click --name "New Terminal"
$H click --name "Files"
$H click --name "Search"
$H key --chord cmd+n          # File → New Agent
$H key --chord cmd+t          # File → New Terminal
$H key --chord cmd+shift+n    # File → New Space
$H key --chord cmd+k          # Search sheet
$H key --chord cmd+b          # toggle sidebar
$H key --chord cmd+d          # Terminal → Split Vertically (needs an attached pane)
$H key --chord cmd+w          # close split, then standalone terminal, then window — avoid unless the recipe says so
$H menu --path "File>New Agent"
$H menu --path "Terminal>Split Vertically"
$H type --text "volcano"
$H key --chord escape         # cancel sheet / search / device popover
$H wait --name "Start Agent" --timeout 8
$H reset-ui                   # Escape × 3
```

Stable English Accessibility / UI names (launch forces `en`):

| Surface | Handle |
| --- | --- |
| Sidebar actions | buttons `New Agent`, `New Terminal`, `Files`, `Search` |
| Sidebar groups | disclosure buttons `Spaces`, `Agents`, `Terminals` |
| Spaces | button `All Spaces`; each space row AX label is `"<space label>"` plus `, Working` / `, Needs input` / `, Unread` when that attention applies |
| Agents | AX label `"<title>"` plus `, Working` / `, Needs input` / `, Unread` |
| Device footer | button whose name is `All Devices` or the filtered device name (`Local` is the built-in device) |
| Device popover | heading `DEVICES`; buttons `All Devices`, each device name, `Add Device…` |
| Search field | text field `Search agents, terminals, and spaces…` |
| Search empty | static text `No matches` |
| Search status | agent rows may show `needs input` |
| Placeholder | `No terminal selected` in the titlebar; body `Connecting…`, a connection-failure string, `No agents or terminals in this space yet`, or `Select an agent or terminal, or start a new one`; connected empty state also has button `New Agent…` or `Reconnect` |
| New Agent sheet | title `New Agent`; sections `DEVICE`, `AGENT`, `SPACE`, optional `OPTIONS`; toggle `Bypass permissions`; buttons `Cancel`, `Start Agent` |
| New Terminal sheet | title `New Terminal`; picker includes `Standalone (not in a space)`; buttons `Cancel`, `Open Terminal` |
| New Space sheet | title `New Space`; button `Create Space`; `Browse…` for the directory |
| Add Device sheet | title `Add Device`; fields with placeholders `mac-studio` and `vincent@10.10.10.87`; buttons `Cancel`, `Add Device` |
| Files titlebar | static text `Files`; panes titled `Local` and the target device name; help strings `Parent folder`, `Home folder`, `Refresh`, `Show hidden files` / `Hide hidden files`; conflict dialog `File Already Exists` with `Replace`, `Keep Both`, `Cancel` |
| Attach ended | `Terminal session ended` or `Connection to <device> dropped` with button `Reconnect` |
| Alerts | `Something went wrong`; close confirms titled `Close space "<name>" on <device>?` or `Close "<name>"?` with `Close` / `Cancel` |

Read `.cursor/skills/verify-herdrm/features/README.md` and the matching feature file before driving. A proof that only exercises one convenient entry point is incomplete when that file lists others.

Default recipes **open a sheet or Search and cancel**. Creating an agent, a herdr-owned terminal, or attaching a pane talks to the user's real herdr session and `--takeover`s an attach. Only mutate when the feature file's recipe says so, use a disposable name, and close the row from the sidebar confirm dialog afterward.

After any failed drive: `doctor`, then `reset-ui` (or `cleanup` + `launch` if the window is wedged). Do not keep clicking.

## Evidence

Proof directory: `.cursor/skills/verify-herdrm/artifacts/<run-id>/` (printed by `launch` as `evidence=...`). Cleanup must not delete it.

```sh
H=.cursor/skills/verify-herdrm/scripts/control-herdrm
$H snapshot --path .cursor/skills/verify-herdrm/artifacts/<run-id>/search/sheet.ax.txt
$H screenshot --path .cursor/skills/verify-herdrm/artifacts/<run-id>/search/sheet.png
```

Standards:

- Drive the real sidebar / menu / keyboard path. Do not poke `AppModel` from a debugger, write `devices.json` by hand, or call herdr RPC as a stand-in for a GUI proof.
- Capture the action **and** the resulting state (sheet title present, then gone after Cancel; Search field + `No matches` or a named result).
- A screenshot must show herdrm chrome (sidebar or the `New Agent` / Search sheet), not a cropped anonymous panel.
- The AX snapshot must contain the named handle you waited for.
- Prefer snapshots while a sheet or the empty placeholder is showing. A live SwiftTerm attach can make `entire contents` huge or slow; do not hang the harness there.
- Side effects: if a recipe creates an agent, space, device, or file, prove it from a second user-facing view (sidebar row, Search result, Files listing), then remove it through the UI.
- `herdr_socket: accepting` is not proof that the GUI connected — the footer dot or a connection-failure placeholder is.
- Language: this map is English. `launch` writes `app.language=en` and restores it on `cleanup`. If you attach to a pre-existing instance (don't), names may be zh-Hans.

Mocks: none. The production boundary is the herdr Unix socket / SSH tunnel. Do not stub it.

On a non-macOS agent, record `verified-unreachable` for every GUI feature with the attempted command (`control-herdrm launch` / `doctor`) and the unmet prerequisite. Do not invent a browser stand-in.

## Cleanup

```sh
.cursor/skills/verify-herdrm/scripts/control-herdrm cleanup
```

- Quits only the launched PID via `tell application id "dev.bybee.herdrm" to quit` (the app tears SSH tunnels down on that path). Falls back to `kill $PID` if it ignores the Apple Event — never `killall herdrm`.
- Restores `app.language` / `AppleLanguages`.
- Removes `/tmp/herdrm-verify/state.env` only.
- Leaves `.cursor/skills/verify-herdrm/artifacts/` untouched.
- Does **not** run `herdr server stop`, delete `devices.json`, or close herdr panes this run did not create.

After cleanup, confirm the proof files still exist at the paths printed during the drive.

## Helpers

`scripts/control-herdrm` is executable. Commands:

| Command | Purpose |
| --- | --- |
| `launch [--rebuild] [--app PATH]` | build if needed, refuse a pre-existing process, open Debug, wait for AX window |
| `doctor [--json]` | read-only health; exit 1 unless `worth-driving` |
| `click --name NAME [--role button]` | click an AX element in window 1 |
| `menu --path File>New Agent` | File / Terminal menu items |
| `key --chord cmd+k` | keystroke; `escape`, `return`, arrows supported |
| `type --text …` | type into the focused field |
| `wait --name NAME [--timeout 8]` | poll AX for a name |
| `snapshot --path FILE` | AX role+name dump of window 1 |
| `screenshot --path FILE` | window screenshot via `screencapture -l` |
| `reset-ui` | Escape × 3 |
| `quit` / `cleanup` | quit our PID; cleanup also drops state, keeps evidence |
| `selftest` | harness sanity (doctor JSON + argument errors); does not launch the app |

A command you have to reverse-engineer is not a helper — if you add one, put the invocation in this table.
