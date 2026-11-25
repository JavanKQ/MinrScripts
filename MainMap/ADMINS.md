# Ocean Puzzle: admin setup sheet

**Map:** [FILL IN: map name]

A four-room ocean temple puzzle, played solo or in co-op teams:
- **Room 1:** players tune 10 note blocks to a song made just for them.
- **Room 2:** symbols replay that song.
- **Room 3:** arithmetic grids reveal each symbol's value.
- **Room 4:** players play the song on an instrument in value order, which raises a parkour path to the exit.

All scripts are MSC 2.0 in the namespace `puzzle1`. **Only use the files in this `MainMap/` folder.** Every script also has a header with the same binding details as the table below.

## Checkpoints

- **Puzzle area checkpoint:** [FILL IN: x y z]. Deaths in the puzzle send players here.
- **Checkpoint after the puzzle:** `11443 168 10955`. It **must be past the Finish line** (Finish is at z=10964), so it can't be reached without passing Finish.

## Setup commands (run once, before importing)

```
/namespace define puzzle1
/variable define puzzle1 relative String answer = ""
/variable define puzzle1 relative Boolean solved = false
/variable define puzzle1 relative Long submit_ready_at = 0L
/variable define puzzle1 relative Long oracle_ready_at = 0L
/variable define puzzle1 relative Long chime_ready_at = 0L
/variable define puzzle1 relative String team = ""
/variable define puzzle1 relative String team_members = ""
/variable define puzzle1 relative Boolean solved3 = false
/variable define puzzle1 relative String altar_seq = ""
/variable define puzzle1 relative Long altar_last_at = 0L
/variable define puzzle1 relative Long altar_ready_at = 0L
/variable define puzzle1 relative String inst_seq = ""
/variable define puzzle1 relative Long inst_started_at = 0L
/variable define puzzle1 relative Int inst_wrong = 0
/variable define puzzle1 relative Boolean solved4 = false
/variable define puzzle1 relative Boolean finished = false
/variable define puzzle1 relative Long door_ready_at = 0L
/variable define puzzle1 relative Long conduit_ready_at = 0L
/variable define puzzle1 String team_registry = ""
/variable define puzzle1 Long door3_close_at = 0L
/variable define puzzle1 Long door4_close_at = 0L
/variable define puzzle1 Long parkour_close_at = 0L
```

### Entry and maze

| Script | Type | Bind to |
|---|---|---|
| `Maze/Maze_Teleport.msc` | walk | The block UNDER each pressure plate (2 binds): `11407 162 10964` and `11405 162 11002` |
| `Ocean_Puzzle_Reset.msc` | walk | Partway down the one-way drop out of the maze, every block across its width: [FILL IN] |
| `Ocean_Puzzle_Entrance.msc` | walk | The one-way drop into the puzzle area: 6 binds, `11441 162 10975` to `11446 162 10975` (fires as players drop through y163; bind to air with a temporary block) |

### Room 1

| Script | Type | Bind to |
|---|---|---|
| `Ocean_Puzzle_NoteTune.msc` | interact | Each of the 10 Room 1 note blocks (10 binds, same paste): see the note block table below |
| `Ocean_Puzzle_Noteblocks.msc` (Submit) | interact | Submit block: `11474 163 10978` |
| `Ocean_Puzzle_Exit.msc` | walk | Past the stairway, every block across the path's width: [FILL IN] |
| `Instructions/Ocean_Puzzle_Instructions_Room1.msc` | interact | Room 1 instructions head: `11459 161 10971` |
| `Ocean_Puzzle_TeamConduit.msc` | interact | Team Conduit: `11460 161 10979` |
| `Ocean_Puzzle_Forget.msc` | interact | Forget head: `11448 161 10979` |

Room 1 stairway (opened by Submit, closed by Exit): [FILL IN: region(s) and block type]

### Room 2

| Script | Type | Bind to |
|---|---|---|
| `Room2_Symbols/Ocean_Puzzle_Symbol_01.msc` ... `_10.msc` | interact | Symbol N's head in Room 2: see the symbol table below |

### Room 3

| Script | Type | Bind to |
|---|---|---|
| `Room3_Altar/Ocean_Puzzle_Altar_01.msc` ... `_10.msc` | interact | Symbol N's head on the altar: see the symbol table below |
| `Instructions/Ocean_Puzzle_Instructions_Room3.msc` | interact | Room 3 instructions head: `11423 161 10990` |
| `Doors/Ocean_Puzzle_Door_Room3_Outside.msc` | interact | Head outside the Room 3 door: `11432 161 10989` |
| `Doors/Ocean_Puzzle_Door_Room3_Inside.msc` | interact | Button inside the Room 3 door: `11428 161 10992` |

Room 3 door (set in the door scripts): prismarine wall, two regions: `11429 160-161 10990-10991` and `11431 160-161 10990-10991`.

### Room 4

| Script | Type | Bind to |
|---|---|---|
| `Room4_Instrument/Ocean_Puzzle_Instrument_01.msc` ... `_10.msc` | interact | Symbol N's note block in Room 4: see the symbol table below. **Do NOT also bind NoteTune here** |
| `Room4_Instrument/Ocean_Puzzle_Instrument_Start.msc` | interact | Start object: [FILL IN] |
| `Instructions/Ocean_Puzzle_Instructions_Room4.msc` | interact | Room 4 instructions head: [FILL IN] |
| `Doors/Ocean_Puzzle_Door_Room4_Outside.msc` | interact | Head outside the Room 4 door: `11453 161 10992` |
| `Doors/Ocean_Puzzle_Door_Room4_Inside.msc` | interact | Button inside the Room 4 door: `11458 161 10989` |
| `Ocean_Puzzle_Finish.msc` | walk | `11443 167 10964` and `11444 167 10964` (one bind each) |

Room 4 door (set in the door scripts): prismarine wall, two regions: `11457 160-162 10990-10991` and `11454 160-162 10990-10991`.
Parkour course (set in the Instrument scripts; players should find it hidden, i.e. air, before playtesting): 11 single glass panes, from `11443 161 10994` up to `11445 170 10990`. The Instrument scripts place them with `/setblock` and clear them back to air 30 s later.

### Symbol table (one row per symbol)

| Symbol | Room 1 note block | Room 2 symbol head | Room 3 altar head | Room 4 note block |
|---|---|---|---|---|
| 1 (A) | `11476 162 10968` | `11424 161 10977` | [FILL IN] | [FILL IN] |
| 2 (B) | `11476 162 10969` | `11420 168 10972` | [FILL IN] | [FILL IN] |
| 3 (C) | `11476 162 10970` | `11417 161 10976` | [FILL IN] | [FILL IN] |
| 4 (D) | `11476 162 10971` | `11428 166 10967` | [FILL IN] | [FILL IN] |
| 5 (E) | `11476 162 10972` | `11411 161 10972` | [FILL IN] | [FILL IN] |
| 6 (F) | `11476 162 10973` | `11411 168 10972` | [FILL IN] | [FILL IN] |
| 7 (G) | `11476 162 10974` | `11411 161 10970` | [FILL IN] | [FILL IN] |
| 8 (H) | `11476 162 10975` | `11423 168 10967` | [FILL IN] | [FILL IN] |
| 9 (I) | `11476 162 10976` | `11426 161 10970` | [FILL IN] | [FILL IN] |
| 10 (J) | `11476 162 10977` | `11427 161 10976` | [FILL IN] | [FILL IN] |

Room 1 note block N is the block whose note Symbol N plays (Submit checks them in this order). The Room 1 block does not need to sit next to its symbol; only the order matters.

## 5. Timings (for reference)

| Setting | Value |
|---|---|
| Room 4 melody time limit (after Start) | 15 s |
| Parkour stays up | 30 s |
| Doors stay open / door click cooldown | 5 s / 5 s |
| Wrong Room 1 submit | -2 hearts, 10 s cooldown |