# Ocean Puzzle: admin setup sheet

**Map:** [FILL IN: map name]  **Area:** [FILL IN: puzzle area name]  **Contact:** [FILL IN: map team contact]

A four-room ocean temple puzzle, played solo or in co-op teams:
- **Room 1:** players tune 10 note blocks to a song made just for them.
- **Room 2:** symbols replay that song.
- **Room 3:** arithmetic grids reveal each symbol's value.
- **Room 4:** players play the song on an instrument in value order, which raises a parkour path to the exit.

All scripts are MSC 2.0 in the namespace `puzzle1`. **Only use the files in this `MainMap/` folder.** Every script also has a header with the same binding details as the table below.

## 1. Area and build requirements

- **Health:** in the puzzle area, natural regeneration must be off, saturation fixed and damage disabled. Wrong Room 1 answers cost hearts, and that must be the only way to lose health.
- **Packed ice** under every Room 1 and Room 4 note block (gives the chime sound the puzzle relies on).
- **Symbol skins:** the 10 symbols are custom player heads. Whichever skin is used for Symbol N must be the same in Room 2, on the Room 3 altar, next to the Room 4 note block for Symbol N, and for letter N on the Room 3 grids (A = Symbol 1 ... J = Symbol 10).

  | Symbol | 1 (A) | 2 (B) | 3 (C) | 4 (D) | 5 (E) | 6 (F) | 7 (G) | 8 (H) | 9 (I) | 10 (J) |
  |---|---|---|---|---|---|---|---|---|---|---|
  | Skin | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |

- **Checkpoints:**
  - Puzzle area checkpoint: [FILL IN: x y z]. Deaths in the puzzle send players here.
  - Next checkpoint after the puzzle: [FILL IN: x y z]. It **must be past the Finish line**, so it can't be reached without passing Finish.

## 2. Setup commands (run once, before importing)

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
| `Ocean_Puzzle_Reset.msc` | walk | Partway down the one-way drop out of the maze, every block across its width: [FILL IN] |
| `Ocean_Puzzle_Entrance.msc` | walk | The one-way drop into the puzzle area (checkpoint side), every block across its width: [FILL IN] |

### Room 1

| Script | Type | Bind to |
|---|---|---|
| `Ocean_Puzzle_NoteTune.msc` | interact | Each of the 10 Room 1 note blocks (10 binds, same paste): see the note block table below |
| `Ocean_Puzzle_Noteblocks.msc` (Submit) | interact | Submit block: [FILL IN] |
| `Ocean_Puzzle_Exit.msc` | walk | Past the stairway, every block across the path's width: [FILL IN] |
| `Instructions/Ocean_Puzzle_Instructions_Room1.msc` | interact | Room 1 instructions head: [FILL IN] |
| `Ocean_Puzzle_TeamConduit.msc` | interact | Team Conduit: [FILL IN] |
| `Ocean_Puzzle_Forget.msc` | interact | Forget head: [FILL IN] |

Room 1 stairway (opened by Submit, closed by Exit): [FILL IN: region(s) and block type]

### Room 2

| Script | Type | Bind to |
|---|---|---|
| `Room2_Symbols/Ocean_Puzzle_Symbol_01.msc` ... `_10.msc` | interact | Symbol N's head in Room 2: see the symbol table below |

### Room 3

| Script | Type | Bind to |
|---|---|---|
| `Room3_Altar/Ocean_Puzzle_Altar_01.msc` ... `_10.msc` | interact | Symbol N's head on the altar: see the symbol table below |
| `Instructions/Ocean_Puzzle_Instructions_Room3.msc` | interact | Room 3 instructions head: [FILL IN] |
| `Doors/Ocean_Puzzle_Door_Room3_Outside.msc` | interact | Head outside the Room 3 door: [FILL IN] |
| `Doors/Ocean_Puzzle_Door_Room3_Inside.msc` | interact | Head inside the Room 3 door: [FILL IN] |

Room 3 door: [FILL IN: region and block type, or the location of a hidden copy of the closed door for a detailed door]

### Room 4

| Script | Type | Bind to |
|---|---|---|
| `Room4_Instrument/Ocean_Puzzle_Instrument_01.msc` ... `_10.msc` | interact | Symbol N's note block in Room 4: see the symbol table below. **Do NOT also bind NoteTune here** |
| `Room4_Instrument/Ocean_Puzzle_Instrument_Start.msc` | interact | Start object: [FILL IN] |
| `Instructions/Ocean_Puzzle_Instructions_Room4.msc` | interact | Room 4 instructions head: [FILL IN] |
| `Doors/Ocean_Puzzle_Door_Room4_Outside.msc` | interact | Head outside the Room 4 door: [FILL IN] |
| `Doors/Ocean_Puzzle_Door_Room4_Inside.msc` | interact | Head inside the Room 4 door: [FILL IN] |
| `Ocean_Puzzle_Finish.msc` | walk | End of the parkour, every block across the path's width: [FILL IN] |

Room 4 door: [FILL IN: same as Room 3]
Parkour course: [FILL IN: the single blocks and their block type, or a hidden copy of the course and where it appears]

### Symbol table (one row per symbol)

| Symbol | Room 1 note block | Room 2 symbol head | Room 3 altar head | Room 4 note block |
|---|---|---|---|---|
| 1 (A) | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |
| 2 (B) | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |
| 3 (C) | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |
| 4 (D) | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |
| 5 (E) | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |
| 6 (F) | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |
| 7 (G) | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |
| 8 (H) | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |
| 9 (I) | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |
| 10 (J) | [FILL IN] | [FILL IN] | [FILL IN] | [FILL IN] |

Room 1 note block N is the block whose note Symbol N plays (Submit checks them in this order). The Room 1 block does not need to sit next to its symbol; only the order matters.

## 5. Timings (for reference)

| Setting | Value |
|---|---|
| Room 4 melody time limit (after Start) | 15 s |
| Parkour stays up | 30 s |
| Doors stay open / door click cooldown | 5 s / 5 s |
| Wrong Room 1 submit | -2 hearts, 10 s cooldown |