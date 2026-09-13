# Search

Search (⌘K) is a command-palette sheet over agents, terminals, and spaces on every device. It ranks agents by urgency (needs input, unread, working, then the rest), filters as the user types, and opening a result attaches that pane.

## Sub-features

- `search-sidebar` opens Search from the sidebar row.
- `search-key` opens Search with ⌘K.
- `search-field` focuses Search agents, terminals, and spaces….
- `search-empty` shows No matches for a query that hits nothing.
- `search-results` lists matching agent titles, terminal titles, and space labels when they exist.
- `search-blocked` shows needs input on a blocked agent row.
- `search-dismiss` closes the sheet with Escape without attaching.
- `search-open-result` (mutation) attaches the highlighted result; not part of the default recipe.

## How to get to it (user POV)

- Choose Search in the sidebar.
- Press ⌘K while herdrm is focused.

## Driving it with control-herdrm

Preconditions:

- `control-herdrm doctor` reports `worth-driving`.
- No other sheet is open.
- Do not press return on a result unless a mutation recipe is explicitly running.

- **Sidebar entry.** Choose Search. Run `control-herdrm click --name "Search"`. `wait --name "Search agents, terminals, and spaces…"` succeeds.
- **Dismiss.** Close with Escape. Run `control-herdrm key --chord escape`. The search field is gone from a snapshot.
- **Keyboard entry.** Open with ⌘K. Run `control-herdrm key --chord cmd+k`. `wait --name "Search agents, terminals, and spaces…"` succeeds. Footer hints `↑↓` / `navigate`, `↩` / `open`, `esc` / `cancel` are visible in the screenshot.
- **Empty query.** With the field blank, the list is every agent (urgency-ranked), then terminals, then spaces — or `No matches` if this session has none. Record which. An empty catalog plus no spaces yields `No matches` immediately.
- **Nonsense query.** Type a string that should not match. Run `control-herdrm type --text "zzzx-herdrm-no-such-item"`. `wait --name "No matches"` succeeds.
- **Clear by dismissing.** Run `control-herdrm key --chord escape`. Reopen with `control-herdrm key --chord cmd+k`. The field is empty again (the sheet is new each open) and `No matches` from the previous query is gone unless the session itself has no rows.
- **Proof.** While Search is open on the nonsense query, run `control-herdrm snapshot --path "$EVIDENCE/search/empty.ax.txt"` and `control-herdrm screenshot --path "$EVIDENCE/search/empty.png"`. The snapshot contains the search field name and `No matches`. The screenshot shows the Search sheet on top of herdrm, not a generic dialog. Then Escape so nothing attaches.

## Gotchas

- Opening a result (return or click) attaches that agent/terminal/space's pane and `--takeover`s any other client. The default recipe never confirms a result.
- Rank order is not sidebar order. Sidebar follows herdr tab order; ⌘K sorts blocked → unread done → working → done → idle → unknown.
- Matches include title, herdr name, kind, tab label, stripped terminal title, device name, space name, and (for terminals) cwd. A "unique" query can still hit a cwd path.
- The sheet is 440pt wide. `No matches` is the exact empty string — not `No matching notes` or similar.
- ⌘K is also the global macOS search chord in some contexts; herdrm must be frontmost (`control-herdrm activate` happens inside `key` / `click`).
- If a New Agent sheet is already open, ⌘K may not show Search. `reset-ui` first.
