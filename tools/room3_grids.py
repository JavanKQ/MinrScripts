"""Room 3 grid generator and checker for the Ocean Puzzle.

Each grid is 3x3 cells (plain numbers or symbols A-J), with a total to the
right of each row and below each column. Every gap between two cells has its
own hidden operator (+, -, x or /), so each row and each column has two
operators, 12 in all. They are the same in every grid. Lines are worked
strictly left to right (rows) or top to bottom (columns), with no "multiply
first" rule. Division always comes out whole, and nothing is ever negative.

Symbols A-J are placeholders for Symbols 1-10 (A = Symbol 1 ... J = Symbol 10),
the 10 custom player heads shared by Rooms 2, 3 and 4.

The checker proves that:
  - Each all-number line in Grid 1 fits exactly one pair of operators, and no
    other pair fits even for a player who assumes "multiply first".
  - Grid 1 deliberately leaves at least one line's operators open, so
    players must come back to it after Grid 2. Every combination of
    operators for those lines is tested, and only the real one survives by
    the end of Grid 2.
  - From Grid 2 on, every symbol is settled by the end of the grid that
    introduces it (searching values 0-120), and all 10 values are different.
  - No symbol appears more than twice in a grid, no division ever divides a
    value by itself, and no line's total equals one of its own cells.
  - No pattern repeats in more than two grids: the same symbol or value in
    the same cell, or the same total for the same row or column.

Usage:  py tools/room3_grids.py [seed] [time limit in seconds]
"""
import itertools
import random
import sys
import time

OPS = '+-x/'
PAIRS = [(a, b) for a in OPS for b in OPS]
SYMBOLS = 'ABCDEFGHIJ'
VALUE_RANGE = range(2, 21)      # real symbol values (distinct, no 0 or 1)
NUMBER_RANGE = range(2, 26)     # plain numbers written in cells
SEARCH_RANGE = range(0, 121)    # values a player might try when solving
MAX_TOTAL = 999                 # totals stay at 3 digits or fewer
NEW_PER_GRID = [1, 3, 2, 2, 2]  # new symbols introduced in grids 1-5
SYMBOL_CELLS = [1, 4, 6, 7, 8]  # how many of the 9 cells are symbols
MAX_PER_GRID = 2                # a symbol appears at most twice per grid
MAX_STATES = 3000               # cap on open possibilities after Grid 1


class TooAmbiguous(Exception):
    pass


def op(o, r, x):
    if o == '+':
        return r + x
    if o == '-':
        return r - x
    if o == 'x':
        return r * x
    if x == 0 or r % x:
        return None
    return r // x


def ltr(pair, xs):
    """Strict left-to-right evaluation (the real rule)."""
    r = xs[0]
    for o, x in zip(pair, xs[1:]):
        r = op(o, r, x)
        if r is None or r < 0:
            return None
    return r


def prec(pair, xs):
    """'Multiply first' evaluation, which a player might wrongly assume."""
    a, b, c = xs
    o1, o2 = pair
    if o1 in '+-' and o2 in 'x/':
        t = op(o2, b, c)
        if t is None or t < 0:
            return None
        r = op(o1, a, t)
        return r if r is not None and r >= 0 else None
    return ltr(pair, xs)


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


def totals_for(cells, values, ops):
    ls = grid_lines(cells, [0] * 3, [0] * 3)
    t = [ltr(ops[pos], [value(x, values) for x in lc]) for lc, pos, _ in ls]
    return t[:3], t[3:]


def totals_ok(rows, cols):
    return all(t is not None and 0 < t <= MAX_TOTAL for t in rows + cols)


def teaches(nums, total, true_pair):
    """Only the true pair fits left to right, and no other pair fits even
    with 'multiply first'."""
    if [p for p in PAIRS if ltr(p, nums) == total] != [true_pair]:
        return False
    return all(p == true_pair for p in PAIRS if prec(p, nums) == total)


def solve(cells, rows, cols, ops, partial, new_syms, budget=None):
    """All assignments of new_syms consistent with this grid under these ops."""
    ls = grid_lines(cells, rows, cols)
    results = []

    def complete_lines_ok(assign):
        if budget is not None:
            budget['left'] -= 1
            if budget['left'] < 0:
                raise TooAmbiguous()
        for lc, pos, tot in ls:
            if all(isinstance(x, int) or x in assign for x in lc):
                if ltr(ops[pos], [value(x, assign) for x in lc]) != tot:
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


def random_true_ops(rng):
    while True:
        ops = tuple(rng.choice(PAIRS) for _ in range(6))
        flat = [o for pair in ops for o in pair]
        if all(flat.count(o) >= 2 for o in OPS):
            return ops


def random_grid(rng, k, new_syms, pool, values, ops):
    count = SYMBOL_CELLS[k]
    for _ in range(5000):
        picks = list(new_syms) + [rng.choice(pool) for _ in range(count - len(new_syms))]
        if any(picks.count(s) > MAX_PER_GRID for s in picks):
            continue
        rng.shuffle(picks)
        positions = rng.sample(range(9), count)
        cells = [[rng.choice(NUMBER_RANGE) for _ in range(3)] for _ in range(3)]
        for pos, sym in zip(positions, picks):
            cells[pos // 3][pos % 3] = sym
        if self_division(cells, values, ops):
            continue
        rows, cols = totals_for(cells, values, ops)
        if totals_ok(rows, cols):
            return cells, rows, cols
    return None


def self_division(cells, values, ops):
    """True if any division in the grid divides a value by itself (a ÷ a = 1),
    or any line's total equals one of its own cells (for example
    a × b ÷ b = a, or b - b + c = c). Both are easy patterns to spot."""
    for lc, pos, _ in grid_lines(cells, [0] * 3, [0] * 3):
        xs = [value(x, values) for x in lc]
        if ltr(ops[pos], xs) in xs:
            return True  # the line cancels out to one of its own cells
        r = xs[0]
        for o, x in zip(ops[pos], xs[1:]):
            if o == '/' and r == x:
                return True
            r = op(o, r, x)
            if r is None:
                return False
    return False


def grid1_states(grid, true_ops):
    """Teach Grid 1's all-number lines; return every (ops, values) a player
    can't yet rule out, or None if a teaching line is ambiguous."""
    cells, rows, cols = grid
    choices = []
    for lc, pos, tot in grid_lines(cells, rows, cols):
        if all(isinstance(x, int) for x in lc):
            if not teaches(lc, tot, true_ops[pos]):
                return None
            choices.append([true_ops[pos]])
        else:
            choices.append(PAIRS)
    syms = sorted({x for row in cells for x in row if isinstance(x, str)})
    states = []
    for ops in itertools.product(*choices):
        for v in solve(cells, rows, cols, ops, {}, syms):
            states.append((ops, v))
            if len(states) > MAX_STATES:
                raise TooAmbiguous()
    return states


def step(states, grid, new_syms, budget=None):
    cells, rows, cols = grid
    out = []
    for ops, vals in states:
        for v in solve(cells, rows, cols, ops, vals, new_syms, budget):
            out.append((ops, v))
            if len(out) > 1:
                return out  # from Grid 2 on, only a single answer is accepted
    return out


def repeats_position(grids, values):
    """True if a pattern repeats across more than two grids: the same symbol
    in the same cell, the same value in the same cell (as a number or a
    symbol), or the same total for the same row or column."""
    seen = {}

    def add(key):
        seen[key] = seen.get(key, 0) + 1

    for cells, rows, cols in grids:
        for r in range(3):
            for c in range(3):
                x = cells[r][c]
                if isinstance(x, str):
                    add(('sym', x, r, c))
                add(('val', value(x, values), r, c))
        for i, t in enumerate(rows + cols):
            add(('total', i, t))
    return any(n > 2 for n in seen.values())


def generate(seed, deadline):
    rng = random.Random(seed)
    values = dict(zip(SYMBOLS, rng.sample(list(VALUE_RANGE), 10)))
    true_ops = random_true_ops(rng)
    grids = []
    states = None
    introduced = []
    nxt = 0
    for k in range(5):
        new_syms = list(SYMBOLS[nxt:nxt + NEW_PER_GRID[k]])
        pool = introduced + new_syms
        accepted = None
        for _ in range(500):
            if time.time() > deadline:
                return None
            g = random_grid(rng, k, new_syms, pool, values, true_ops)
            if g is None:
                return None
            if repeats_position(grids + [g], values):
                continue
            truth = {s: values[s] for s in pool}
            try:
                if k == 0:
                    new_states = grid1_states(g, true_ops)
                    if not new_states or (true_ops, truth) not in new_states:
                        continue
                    if len({ops for ops, _ in new_states}) < 2:
                        continue  # Grid 1 must leave some operators for Grid 2
                else:
                    new_states = step(states, g, new_syms, {'left': 200000})
                    if new_states != [(true_ops, truth)]:
                        continue
            except TooAmbiguous:
                continue
            accepted = (g, new_states)
            break
        if accepted is None:
            return None
        g, states = accepted
        grids.append(g)
        introduced += new_syms
        nxt += NEW_PER_GRID[k]
    if not good_mix(grids, values):
        return None
    return values, true_ops, grids


def good_mix(grids, values):
    """A good spread of 1-, 2- and 3-digit numbers across the whole set:
    at least a quarter of the cells single-digit and a quarter double-digit,
    and at least 6 each of 1-, 2- and 3-digit totals (out of 30)."""
    cells = [value(x, values) for g in grids for row in g[0] for x in row]
    totals = [t for g in grids for t in g[1] + g[2]]
    def digits(n):
        return len(str(n))
    quarter = len(cells) // 4
    if sum(digits(c) == 1 for c in cells) < quarter:
        return False
    if sum(digits(c) == 2 for c in cells) < quarter:
        return False
    return all(sum(digits(t) == d for t in totals) >= 6 for d in (1, 2, 3))


def candidates_report(grids, true_ops):
    states = grid1_states(grids[0], true_ops)
    lines = []
    introduced = list(SYMBOLS[:NEW_PER_GRID[0]])
    nxt = NEW_PER_GRID[0]

    def describe(k, states):
        ops_left = len({ops for ops, _ in states})
        sym = ', '.join(
            f"{x}={'/'.join(str(v) for v in sorted({s[x] for _, s in states}))}"
            for x in introduced)
        return f'After grid {k}: {ops_left} operator set(s) possible; {sym}'

    lines.append(describe(1, states))
    for k in range(1, 5):
        new_syms = list(SYMBOLS[nxt:nxt + NEW_PER_GRID[k]])
        states = step(states, grids[k], new_syms)
        introduced += new_syms
        nxt += NEW_PER_GRID[k]
        lines.append(describe(k + 1, states))
    return '\n'.join(lines)


def show(values, true_ops, grids):
    out = ['Hidden operators (left to right / top to bottom):']
    for r in range(3):
        a, b = true_ops[r]
        out.append(f'  Row {r + 1}:    cell {a} cell {b} cell')
    for c in range(3):
        a, b = true_ops[3 + c]
        out.append(f'  Column {c + 1}: cell {a} cell {b} cell')
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
    out.append('Room 4 order (lowest first): ' + ' '.join(order)
               + '  = Symbols ' + ', '.join(str(SYMBOLS.index(s) + 1) for s in order))
    out.append('')
    out.append(candidates_report(grids, true_ops))
    return '\n'.join(out)


if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    limit = float(sys.argv[2]) if len(sys.argv) > 2 else 120
    deadline = time.time() + limit
    while time.time() < deadline:
        result = generate(seed, deadline)
        if result:
            values, true_ops, grids = result
            print(f'Seed {seed}')
            print(show(values, true_ops, grids))
            sys.exit(0)
        seed += 1
    print(f'No grid set found within {limit:.0f} seconds (stopped at seed {seed}).')
    sys.exit(1)
