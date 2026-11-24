"""Room 3 grid generator and checker for the Ocean Puzzle.

Each grid is 3x3 cells (plain numbers or symbols A-J), with a total to the
right of each row and below each column. Each row and each column has its own
hidden operator, the same in every grid, applied left to right (rows) or top
to bottom (columns). No negative numbers anywhere.

Symbols A-J are placeholders for Symbols 1-10 (A = Symbol 1 ... J = Symbol 10),
the 10 custom player heads shared by Rooms 2, 3 and 4.

The generator proves that:
  - The all-number lines of Grid 1 each fit only one operator, even if a
    player also tries division or mixing two operators within one line.
  - Across the grids, only the real operators work: every combination of
    + - x / for the rows and columns is tested, and only one survives by the
    end of Grid 2.
  - After each later grid, every symbol from earlier grids is pinned to one
    value, and each new symbol has at most 2 possible values (a later grid
    settles it).
  - After Grid 5, exactly one set of values fits, and all 10 are different.

Usage:  py tools/room3_grids.py [seed]
"""
import itertools
import random
import sys

ROW_OPS = ('+', '-', 'x')   # row 1, row 2, row 3
COL_OPS = ('x', '+', '-')   # column 1, column 2, column 3
TRUE_OPS = ROW_OPS + COL_OPS
SYMBOLS = 'ABCDEFGHIJ'
VALUE_RANGE = range(2, 16)     # real symbol values (distinct, no 0 or 1)
NUMBER_RANGE = range(2, 13)    # plain numbers written in cells
SEARCH_RANGE = range(0, 61)    # values a player might try when solving
MAX_TOTAL = 400                # keep the arithmetic doable by hand
NEW_PER_GRID = [2, 2, 2, 2, 2]  # new symbols introduced in grids 1-5
SYMBOL_CELLS = [2, 5, 7, 8, 9]  # how many of the 9 cells are symbols
MIN_TWO_WAY_STEPS = 2           # grids that leave a symbol with 2 options


def apply(op, xs):
    r = xs[0]
    for x in xs[1:]:
        if op == '+':
            r = r + x
        elif op == '-':
            r = r - x
        elif op == 'x':
            r = r * x
        elif op == '/':
            if x == 0 or r % x:
                return None
            r = r // x
        if r < 0:
            return None
    return r


def grid_lines(cells, rows, cols):
    """(cells, position 0-5, total) for each row then each column."""
    out = []
    for r in range(3):
        out.append(([cells[r][c] for c in range(3)], r, rows[r]))
    for c in range(3):
        out.append(([cells[r][c] for r in range(3)], 3 + c, cols[c]))
    return out


def value(cell, assign):
    return cell if isinstance(cell, int) else assign[cell]


def totals_for(cells, values):
    ls = grid_lines(cells, [0] * 3, [0] * 3)
    t = [apply(TRUE_OPS[pos], [value(x, values) for x in lc]) for lc, pos, _ in ls]
    return t[:3], t[3:]


def totals_ok(rows, cols):
    return all(t is not None and 0 < t <= MAX_TOTAL for t in rows + cols)


def operator_unique(nums, total, true_op):
    """Only the true operator (used twice) fits, among all pairs of + - x /."""
    a, b, c = nums
    hits = []
    for o1 in '+-x/':
        first = apply(o1, [a, b])
        if first is None:
            continue
        for o2 in '+-x/':
            if apply(o2, [first, c]) == total:
                hits.append((o1, o2))
    return hits == [(true_op, true_op)]


class TooAmbiguous(Exception):
    pass


def solve(cells, rows, cols, ops, partial, new_syms, budget=None):
    """All assignments of new_syms consistent with this grid under these ops.
    With a budget (shared dict {'left': n}), gives up by raising TooAmbiguous
    once that many candidate values have been tried."""
    ls = grid_lines(cells, rows, cols)
    results = []

    def complete_lines_ok(assign):
        if budget is not None:
            budget['left'] -= 1
            if budget['left'] < 0:
                raise TooAmbiguous()
        for lc, pos, tot in ls:
            if all(isinstance(x, int) or x in assign for x in lc):
                if apply(ops[pos], [value(x, assign) for x in lc]) != tot:
                    return False
        return True

    def rec(assign, todo):
        if not todo:
            results.append(dict(assign))
            return

        def completes(s):
            n = 0
            for lc, _, _ in ls:
                missing = {x for x in lc if isinstance(x, str) and x not in assign}
                if missing == {s}:
                    n += 1
            return n
        s = max(todo, key=completes)
        rest = [t for t in todo if t != s]
        for v in SEARCH_RANGE:
            assign[s] = v
            if complete_lines_ok(assign):
                rec(assign, rest)
            del assign[s]

    if complete_lines_ok(partial):
        rec(dict(partial), list(new_syms))
    return results


def random_grid(rng, count, new_syms, old_syms, values):
    for _ in range(4000):
        positions = rng.sample(range(9), count)
        pool = list(old_syms) + list(new_syms)
        picks = list(new_syms) + [rng.choice(pool) for _ in range(count - len(new_syms))]
        rng.shuffle(picks)
        cells = [[rng.choice(NUMBER_RANGE) for _ in range(3)] for _ in range(3)]
        for pos, sym in zip(positions, picks):
            cells[pos // 3][pos % 3] = sym
        rows, cols = totals_for(cells, values)
        if totals_ok(rows, cols):
            return cells, rows, cols
    return None


def grid1_ok(cells, rows, cols):
    """Grid 1's all-number lines must each point to exactly one operator."""
    for lc, pos, tot in grid_lines(cells, rows, cols):
        if all(isinstance(x, int) for x in lc):
            if not operator_unique(lc, tot, TRUE_OPS[pos]):
                return False
    return True


def grid1_op_candidates(grid):
    """Operator combinations a player can't rule out from Grid 1's all-number
    lines alone (those lines each prove their operator; see grid1_ok)."""
    cells, rows, cols = grid
    choices = []
    for lc, pos, _ in grid_lines(cells, rows, cols):
        if all(isinstance(x, int) for x in lc):
            choices.append([TRUE_OPS[pos]])
        else:
            choices.append(list('+-x/'))
    return [tuple(o) for o in itertools.product(*choices)]


def step(states, grid, new_syms, budget=None):
    cells, rows, cols = grid
    out = []
    for ops, vals in states:
        for v in solve(cells, rows, cols, ops, vals, new_syms, budget):
            out.append((ops, v))
            if len(out) > 60:
                return out
    return out


def generate(seed):
    rng = random.Random(seed)
    values = dict(zip(SYMBOLS, rng.sample(list(VALUE_RANGE), 10)))
    grids = []
    states = None
    known = []
    two_way = 0
    nxt = 0
    for k in range(5):
        new_syms = SYMBOLS[nxt:nxt + NEW_PER_GRID[k]]
        fallback = None
        chosen = None
        for _ in range(300):
            g = random_grid(rng, SYMBOL_CELLS[k], new_syms, known, values)
            if g is None:
                return None
            if k == 0:
                if not grid1_ok(*g):
                    continue
                cand = [(ops, {}) for ops in grid1_op_candidates(g)]
            else:
                cand = states
            try:
                new_states = step(cand, g, new_syms, {'left': 60000})
            except TooAmbiguous:
                continue
            if not new_states or len(new_states) > 60:
                continue
            if (TRUE_OPS, {s: values[s] for s in known + list(new_syms)}) not in new_states:
                continue
            if k >= 1:
                # Operators and all earlier symbols must be settled by now.
                if {ops for ops, _ in new_states} != {TRUE_OPS}:
                    continue
                if any(len({v[x] for _, v in new_states}) != 1 for x in known):
                    continue
                if any(len({v[x] for _, v in new_states}) > 2 for x in new_syms):
                    continue
            if k == 4 and len(new_states) != 1:
                continue
            is_two_way = 1 <= k <= 3 and any(
                len({v[x] for _, v in new_states}) == 2 for x in new_syms)
            if is_two_way or k in (0, 4):
                chosen = (g, new_states, is_two_way)
                break
            if fallback is None:
                fallback = (g, new_states, False)
        chosen = chosen or fallback
        if chosen is None:
            return None
        g, states, is_two_way = chosen
        two_way += is_two_way
        grids.append(g)
        known += list(new_syms)
        nxt += NEW_PER_GRID[k]
    return values, grids, two_way


def candidates_report(grids):
    """Possible values for each symbol after each grid, as a player sees it."""
    states = [(ops, {}) for ops in grid1_op_candidates(grids[0])]
    known = []
    nxt = 0
    lines = []
    for k, g in enumerate(grids):
        new_syms = SYMBOLS[nxt:nxt + NEW_PER_GRID[k]]
        states = step(states, g, new_syms)
        known += list(new_syms)
        nxt += NEW_PER_GRID[k]
        ops_left = len({ops for ops, _ in states})
        sym = ', '.join(f"{x}={'/'.join(str(v) for v in sorted({s[x] for _, s in states}))}" for x in known)
        lines.append(f'After grid {k + 1}: {ops_left} operator set(s) still possible; {sym}')
    return '\n'.join(lines)


def show(values, grids):
    out = []
    out.append('Operators: rows ' + ', '.join(ROW_OPS) + ' | columns ' + ', '.join(COL_OPS))
    for i, (cells, rows, cols) in enumerate(grids, 1):
        out.append('')
        out.append(f'Grid {i}')
        for r in range(3):
            out.append('  ' + ' '.join(f'{str(x):>4}' for x in cells[r]) + f'  | {rows[r]:>4}')
        out.append('  ' + '-' * 15)
        out.append('  ' + ' '.join(f'{t:>4}' for t in cols))
    out.append('')
    out.append('Values: ' + ', '.join(f'{s}={values[s]}' for s in SYMBOLS))
    order = sorted(SYMBOLS, key=lambda s: values[s])
    out.append('Room 4 order (lowest first): ' + ' '.join(order))
    out.append('')
    out.append(candidates_report(grids))
    return '\n'.join(out)


if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    while True:
        result = generate(seed)
        if result and result[2] >= MIN_TWO_WAY_STEPS:
            values, grids, amb = result
            print(f'Seed {seed}')
            print(show(values, grids))
            break
        seed += 1
