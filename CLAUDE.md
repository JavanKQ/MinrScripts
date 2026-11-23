# MinrScripts

MSC 2.0 scripts for a puzzle map on zero.minr.org (Minecraft). See [References.md](References.md) for doc links.

## Working rules

- **The docs are the authority:** https://msc-documentation.readthedocs.io/en/latest/. If the VS Code MSC extension (lightwood13.msc) disagrees, trust the docs. The extension's type list is out of date; for example, it flags `Block.getBlockDataValue` as unknown, but that method works. Namespace variables also show as "not defined" because the extension can't see server-side namespaces.
- **Testing:** the user tests on the Minr **test server**, which has a single world. Don't hardcode world names; use `block.getWorld()` when a world string is required.
- **Admins import scripts on the main map**, not the user. Every script needs the standard `#` header block (see any `Ocean_Puzzle_*.msc`): title with (n of N), script type, `Bind to: [FILL IN]`, `Map/area`, import command, what it does, placement notes, setup commands, coordinates used inside the script, and related scripts. Hand-off should need as little back-and-forth with admins as possible.
- **Import:** `/s i i <paste URL>` (interact) or `/script import walk <paste URL>`, then click the block. Pastes go on paste.minr.org.
- **Walk scripts** fire when the player's feet enter the space *above* the bound block. They can be bound to air: place a temporary block, import, click it, then break it.
- **Player-facing text:** ancient ocean temple theme. Speaker format is `&3Oracle: &b<message>` (dark aqua name, aqua message). Tuning feedback is white italics (`&f&o`).

## MSC syntax confirmed working on the test server

`Block[...]` list literals, `Block(x, y, z, world)`, `block.getBlockDataValue("note")` (returns the note as a String, 0-24), `list::range(a, b)`, `list[i]`, `String == String`, `@for ... @done`, `@if/@elseif/@else/@fi`, `@using`, relative namespace variables, `player.setHealth(...)`, `@bypass /fill ...`, `#` comments.

## Ocean Puzzle (namespace `puzzle1`)

- **Room 1:** 10 note blocks. Players tune them and press a submit block.
- **Room 2:** 10 clickable symbols. Each plays one note from that player's answer.
- **Room 3:** grid puzzle to work out each symbol's hidden number value.
- **Room 4:** "ancient instrument." Players tune 10 note blocks (symbols in a different order) to each symbol's Room 2 note, then play the melody quickly in order of value, lowest first. The per-player `answer` therefore has to last from Room 1 through Room 4.

Flow:
- **Entrance:** the player drops through a one-way drop and gets a new random answer: 10 distinct notes from 0-24, stored as a comma-joined String. This is skipped if they've already solved it.
- **Wrong submit:** costs 1 heart (10 lives). Dying respawns the player at the checkpoint, they drop back through, and they get a new answer. This stops brute-forcing, because what a player learned by guessing is lost on death.
- **Solve:** the stairway ceiling and wall are filled with air. The Exit walk trigger fills them back with prismarine bricks.
- **Reset:** clears `answer`/`solved` partway down the one-way drop out of the maze. Leaving and rejoining the map restarts the puzzle; dying at the checkpoint does not.
- **Multiplayer:** handled by Minr rules. Co-op players are told by in-world signs that their answers differ.

Relative variables in `puzzle1`: `answer` (String), `solved` (Boolean), `submit_ready_at` (Long, 10s submit cooldown), `oracle_ready_at` (Long, 45s instruction cooldown shared by all instruction scripts).

| File | Type | Purpose |
|---|---|---|
| Ocean_Puzzle_Noteblocks.msc | interact | Submit (1 of 5) |
| Ocean_Puzzle_Entrance.msc | walk | New answer on entry (2 of 5) |
| Ocean_Puzzle_Exit.msc | walk | Close stairway (3 of 5) |
| Ocean_Puzzle_Reset.msc | walk | Clear progress (4 of 5) |
| Ocean_Puzzle_NoteTune.msc | interact | "The note shifts to its Nth position." on every puzzle note block (5 of 5) |
| Ocean_Puzzle_Instructions_Room1/3/4.msc | interact | Oracle instructions |

## Status (as of 2026-11-23)

- **Tested and working** under the old `oceanpuzzle` namespace: submit check, hearts, entrance re-roll, stairway open/close.
- **NOT yet imported or tested:** the most recent changes, which are the rename to `puzzle1`, the 10s submit cooldown, NoteTune, Reset (being tested as interact for now), and the updated instruction scripts. The `puzzle1` namespace and variables have not been created on the test server yet. Run the setup commands from the Submit script header, then re-import everything.
- **Debug:** the Submit script has `debug = true`, which prints the answer in chat. Turn it off before handing off to admins.

## Next up

1. Room 2 symbol scripts: one interact script per symbol, each playing its note from `answer` via `@bypass /playsound` with the matching pitch.
2. Room 4 instrument check.

## Open questions

- Which instrument (block under the note blocks) Rooms 1 and 4 use. The symbol sounds must match it.
- Whether natural regeneration is off in the puzzle area. If it's on, hearts regenerate during the cooldown and "10 lives" becomes weaker.
- The stairway is shared blocks, so while it's open, other players could slip through. This is currently accepted.
