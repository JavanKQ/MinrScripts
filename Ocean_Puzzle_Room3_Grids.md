# Ocean Puzzle – Room 3 grids (design)

Room 3 has no scripts. It's five grids built on the walls: three on the room's walls and one on each side of the main room divider. Players work out a number value for each of the 10 symbols. Room 4 then asks them to play the symbols' notes in order of value, lowest first.

## Symbols: letters, numbers and player heads

The same 10 symbols are used in Rooms 2, 3 and 4. They're 10 custom player heads, and only their skin tells them apart. Designs and scripts refer to them by letter or number, never by appearance:

| Letter (designs) | Symbol number (scripts and headers) | Room 2 script |
|---|---|---|
| A | Symbol 1 | `Ocean_Puzzle_Symbol_01.msc` |
| B | Symbol 2 | `Ocean_Puzzle_Symbol_02.msc` |
| C | Symbol 3 | `Ocean_Puzzle_Symbol_03.msc` |
| D | Symbol 4 | `Ocean_Puzzle_Symbol_04.msc` |
| E | Symbol 5 | `Ocean_Puzzle_Symbol_05.msc` |
| F | Symbol 6 | `Ocean_Puzzle_Symbol_06.msc` |
| G | Symbol 7 | `Ocean_Puzzle_Symbol_07.msc` |
| H | Symbol 8 | `Ocean_Puzzle_Symbol_08.msc` |
| I | Symbol 9 | `Ocean_Puzzle_Symbol_09.msc` |
| J | Symbol 10 | `Ocean_Puzzle_Symbol_10.msc` |

**For admins:** which skin is "Symbol 1", "Symbol 2" and so on is decided by the map builder when placing heads and applying scripts. Whatever skin is bound to `Ocean_Puzzle_Symbol_01.msc` in Room 2 must be the head used for every **A** in these grids and for Symbol 1 in Room 4, and the same for the other nine.

## How the grids work

- Each grid is 3×3 cells. A cell is a plain number or a symbol head.
- There's a total to the right of each row and below each column.
- Each row and each column has its own hidden operator, the same in every grid. Players are never told the operators.
- Rows are worked left to right, and columns top to bottom, with no "multiply first" rule.
- No negative numbers appear anywhere.

Hidden operators (**never shown to players**):

| | Operator |
|---|---|
| Row 1 | + |
| Row 2 | − |
| Row 3 | × |
| Column 1 | × |
| Column 2 | + |
| Column 3 | − |

## The five grids

Grid 1 is all numbers. It's where players work out the operators. Each later grid adds new symbols.

```
Grid 1               Grid 2               Grid 3
 8   2   8 | 18       3   A   A | 21       5   2   B | 18
 9   4   2 |  3       7   2   4 |  1       A   F   E |  2
 5   8   3 | 120      C   B   3 | 231      7   D   F | 126
 ----------          ----------           ----------
360  14  3           147  22   2           315  11   4

Grid 4               Grid 5
 A   H   G | 23       F   I   I | 29
 B   D   2 |  3       G   H   H |  8
 H   G   D | 144      J   J   F | 75
 ----------          ----------
198  20   4           180  20   8
```

How it unfolds (checked by `tools/room3_grids.py`):

- **Grid 1:** only one set of operators fits, even if a player also tries division or mixes two operators in a line.
- **Grid 2:** settles A, B and C.
- **Grid 3:** leaves D, E and F each with two possible values (D and F are 3 and 6 in some order; E is 1 or 4).
- **Grid 4:** settles D, E and F, and also G and H.
- **Grid 5:** settles I and J.

Exactly one set of values fits all five grids (checked over every value from 0 to 60), and all 10 values are different.

## Answer (never shown to players)

| Symbol | A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|---|
| Symbol number | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| Value | 9 | 11 | 7 | 6 | 4 | 3 | 12 | 2 | 13 | 5 |

**Room 4 playing order, lowest value first:** H, F, E, J, D, C, A, B, G, I
= Symbols **8, 6, 5, 10, 4, 3, 1, 2, 7, 9**

## Notes

- Room 4's check script uses the symbol-number order above.
- The grids were generated with an earlier version of `tools/room3_grids.py` (seed 9). The current version of the tool produces different grids, so treat this file as the record of the chosen set.
- The Room 3 instructions don't hint that each row and column has its own operator. That's on purpose, to keep it hard. Revisit after playtesting.
