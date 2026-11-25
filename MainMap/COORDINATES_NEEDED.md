# Main map: what's needed before admins import

`MainMap/` holds the main-map copies of every Ocean Puzzle script (46 files). The test-server copies stay in the repo root folders, and `Testing/` is never handed over. **The MainMap copies still contain test-server coordinates (or blanks) until every item below is filled in. Don't give them to admins yet.**

Coordinates are `x y z`. A region means two opposite corners. "In symbol order" means Symbol 1 through Symbol 10, where Symbol N is the head skin chosen for design letter N (A = 1 ... J = 10).

## General

| # | Item | Notes |
|---|---|---|
| 1 | Map name / area name | Goes in every header's `Map/area` line |
| 2 | Which skin is Symbol 1-10 | Must be the same skin for Symbol N in Rooms 2, 3 and 4 and in the Room 3 grids (see `Ocean_Puzzle_Room3_Grids.md`) |
| 3 | Puzzle-area checkpoint location | Death (5th wrong Room 1 submit, Finish anti-cheat) sends players here |
| 4 | Next checkpoint after the puzzle | Must be past the Finish line |
| 5 | Confirm area settings for admins | No natural regen, fixed saturation, no damage in the puzzle area (wrong submits must be the only way to lose health) |

## Entry and maze

| # | Item | Notes |
|---|---|---|
| 6 | Reset walk blocks | Partway down the one-way drop out of the maze. Every block across the drop's width |
| 7 | Entrance walk blocks | The drop into the puzzle area, on the checkpoint side. Every block across its width |

## Room 1

| # | Item | Notes |
|---|---|---|
| 8 | The 10 note blocks, in symbol order | Each on packed ice. NoteTune is bound to each one. Particles show above each, and the script will be rewritten so any layout works |
| 9 | Submit block | |
| 10 | Stairway region(s) that open on solve, and their block type | Test: a ceiling region plus a wall region, prismarine bricks |
| 11 | Exit walk blocks | Close the stairway behind the player. Every block across the path's width |
| 12 | Room 1 instructions head | |
| 13 | Team Conduit block | |
| 14 | Forget head | |

## Room 2

| # | Item | Notes |
|---|---|---|
| 15 | The 10 symbol heads, in symbol order | |

## Room 3

| # | Item | Notes |
|---|---|---|
| 16 | The 10 altar heads, in symbol order | Each wears its symbol's skin |
| 17 | Room 3 instructions head | |
| 18 | Room 3 door: outside head and inside head | |
| 19 | Room 3 door shape | Either a simple region + block type, or (for a detailed door) a hidden copy of the closed door elsewhere, the same-size region it fills, and the door's position. I'll switch the doors to copy-in/copy-out for detailed doors |

## Room 4

| # | Item | Notes |
|---|---|---|
| 20 | Room 4 door: outside head, inside head, door shape | Same as items 18-19 |
| 21 | The 10 instrument note blocks, in symbol order | Each on packed ice and marked with its symbol's skin. No NoteTune on these |
| 22 | Start object | A head or button near the instrument. If its look is known, I can tailor the instructions' "Wake it" line |
| 23 | Room 4 instructions head | |
| 24 | Parkour course | Either the list of single blocks + block type (as on the test server), or, for a detailed course, a hidden copy, a same-size "empty" copy, and where it appears |
| 25 | Finish walk blocks | End of the parkour. Every block across the path's width |

## Timing (confirm or change)

| # | Item | Current |
|---|---|---|
| 26 | Melody time limit after Start | 15 s |
| 27 | How long the parkour stays up | 30 s |
| 28 | Door open time / click cooldown | 5 s / 5 s |

## Already done in MainMap

- Submit `debug = false` (no answers printed in chat).
- Generated scripts (doors, altar, instrument) come from `py tools/gen_room_scripts.py main`, using the `MAIN` settings in that file.
