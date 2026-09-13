# herdrm verification map

This directory is the maintained source for verifying the user-facing behavior of the herdrm macOS console. Read the index before driving the app, then use the matching feature file as the recipe.

## Baseline preconditions

- Host is macOS 14+. Linux cloud agents cannot launch the app; report every GUI feature `verified-unreachable` with that prerequisite rather than substituting tests or a browser.
- Launch with `.cursor/skills/verify-herdrm/scripts/control-herdrm launch` so English Accessibility names match this map.
- `control-herdrm doctor` reports `verdict: worth-driving` and `owned: yes`.
- Never drive an instance this run did not start. A second herdrm shares `~/Library/Application Support/HerdrM/devices.json` and `~/.config/herdr/herdr.sock`, and attach uses `--takeover`.
- Default recipes open UI and cancel. Do not start an agent, create a herdr pane, add a device, or attach a live PTY unless the feature file's mutation steps say so.
- `herdr_socket: accepting` plus a non-failed footer/placeholder is required for recipes that list agents or attach. Sheet/Search open-and-cancel does not.

## Driving conventions

- Start every recipe from the baseline window (sidebar visible, no sheet). Run `control-herdrm reset-ui` if a previous step left Search or a sheet open.
- Prefer Accessibility names and menu/keyboard chords from `SKILL.md` over coordinates.
- Treat every command as literal. Keep quoted names and flags unchanged.
- Run every GUI action through `control-herdrm`.
- Restore any mutation through the UI (sidebar Close confirm, Remove device, Files conflict Cancel). Do not remove proof artifacts.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final screen.
- UI proof includes an AX snapshot and a screenshot that shows herdrm chrome (sidebar and/or the sheet).
- Mutation proof includes a second user-facing read (sidebar row, Search result, Files listing).
- Record the feature ID and entry point used with every artifact.
- Report an unreachable path with the attempted command and the unmet precondition.
- Do not report a skipped entry point as verified through a different path.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible behavior. It then uses exactly four H2 sections in this order.

1. `Sub-features` lists short IDs with one line for each behavior.
2. `How to get to it (user POV)` lists every user entry point.
3. `Driving it with control-herdrm` starts with `Preconditions:` and uses labeled bullets that pair each user action with an exact command and observable result.
4. `Gotchas` lists traps that can waste or invalidate a verification run.

Keep implementation details out of the map. Name only user paths, stable handles, required state, commands, and observable proof.

## Features

- [Sidebar and devices](./sidebar-and-devices.md) covers the Spaces/Agents/Terminals sidebar, All Spaces, the device footer, and Add Device open/cancel.
- [New Agent](./new-agent.md) covers opening the New Agent sheet from the sidebar, File menu, and ⌘N, then cancelling without starting a CLI.
- [Search](./search.md) covers ⌘K / sidebar Search across agents, terminals, and spaces, including empty results and Escape.
- [Terminal](./terminal.md) covers the empty placeholder, attaching a pane, Reconnect, and the Terminal split menu.
- [Files](./files.md) covers the two-pane Files workspace, Local listing, and leaving without a transfer.
