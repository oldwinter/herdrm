# Files

Files is a two-pane workspace that browses Local and another configured device and copies regular files in either direction. The default verification opens it, confirms the Local listing, and leaves without transferring.

## Sub-features

- `files-open` replaces the terminal pane with the Files workspace from the sidebar Files row.
- `files-titlebar` shows Files in the titlebar instead of No terminal selected.
- `files-panes` shows a Local pane and a target pane titled with the other device name (or Local when no SSH device exists).
- `files-listing` lists Name / Size / Modified, or Empty Folder with This folder contains no visible items.
- `files-path` exposes Path, Parent folder, Home folder, Refresh, and Show hidden files / Hide hidden files.
- `files-leave` returns to the terminal placeholder or the previously selected pane by choosing an agent, terminal, or space row.
- `files-transfer` (mutation) copies a selected regular file; conflict UI is File Already Exists with Replace, Keep Both, Cancel.

## How to get to it (user POV)

- Choose Files in the sidebar.
- Leave by selecting a Space, Agent, or Terminal row (Files is not a herdr pane; it is an in-app mode).

## Driving it with control-herdrm

Preconditions:

- `control-herdrm doctor` reports `worth-driving`.
- Prefer `herdr_socket: accepting` so the Local pane can list the home directory. If the socket is down, Local still lists via the local file service; SSH target panes may error.
- Do not click the transfer arrows unless a mutation recipe names a disposable file.

- **Open Files.** Choose Files. Run `control-herdrm click --name "Files"`. `wait --name "Files"` succeeds in the titlebar sense: a snapshot contains `Files`, `Local`, `Name`, `Size`, and `Modified` (or `Empty Folder`).
- **Device bar.** The top bar reads `Local`, `Transfer with`, and the target device name. With only the built-in device, both sides can be `Local`.
- **Local listing.** The Local pane footer shows `<n> items` or an error string. `Empty Folder` / `This folder contains no visible items.` is valid for an empty visible directory, not a load failure. A load failure is a warning string in the pane footer, not the empty-folder placeholder.
- **Path controls.** Help names `Parent folder`, `Home folder`, `Refresh`, and either `Show hidden files` or `Hide hidden files` are in the tree or tooltip-backed icon buttons. The path field's name is `Path`.
- **Screenshot.** Run `control-herdrm screenshot --path "$EVIDENCE/files/workspace.png"` and `control-herdrm snapshot --path "$EVIDENCE/files/workspace.ax.txt"`. The screenshot shows two columns and the Files titlebar. The snapshot contains `Local` and `Files`.
- **Leave without transfer.** Choose All Spaces. Run `control-herdrm click --name "All Spaces"`. The titlebar returns to `No terminal selected` (or the previously attached title). No `File Already Exists` dialog appeared.
- **Transfer (only when explicitly proving a copy).** Select a regular file on one side, then the arrow whose help is `Copy the selected local file to <device>` (right) or `Copy the selected file from <device> to Local` (left). If the name exists, `File Already Exists` offers `Replace`, `Keep Both`, `Cancel`. Default of that dialog in a verification run is `Cancel`. Progress text is `Uploading <name>` or `Downloading <name>` with a `Cancel` button.

## Gotchas

- Files stays mounted after the first open (`hasOpenedFileManager`); leaving only hides it. A stale transfer bar should not linger after Cancel.
- Transfer arrows are icon-only. Drive them by help/AX name, not by assuming left/right coordinates. They stay disabled until a **regular file** (not a directory) is selected.
- Packages (`.app`) are not regular files for transfer. Symbolic links are not the default copy target.
- Choosing a folder in the listing navigates; choosing a file selects it. Double-purpose rows: wait for the path field or footer `selected name` to change before asserting.
- `Choose folder` on the Local pane opens an NSOpenPanel. That panel is a system dialog — cancel it with Escape; do not screenshot-assert it as herdrm chrome.
- Copying to a real SSH device writes bytes on that host. Use a disposable file and a disposable destination, or skip transfer and report `verified-unreachable` if no safe target exists.
- If the titlebar still says `Files` after clicking All Spaces, the click missed (the Files button and the titlebar both say `Files`). Snapshot to see whether `Name` / `Size` / `Modified` remain.
