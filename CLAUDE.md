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
- **Teams (any size):** each player right-clicks the Team Conduit and types the same team word. The first player creates the word; it accepts new members for 2 minutes, then locks. At the end of the window, all members get the team roster, or, if nobody joined, the team is deleted and the creator is told. Every join gives the whole team a new shared song and sets them unsolved, so a finished player can't carry someone through. A player who has already solved Room 1 can't use the conduit at all (2026-11-24): "already bound and sung" if they're on a team, "cannot be bound anew" if they're solo. A wrong submit costs every online teammate 2 hearts (they get a chat line naming who submitted, plus the particles), so teams don't get extra guesses. A teammate's death re-rolls the whole team's song. A correct submit marks the whole team solved. Joining another team, or the Reset script, removes a player from their team. Each player stores a team ID (`word@createdSeconds`); updates only go to members whose current team ID matches, so stale rosters are harmless.
- **Leaving a team (follows Minr's co-op rules, 2026-11-24):** a player is off the team, with no credit, if they're offline during any team event (new song on death, hearts on a wrong submit, a solve), rejoin the map (Reset), join another map, or finish the puzzle (the Finish script after the Room 4 parkour). Offline players' variables can't safely be written, so at each team event a "team check" (copied into Entrance and Submit) rebuilds the team from the online, same-ID members. If anyone is missing, the remaining members get a new team ID (`<old id>~<seconds>`), a new roster and a grey `[Note]` saying who left. The missing player keeps the old ID, so they're effectively solo when they return. If nobody is left, the player's team is cleared. Regions aren't needed: players can't leave the puzzle area except by finishing the Room 4 parkour or leaving the map. Leaving by Reset or by switching teams at the conduit notifies and regroups the remaining online teammates immediately; going offline is only noticed at the next team event. **Finishing (walking over the Finish script after the Room 4 parkour) disbands the team entirely** (clears `team` and `team_members` for every online member on the same ID) so nobody gets stray team messages afterwards.
- **Dialogue tone:** Oracle instructions should be cryptic but complete. Every rule is hinted through metaphor (note blocks = "voices", symbols = "signs", particles = "glimmer/smoulder"), not stated plainly. The user found plain wording "too straightforward." The Room 1 instructions are the reference example.
- **Dialogue pacing:** multi-line Oracle dialogue uses `@delay 4s` between lines. The user found 3s too fast.
- **Out-of-character notes** use grey `&7&o[Note]`, never the Oracle's format. The co-op note is at the end of the Room 1 instructions.

Variables in `puzzle1`:
- **Relative (per player):** `answer` (String), `solved` (Boolean), `submit_ready_at` (Long, 10s submit cooldown), `chime_ready_at` (Long, 2s cooldown shared by the 10 Room 2 symbols; clicks during it are silent), `oracle_ready_at` (Long, instruction cooldown shared by all instruction scripts: 60s after Room 1, 45s after Rooms 3 and 4; keep each cooldown longer than its speech), `team` (String team ID), `team_members` (String, comma-joined UUIDs), `solved3` (Boolean, Room 3 altar solved), `altar_seq` (String, comma-joined symbol numbers clicked so far), `altar_last_at` (Long, time of the last altar click), `altar_ready_at` (Long, 30s altar cooldown after a wrong order), `inst_seq` (String, symbols played so far in the current melody), `inst_started_at` (Long, when Start was clicked; 0 = no performance running), `inst_wrong` (Int, mistuned blocks hit in the current melody). `solved4` (Boolean, played the Room 4 melody correctly; set for online teammates too; Finish requires it), `finished` (Boolean, passed Finish; stops Finish killing a finished player who walks back over it; cleared by Reset), `door_ready_at` (Long, 5s per-player cooldown on all door heads, whether or not the door opens), `conduit_ready_at` (Long, 5s per-player Team Conduit cooldown whatever the outcome, extended to 30s while the word prompt is open so a second prompt can't stack).
- **Global:** `team_registry` (String, `word:createdSeconds:uuid,uuid;...`, only used during the 2-minute join window), `door3_close_at` / `door4_close_at` (Long, so a door closes 5s after the *last* click), `parkour_close_at` (Long, so the parkour course sinks 30s after the *last* correct melody).

Room 3 altar and doors (designed 2026-11-24):
- **Doors (Rooms 3 and 4):** each door has an outside head and an inside head. A click fills the door with air for 5s. Each player can click any door head only once every 5s (`DOOR_COOLDOWN`), allowed or not, so nobody can spam the door or its messages (user request 2026-11-25). The inside heads open for anyone, so nobody gets trapped. The Room 3 outside head needs `solved`; the Room 4 outside head needs `solved` and `solved3`. A player who sneaks into Room 3 unsolved can solve it out of order, which is accepted, but they still need Room 1 for Room 4.
- **Altar:** 10 symbol heads inside Room 3. Players click them in value order, lowest first. Every click plays the same amethyst chime and shows `(n/10)`; there's deliberately no rising pitch, which could be confused with Room 4. There's no right/wrong feedback until the 10th click. More than 15s between clicks, or clicking the same head twice, clears the offering with a message. A wrong order costs no hearts and has a 30s cooldown. The right order sets `solved3` for the player and their teammates (with the team check). Dying doesn't clear `solved3`, because the answer never changes; Reset and joining a team do.
- **Room 4 instrument (redesigned 2026-11-24):** each of Room 4's 10 note blocks has its own script, which knows its symbol (there's no NoteTune on Room 4's blocks). As in NoteTune, an unchanged note after `@delay 1` means a hit (playing) and a changed note means tuning. Tuning shows the pitch message and breaks a running performance.
  - **Start object:** a separate Start object (head/button, `Instrument_Start`) begins a performance. Until it's clicked, the blocks are free to play, so players can experiment without confusion. Only players with `solved` and `solved3` can start. Clicking it again restarts.
  - **Timing:** all 10 hits in Room 3 value order within **15s of clicking Start** (`INST_SECONDS` in the generator). Too slow → the Start script says the melody faded.
  - **Mistakes:** an out-of-order hit breaks the performance (click Start again).
  - **Tuning check:** each block's tuning is checked when it's hit. A complete melody with mistuned blocks gets a count only (never which). **No hearts are ever lost in Room 4.**
  - **Success:** a mini parkour course appears for **30s** (`PARKOUR_SECONDS`), shown by `/setblock`-ing each block in `PARKOUR_BLOCKS` to `PARKOUR_MATERIAL` and hidden by setting them back to air (generator settings). The test course is 13 single sea lanterns inside Room 4, from `-1824 75 1571` up to `-1830 87 1558`. If the real course is more detailed, switch to `/clone` from a hidden copy. A new correct melody while it's up extends it. The player and online teammates get `solved4` and a message. Failing the parkour means playing the melody again. The parkour start is only reachable from inside Room 4, so anyone who sneaks onto it is knowingly cheating (accepted).
  - **Finish:** a walk script at the end of the parkour (`Ocean_Puzzle_Finish.msc`). **Anti-cheat (2026-11-25):** anyone without `solved`, `solved3` and `solved4` is killed (`setHealth(0)`), which sends them back to the puzzle area checkpoint. The next checkpoint must be past Finish. Otherwise it sets `finished` and clears all of the player's puzzle progress and disbands their team (online same-ID teammates are told). The next checkpoint saves map progress, so nothing needs to be kept. Teammates who haven't finished keep all their progress (nothing of theirs is reset) and continue solo; the user may also move Finish farther down the line.

**Folders (2026-11-24):** the core scripts stay at the top level. `MainMap/` mirrors everything for the main map (see "Main map" below). Groups go in folders: `Room2_Symbols/`, `Room3_Altar/`, `Room4_Instrument/`, `Doors/` and `Instructions/`. `Testing/` holds test-server-only helpers (`Test_Complete_Room1/3/4/All.msc` set the solved flags for the clicking player and print the song as tuning positions). They are never handed to admins. Put new script groups in a folder of their own. **The altar, instrument and door scripts are generated** by `tools/gen_room_scripts.py` (`py tools/gen_room_scripts.py`). Edit the templates and settings there and regenerate, rather than editing the 25 files by hand. Regenerating overwrites hand edits such as door `corners`, so put those settings into the generator once they're known.

| File | Type | Purpose |
|---|---|---|
| Ocean_Puzzle_Noteblocks.msc | interact | Submit (1 of 12) |
| Ocean_Puzzle_Entrance.msc | walk | New answer on entry (2 of 12) |
| Ocean_Puzzle_Exit.msc | walk | Close stairway (3 of 12) |
| Ocean_Puzzle_Reset.msc | walk | Clear progress (4 of 12) |
| Ocean_Puzzle_NoteTune.msc | interact | "The note shifts to its Nth position." on Room 1's note blocks only (5 of 12) |
| Ocean_Puzzle_TeamConduit.msc | interact | Team word linking on the conduit (6 of 12) |
| Doors/Ocean_Puzzle_Door_Room3/4_Outside/Inside.msc | interact | Door heads (8 of 12). The 4 files are identical except for the settings block at the top (`need`, `door`, `corners`, `material`). Door corners and material come from `DOOR_CORNERS`/`DOOR_MATERIAL` in the generator (test values are set). |
| Room3_Altar/Ocean_Puzzle_Altar_01..10.msc | interact | Room 3 altar signs (9 of 12). Identical except `symbol` (1-10). Generated. |
| Room4_Instrument/Ocean_Puzzle_Instrument_01..10.msc + _Start.msc | interact | Room 4 instrument note blocks and the Start object (10 of 12). Voices are identical except `symbol` (1-10). Generated. |
| Ocean_Puzzle_Finish.msc | walk | End of the parkour: clears all progress, disbands the team (11 of 12) |
| Ocean_Puzzle_Forget.msc | interact | Room 1 "forget your song" head: confirm by typing `forget`; new song, Room 1 unsolved, leaves the team (12 of 12) |
| Room2_Symbols/Ocean_Puzzle_Symbol_01..10.msc | interact | Room 2 symbols (7 of 12). Each plays its slot of `answer` as a chime, heard only by the clicking player. The 10 files are identical except `slot` (0-9). Symbol N pairs with Room 1 note block N. |
| Instructions/Ocean_Puzzle_Instructions_Room1/3/4.msc | interact | Oracle instructions |

## Switching machines

The user works on more than one machine. This file is the full record: Claude's memory isn't synced between machines, so anything worth keeping goes here. On a new machine, run `git pull` first. On Windows, Python is run as `py`; elsewhere it may be `python3`. Generated scripts come from `tools/gen_room_scripts.py`, and `tools/room3_grids.py` reproduces the Room 3 grids.

## Status (as of 2026-11-24)

- **Tested and working** under the old `oceanpuzzle` namespace: submit check, hearts, entrance re-roll, stairway open/close.
- **Working under `puzzle1`:** Submit and Entrance, after re-importing the Entrance (an old `oceanpuzzle` copy was still bound). NoteTune works; `@delay 1t` was rejected, so it uses `@delay 1`. Interact scripts also fire on left-click (hit), so NoteTune compares the note before and after the delay and stays silent if it didn't change.
- **Tested solo and working:** all of Rooms 1-2's flow (instructions, NoteTune, entrance, submit, cooldown, hearts, death and new song, solve, stairway, exit, reset) and the Team Conduit with a team of one: word validation, prompt timeout, creating a word, "already bound", team-of-one submits and deaths, and the "bond dissolves" expiry. So `@prompt`, `String.matches`, `Player(uuid)` and the "{{...}}" Long-to-Int trick work.
- **`@prompt` timeout message:** it showed in yellow, ignoring `&` codes. It now uses `§` codes instead; whether that works is untested. If it doesn't, drop the colors from that one line.
- **Co-op tested 2026-11-24 (2 players), after re-importing everything:** a standard 2-player playthrough of Rooms 1-2 works. The team solved together and both were marked solved, and teammate messages now show in color (`§` codes in `sendMessage` confirmed).
- **NOT yet tested (edge cases, needs a second player):** the team check when someone goes offline or switches teams before a team event (new team ID, "no longer on your team" note), e.g. a teammate logging off and the rest completing the puzzle. The user considers this low priority.
- **Full solo run tested and working (2026-11-25):** Rooms 1-4 end to end: doors (Room 3 opens after Room 1, Room 4 stays shut until the altar), altar, instrument with Start, parkour shows and hides via `/setblock`, Finish passes a qualified player. Finish's anti-cheat kill also works: an old instrument script that didn't set `solved4` got the player killed there. Failure paths and co-op for Rooms 3-4 are still untested.
- **Room 3 playtest (2026-11-24):** a second player tried the grids for about 10 minutes without getting A. That is the intended difficulty; keep it.
- **Room 2 symbols and per-block particle feedback: tested solo and working (2026-11-23),** so `@bypass /playsound` and `/particle ... force <player>` work, as does `{{1573 - i}}.5` inside a command.
- **Debug:** the Submit script has `debug = true`, which prints the answer in chat. Turn it off before handing off to admins.

## Pending re-import

Everything on the test server was imported, and all variables defined, by 2026-11-25 (including the conduit cooldown). Keep this list up to date: add every script changed since then, and clear the list only when the user confirms they've re-imported. When they ask what needs importing, give this whole list, plus any one-time setup commands.

| Script | Bind to | What changed |
|---|---|---|
| (none) | | |

All one-time setup commands are listed in the Submit script header.

## Main map (2026-11-25)

The puzzle is ready for Minr's playtesting phase. Submitted maps are played by Green+ players before release, and admins must import every script *before* playtesting. `MainMap/` holds the main-map copy of every script (46 files, no `Testing/`). Generated ones come from `py tools/gen_room_scripts.py main` (the `MAIN` settings in the generator); the rest are hand copies.
- **Submit:** `debug = false`.
- **Coordinates:** the copies still hold test coordinates or blanks. `MainMap/COORDINATES_NEEDED.md` is the checklist of everything the user must supply. Some items come from other builders on the map team, so it may arrive in pieces.
- **Changes once coordinates arrive:**
  - Generalize the Submit particles, which assume the test line at x = -1852.
  - Switch doors (and the parkour, if detailed) to `/clone` copy-in/copy-out.
  - Fill every header.
- **Keep the copies in step:** changes to the test copies must also be made in `MainMap/` (or regenerated with `main`), and the reverse.

## Next up

1. **Test coordinates (waiting on the user):**
   - Both test doors are done (sea lantern; Room 3 `-1846 77 1553 -1841 75 1553`, Room 4 `-1839 76 1558 -1839 74 1560`; in `DOOR_CORNERS`/`DOOR_MATERIAL` in the generator). The real doors will be larger and more detailed, so switch the door scripts to the same `/clone` show/hide approach as the parkour (one command however detailed the door is) instead of many `/fill`s.
   - The 4 door heads, the 10 Room 4 note blocks and the Start object.
   - The Finish walk blocks.

   Put the door `corners` and parkour coordinates in the generator settings, then test the doors, the altar, the instrument and the parkour.
2. Instrument test points:
   - Whether a hit fires the script for players in the map's game mode (NoteTune suggests yes).
   - Whether 15s (from Start) is enough, and whether 30s of parkour is right.
   - That `/setblock` works through `@bypass` (show and hide), and that `setHealth(0.0D)` at Finish kills an unqualified player.
   - That Finish disbands the team.
3. Room 4 instructions rewritten and imported 2026-11-25 (6 lines, ~20s, 45s cooldown). Line 3 ("Wake it") may need to point at the Start object once its look is decided.
4. Later: co-op edge-case tests (see "NOT yet tested" above).
5. **Before admin handoff:** fill in everything in `MainMap/COORDINATES_NEEDED.md` (see "Main map" above).

## Decisions

- **Health (confirmed 2026-11-23):** natural regeneration is off, saturation is fixed and damage is disabled in the puzzle area, so wrong submits are the only way to lose health or die.

- **Instrument (2026-11-23):** packed ice under the Room 1 and Room 4 note blocks, which gives the chime sound (`minecraft:block.note_block.chime`, F#5-F#7), chosen for its watery, magical feel. The symbols play the same sound at pitch 2^((note-12)/12).

- **Forgotten notes (2026-11-25):** a player who didn't write down their Room 1 notes recovers them in Room 2. The symbols always replay that player's own `answer`, which nothing clears before Finish and other players can't change. They tune Room 4 by ear to match (same chime sound, no hearts lost, a count of mistuned voices). Room 1's note blocks are NOT a reliable source, because other players retune them. So Room 2 must stay reachable from Room 4 (via the inside door heads); never clear `answer` between Room 1 and Finish (except by the player's own choice at Forget).
- **Forget (2026-11-25):** Room 2's scattered symbols make re-listening tedious, so the user chose a self-reset over handing out the answer. The Forget head in Room 1 asks the player to type `forget`. It then gives a new song, sets `solved` (and `solved4`, any melody) back, keeps `solved3`, and removes the player from their team (teammates are told and keep their song). Griefing a team this way only removes the griefer. A forgetful team can re-team at the conduit, which un-solves Room 3 for them, as usual.

## Open questions

- The stairway is shared blocks, so while it's open, other players could slip through. This is currently accepted.
