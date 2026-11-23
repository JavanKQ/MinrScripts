# MinrScripts

MSC 2.0 scripts for a puzzle map on zero.minr.org (Minecraft). See [References.md](References.md) for doc links.

## Working rules

- **The docs are the authority:** https://msc-documentation.readthedocs.io/en/latest/. If the VS Code MSC extension (lightwood13.msc) disagrees, trust the docs. The extension's type list is out of date; for example, it flags `Block.getBlockDataValue` as unknown, but that method works. Namespace variables also show as "not defined" because the extension can't see server-side namespaces.
- **Testing:** the user tests on the Minr **test server**, which has a single world. Don't hardcode world names; use `block.getWorld()` when a world string is required.
- **Admins import scripts on the main map**, not the user. Every script needs the standard `#` header block (see any `Ocean_Puzzle_*.msc`): title with (n of N), script type, `Bind to: [FILL IN]`, `Map/area`, import command, what it does, placement notes, setup commands, coordinates used inside the script, and related scripts. Hand-off should need as little back-and-forth with admins as possible.
- **Import:** `/s i i <paste URL>` (interact) or `/script import walk <paste URL>`, then click the block. Pastes go on paste.minr.org.
- **Walk scripts** fire when the player's feet enter the space *above* the bound block. They can be bound to air: place a temporary block, import, click it, then break it.
- **Git:** commit work for the current map straight to `main`. Create a branch only when starting work on a different map.
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
- **Teams (any size):** each player right-clicks the Team Conduit and types the same team word. The first player creates the word; it accepts new members for 2 minutes, then locks. Every join gives the whole team a new shared song and sets them unsolved, so a finished player can't carry someone through. A wrong submit costs every online teammate 1 heart, so teams don't get extra guesses. A teammate's death re-rolls the whole team's song. A correct submit marks the whole team solved. Joining another team, or the Reset script, removes a player from their team. Each player stores a team ID (`word@createdSeconds`); updates only go to members whose current team ID matches, so stale rosters are harmless.
- **Out-of-character notes** use grey `&7&o[Note]`, never the Oracle's format. The co-op note is at the end of the Room 1 instructions.

Variables in `puzzle1`:
- **Relative (per player):** `answer` (String), `solved` (Boolean), `submit_ready_at` (Long, 10s submit cooldown), `oracle_ready_at` (Long, 45s instruction cooldown shared by all instruction scripts), `team` (String team ID), `team_members` (String, comma-joined UUIDs).
- **Global:** `team_registry` (String, `word:createdSeconds:uuid,uuid;...`, only used during the 2-minute join window).

| File | Type | Purpose |
|---|---|---|
| Ocean_Puzzle_Noteblocks.msc | interact | Submit (1 of 5) |
| Ocean_Puzzle_Entrance.msc | walk | New answer on entry (2 of 5) |
| Ocean_Puzzle_Exit.msc | walk | Close stairway (3 of 5) |
| Ocean_Puzzle_Reset.msc | walk | Clear progress (4 of 5) |
| Ocean_Puzzle_NoteTune.msc | interact | "The note shifts to its Nth position." on every puzzle note block (5 of 6) |
| Ocean_Puzzle_TeamConduit.msc | interact | Team word linking on the conduit (6 of 6) |
| Ocean_Puzzle_Instructions_Room1/3/4.msc | interact | Oracle instructions |

## Status (as of 2026-11-23)

- **Tested and working** under the old `oceanpuzzle` namespace: submit check, hearts, entrance re-roll, stairway open/close.
- **Working under `puzzle1`:** Submit and Entrance, after re-importing the Entrance (an old `oceanpuzzle` copy was still bound). NoteTune works; `@delay 1t` was rejected, so it uses `@delay 1`. Interact scripts also fire on left-click (hit), so NoteTune compares the note before and after the delay and stays silent if it didn't change.
- **NOT yet tested:** the team system (Team Conduit plus the team parts of Entrance, Submit and Reset), the new Room 1 instruction lines, and Reset. Untested MSC features it relies on: `@prompt`, `Player(uuid)`, writing another player's relative variable (`answer[p] = ...`), `p.isOnline()`, `p.sendMessage(...)` (unknown whether `&` color codes work there), `String.matches`, and the "{{...}}" interpolation trick to turn a Long into an Int. The three team variables must be defined on the test server (see the Submit header).
- **Debug:** the Submit script has `debug = true`, which prints the answer in chat. Turn it off before handing off to admins.

## Next up

1. Room 2 symbol scripts: one interact script per symbol, each playing its note from `answer` via `@bypass /playsound` with the matching pitch.
2. Room 4 instrument check.

## Open questions

- Which instrument (block under the note blocks) Rooms 1 and 4 use. The symbol sounds must match it.
- Whether natural regeneration is off in the puzzle area. If it's on, hearts regenerate during the cooldown and "10 lives" becomes weaker.
- The stairway is shared blocks, so while it's open, other players could slip through. This is currently accepted.
