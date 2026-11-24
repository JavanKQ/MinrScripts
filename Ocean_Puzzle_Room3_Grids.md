# Ocean Puzzle – Room 3 grids (design)

Room 3 has no puzzle scripts, only the Oracle's instructions on a head block. It's five grids built on the walls: three on the room's walls and one on each side of the main room divider. Players work out a number value for each of the 10 symbols. Room 4 then asks them to play the symbols' notes in order of value, lowest first.

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
- **Every gap between two cells has its own hidden operator** (+, −, × or ÷). That's two per row and two per column, 12 in all, and they're the same in every grid. Players are never told any of them.
- Rows are worked strictly left to right and columns strictly top to bottom, with no "multiply first" rule. For example, 3 + 4 × 2 = 14.
- Division always comes out whole, and no number is ever negative.

Hidden operators (**never shown to players**):

| Line | Operators |
|---|---|
| Row 1 | cell − cell + cell |
| Row 2 | cell + cell × cell |
| Row 3 | cell − cell − cell |
| Column 1 | cell + cell × cell |
| Column 2 | cell × cell ÷ cell |
| Column 3 | cell + cell ÷ cell |

## The five grids

```
Grid 1                 Grid 2                 Grid 3
19   9   A |  22        B   A  20 |  21        B   F   E |  15
 5  10   3 |  45       12   7   C | 342       17   C   C | 630
23   6   3 |  14       18   D   2 |  12       24   2   B |   9
 -----------           -----------            -----------
552 15   5             450 21  19             720 54   2

Grid 4                 Grid 5
 H   A   G |   6        C   9   H |  25
 A   E   H | 320        H   F   A | 264
 5   2   G |   1        A   I   J |   2
 -----------           -----------
140 48   9             408 18   4
```

How it unfolds (checked by `tools/room3_grids.py`, seed 131):

- **Grid 1:** the all-number lines each fit only one pair of operators, even for a player who wrongly assumes "multiply first". The operators of row 1 and column 3, which contain A, stay open: A could be 6 or 12.
- **Grid 2:** settles those operators, so players go back to Grid 1 for A = 12. Also settles B, C and D.
- **Grid 3:** settles E and F.
- **Grid 4:** settles G and H.
- **Grid 5:** settles I and J.

Exactly one set of values fits (checked over every value from 0 to 120), and all 10 are different. The generator also rules out easy patterns: no symbol more than twice in a grid, no division of a number by itself, no line whose total equals one of its own cells, and no cell value or line total repeated in more than two grids.

## Answer (never shown to players)

| Symbol | A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|---|
| Symbol number | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| Value | 12 | 13 | 18 | 4 | 8 | 6 | 2 | 16 | 3 | 7 |

**Room 4 playing order, lowest value first:** G, I, D, F, J, E, A, B, H, C
= Symbols **7, 9, 4, 6, 10, 5, 1, 2, 8, 3**

## Notes

- Room 4's check script uses the symbol-number order above.
- To regenerate this exact set: `py tools/room3_grids.py 131`. Changing the generator's settings can change what a seed produces, so treat this file as the record of the chosen set.
- The Room 3 instructions hint at the rules in metaphor without stating them. See `Ocean_Puzzle_Instructions_Room3.msc`.
