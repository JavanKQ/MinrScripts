# MinrScripts

MSC 2.0 scripts for a puzzle map on zero.minr.org (Minecraft). See [References.md](References.md) for doc links.

## Working rules

- **The docs are the authority:** https://msc-documentation.readthedocs.io/en/latest/. If the VS Code MSC extension (lightwood13.msc) disagrees, trust the docs. The extension's type list is out of date; for example, it flags `Block.getBlockDataValue` as unknown, but that method works. Namespace variables also show as "not defined" because the extension can't see server-side namespaces.
- **Testing:** the user tests on the Minr **test server**, which has a single world. Don't hardcode world names; use `block.getWorld()` when a world string is required.
- **Admins import scripts on the main map**, not the user. Every script needs the standard `#` header block (see any `Ocean_Puzzle_*.msc`): title with (n of N), script type, `Bind to: [FILL IN]`, `Map/area`, import command, what it does, placement notes, setup commands, coordinates used inside the script, and related scripts. Hand-off should need as little back-and-forth with admins as possible.
- **Import:** `/s i i <paste URL>` (interact) or `/script import walk <paste URL>`, then click the block. Pastes go on paste.minr.org.
- **Walk scripts** fire when the player's feet enter the space *above* the bound block. They can be bound to air: place a temporary block, import, click it, then break it.
- **Git:** commit work for the current map straight to `main`. Create a branch only when starting work on a different map.
- **Colors in `sendMessage`:** `p.sendMessage(...)` (messages to *other* players) does NOT convert `&` color codes; teammates saw plain white text. Use `§` codes there (`§3Oracle: §b...`, `§7§o[Note]`). `@player` lines do convert `&` codes, so keep `&` there.
- **Player-facing text:** ancient ocean temple theme. Speaker format is `&3Oracle: &b<message>` (dark aqua name, aqua message). Tuning feedback is white italics (`&f&o`).

## MSC syntax confirmed working on the test server

`Block[...]` list literals, `Block(x, y, z, world)`, `block.getBlockDataValue("note")` (returns the note as a String, 0-24), `list::range(a, b)`, `list[i]`, `String == String`, `@for ... @done`, `@if/@elseif/@else/@fi`, `@using`, relative namespace variables, `player.setHealth(...)`, `@bypass /fill ...`, `#` comments.

## Ocean Puzzle (namespace `puzzle1`)

- **Room 1:** 10 note blocks. Players tune them and press a submit block.
- **Room 2:** 10 clickable symbols. Each plays one note from that player's answer.
- **Room 3:** five symbol-arithmetic grids (no puzzle scripts). Every gap between two cells has its own hidden operator (+, -, x, /; 12 in all), the same in every grid. Lines are worked strictly left to right / top to bottom, division is always whole, nothing is negative. Grid 1 deliberately leaves some operators open until Grid 2. Full design, answer and order: [Ocean_Puzzle_Room3_Grids.md](Ocean_Puzzle_Room3_Grids.md). Room 4 order, lowest first: Symbols 7, 9, 4, 6, 10, 5, 1, 2, 8, 3. `tools/room3_grids.py` generates and checks grid sets (`py tools/room3_grids.py 131` reproduces the chosen one).
- **Symbols are custom player heads.** Only their skins differ. Designs use letters A-J and scripts use Symbol 1-10 (A = Symbol 1 ... J = Symbol 10). The map builder matches skins to numbers physically, and the same skin must be Symbol N in Rooms 2, 3 and 4. Explain this in headers for admins.
- **Room 4:** "ancient instrument." Players tune 10 note blocks (symbols in a different order) to each symbol's Room 2 note, then play the melody quickly in order of value, lowest first. The per-player `answer` therefore has to last from Room 1 through Room 4.

Flow:
- **Entrance:** the player drops through a one-way drop and gets a new random answer: 10 distinct notes from 0-24, stored as a comma-joined String. This is skipped if they've already solved it.
- **Wrong submit:** costs 2 hearts (the 5th wrong submit kills). The Oracle says how many notes are wrong but never which. Only the particles show that: green sparkles over right note blocks and smoke over wrong ones, shown only to the player and teammates. The user wants players to learn to watch the particles. Changed on 2026-11-23 from "1 heart, count of wrong notes only" to reward a good ear over bookkeeping. With 5 tries, a player whose ear gets each block within 2 notes can always solve it; blind guessing has roughly a 1 in 10 million chance. Never add higher/lower hints: that would allow binary search in 5 tries. Dying respawns the player at the checkpoint, they drop back through, and they get a new answer. This stops brute-forcing, because what a player learned by guessing is lost on death.
- **Solve:** the stairway ceiling and wall are filled with air. The Exit walk trigger fills them back with prismarine bricks.
- **Reset:** clears `answer`/`solved` partway down the one-way drop out of the maze. Leaving and rejoining the map restarts the puzzle; dying at the checkpoint does not.
- **Teams (any size):** each player right-clicks the Team Conduit and types the same team word. The first player creates the word; it accepts new members for 2 minutes, then locks. At the end of the window, all members get the team roster, or, if nobody joined, the team is deleted and the creator is told. Every join gives the whole team a new shared song and sets them unsolved, so a finished player can't carry someone through. A wrong submit costs every online teammate 2 hearts (they get a chat line naming who submitted, plus the particles), so teams don't get extra guesses. A teammate's death re-rolls the whole team's song. A correct submit marks the whole team solved. Joining another team, or the Reset script, removes a player from their team. Each player stores a team ID (`word@createdSeconds`); updates only go to members whose current team ID matches, so stale rosters are harmless.
- **Leaving a team (follows Minr's co-op rules, 2026-11-24):** a player is off the team, with no credit, if they're offline during any team event (new song on death, hearts on a wrong submit, a solve), rejoin the map (Reset), join another map, or reach the checkpoint after Room 4. Offline players' variables can't safely be written, so at each team event a "team check" (copied into Entrance and Submit) rebuilds the team from the online, same-ID members. If anyone is missing, the remaining members get a new team ID (`<old id>~<seconds>`), a new roster and a grey `[Note]` saying who left. The missing player keeps the old ID, so they're effectively solo when they return. If nobody is left, the player's team is cleared. Regions aren't needed: players can't leave the puzzle area except by finishing Room 4 or leaving the map. Leaving by Reset or by switching teams at the conduit notifies and regroups the remaining online teammates immediately; going offline is only noticed at the next team event. Room 4's scripts need the same team check, and **completing Room 4 must disband the team entirely** (clear `team` and `team_members` for every member) so nobody gets stray team messages afterwards.
- **Dialogue tone:** Oracle instructions should be cryptic but complete. Every rule is hinted through metaphor (note blocks = "voices", symbols = "signs", particles = "glimmer/smoulder"), not stated plainly. The user found plain wording "too straightforward." The Room 1 instructions are the reference example.
- **Dialogue pacing:** multi-line Oracle dialogue uses `@delay 4s` between lines. The user found 3s too fast.
- **Out-of-character notes** use grey `&7&o[Note]`, never the Oracle's format. The co-op note is at the end of the Room 1 instructions.

Variables in `puzzle1`:
- **Relative (per player):** `answer` (String), `solved` (Boolean), `submit_ready_at` (Long, 10s submit cooldown), `chime_ready_at` (Long, 2s cooldown shared by the 10 Room 2 symbols; clicks during it are silent), `oracle_ready_at` (Long, instruction cooldown shared by all instruction scripts: 60s after Room 1, 45s after Rooms 3 and 4; keep each cooldown longer than its speech), `team` (String team ID), `team_members` (String, comma-joined UUIDs), `solved3` (Boolean, Room 3 altar solved), `altar_seq` (String, comma-joined symbol numbers clicked so far), `altar_last_at` (Long, time of the last altar click), `altar_ready_at` (Long, 30s altar cooldown after a wrong order).
- **Global:** `team_registry` (String, `word:createdSeconds:uuid,uuid;...`, only used during the 2-minute join window), `door3_close_at` / `door4_close_at` (Long, so a door closes 5s after the *last* click).

Room 3 altar and doors (designed 2026-11-24):
- **Doors (Rooms 3 and 4):** each door has an outside head and an inside head. A click fills the door with air for 5s. The inside heads open for anyone, so nobody gets trapped. The Room 3 outside head needs `solved`; the Room 4 outside head needs `solved` and `solved3`. A player who sneaks into Room 3 unsolved can solve it out of order, which is accepted, but they still need Room 1 for Room 4.
- **Altar:** 10 symbol heads inside Room 3. Players click them in value order, lowest first. Every click plays the same amethyst chime and shows `(n/10)`; there's deliberately no rising pitch, which could be confused with Room 4. There's no right/wrong feedback until the 10th click. More than 15s between clicks, or clicking the same head twice, clears the offering with a message. A wrong order costs no hearts and has a 30s cooldown. The right order sets `solved3` for the player and their teammates (with the team check). Dying doesn't clear `solved3`, because the answer never changes; Reset and joining a team do.

| File | Type | Purpose |
|---|---|---|
| Ocean_Puzzle_Noteblocks.msc | interact | Submit (1 of 9) |
| Ocean_Puzzle_Entrance.msc | walk | New answer on entry (2 of 9) |
| Ocean_Puzzle_Exit.msc | walk | Close stairway (3 of 9) |
| Ocean_Puzzle_Reset.msc | walk | Clear progress (4 of 9) |
| Ocean_Puzzle_NoteTune.msc | interact | "The note shifts to its Nth position." on every puzzle note block (5 of 9) |
| Ocean_Puzzle_TeamConduit.msc | interact | Team word linking on the conduit (6 of 9) |
| Ocean_Puzzle_Door_Room3/4_Outside/Inside.msc | interact | Door heads (8 of 9). The 4 files are identical except for the settings block at the top (`need`, `door`, `corners`, `material`). `corners` is empty until coordinates are given, and the script refuses to run until it's set. |
| Ocean_Puzzle_Altar_01..10.msc | interact | Room 3 altar signs (9 of 9). Identical except `symbol` (1-10). Generated by a scratch script; edit all 10 the same way. |
| Ocean_Puzzle_Symbol_01..10.msc | interact | Room 2 symbols (7 of 9). Each plays its slot of `answer` as a chime, heard only by the clicking player. The 10 files are identical except `slot` (0-9). Symbol N pairs with Room 1 note block N. |
| Ocean_Puzzle_Instructions_Room1/3/4.msc | interact | Oracle instructions |

## Status (as of 2026-11-24)

- **Tested and working** under the old `oceanpuzzle` namespace: submit check, hearts, entrance re-roll, stairway open/close.
- **Working under `puzzle1`:** Submit and Entrance, after re-importing the Entrance (an old `oceanpuzzle` copy was still bound). NoteTune works; `@delay 1t` was rejected, so it uses `@delay 1`. Interact scripts also fire on left-click (hit), so NoteTune compares the note before and after the delay and stays silent if it didn't change.
- **Tested solo and working:** all of Rooms 1-2's flow (instructions, NoteTune, entrance, submit, cooldown, hearts, death and new song, solve, stairway, exit, reset) and the Team Conduit with a team of one: word validation, prompt timeout, creating a word, "already bound", team-of-one submits and deaths, and the "bond dissolves" expiry. So `@prompt`, `String.matches`, `Player(uuid)` and the "{{...}}" Long-to-Int trick work.
- **`@prompt` timeout message:** it showed in yellow, ignoring `&` codes. It now uses `§` codes instead; whether that works is untested. If it doesn't, drop the colors from that one line.
- **Co-op tested 2026-11-24 (2 players), after re-importing everything:** a standard 2-player playthrough of Rooms 1-2 works. The team solved together and both were marked solved, and teammate messages now show in color (`§` codes in `sendMessage` confirmed).
- **NOT yet tested (edge cases, needs a second player):** the team check when someone goes offline or switches teams before a team event (new team ID, "no longer on your team" note), e.g. a teammate logging off and the rest completing the puzzle. The user considers this low priority.
- **Room 3 playtest (2026-11-24):** a second player tried the grids for about 10 minutes without getting A. That is the intended difficulty; keep it.
- **Room 2 symbols and per-block particle feedback: tested solo and working (2026-11-23),** so `@bypass /playsound` and `/particle ... force <player>` work, as does `{{1573 - i}}.5` inside a command.
- **Debug:** the Submit script has `debug = true`, which prints the answer in chat. Turn it off before handing off to admins.

## Pending re-import

Everything was re-imported on 2026-11-24. Keep this list up to date: add every script changed since then, and clear the list only when the user confirms they've re-imported. When they ask what needs importing, give this whole list, plus any one-time setup commands.

| Script | Bind to | What changed |
|---|---|---|
| `Ocean_Puzzle_Symbol_01..10.msc` (all 10) | each Room 2 symbol head | 2s chime cooldown shared by all symbols; white-italic line "The chime washes over your soul like a tide." after each chime |
| `Ocean_Puzzle_Reset.msc` | Reset block | Also clears `solved3` and `altar_seq` |
| `Ocean_Puzzle_TeamConduit.msc` | conduit | Joining a team also resets `solved3` for the whole team |
| `Ocean_Puzzle_Door_*.msc` (4, NEW) | door heads (2 per door) | New. Needs the door `corners` (and `material`) filled in before importing |
| `Ocean_Puzzle_Altar_01..10.msc` (10, NEW) | Room 3 altar heads | New. Altar head N must wear Symbol N's skin |

**One-time setup commands (run before importing the above):**
```
/variable define puzzle1 relative Long chime_ready_at = 0L
/variable define puzzle1 relative Boolean solved3 = false
/variable define puzzle1 relative String altar_seq = ""
/variable define puzzle1 relative Long altar_last_at = 0L
/variable define puzzle1 relative Long altar_ready_at = 0L
/variable define puzzle1 Long door3_close_at = 0L
/variable define puzzle1 Long door4_close_at = 0L
```

## Next up

1. **Test coordinates (waiting on the user):** the Room 3 and Room 4 door corners and block type, plus the 4 door heads and the 10 altar heads. Fill in the door `corners` settings, then test the doors and the altar.
2. Room 4 instrument check script (see the grids file for the order). It needs the team check and must disband the team on completion.
3. Rewrite the Room 4 instructions in the cryptic style of Room 1 (4s per line). Room 3's are done.
4. Later: co-op edge-case tests (see "NOT yet tested" above).
5. **Before admin handoff, once every script is done:** the user prepares the main map and gives the real coordinates. Put them in every header (`Bind to`, `Map/area`, coordinates used inside the script) and in the scripts themselves: the Submit note blocks, stairway and particles; the Entrance blocks; the door `corners`; and the Room 4 blocks. Set `debug = false` in Submit.

## Decisions

- **Health (confirmed 2026-11-23):** natural regeneration is off, saturation is fixed and damage is disabled in the puzzle area, so wrong submits are the only way to lose health or die.

- **Instrument (2026-11-23):** packed ice under the Room 1 and Room 4 note blocks, which gives the chime sound (`minecraft:block.note_block.chime`, F#5-F#7), chosen for its watery, magical feel. The symbols play the same sound at pitch 2^((note-12)/12).

## Open questions

- The stairway is shared blocks, so while it's open, other players could slip through. This is currently accepted.
