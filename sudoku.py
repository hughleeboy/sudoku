class Illegal(Exception):
    pass

class board:
    def __init__(self, s):
        #init 2x2 grid of (val, possibilities)
        #2d list compr
        self.grid = [ [ 
            [ch, {'1','2','3','4','5','6','7','8','9'}] for ch in r ] 
            for r in s.split('|') ]
        self.resolve_possib()

    def _won(self):
        #determine anything left to fill
        won=True
        for r in self.grid:
            for c in r:
                if c[0] == ' ': won=False
        return won

    def succ(self):
        grid = self.grid
        if self._won(): return []

        #check if lost
        for r in grid:
            for c in r:
                if c[0] == ' ' and c[1] == set(): return []

        #find min branching factor
        m = min( filter(lambda x: x[0] != 0, [(len(grid[r][c][1]), r, c) for c in range(9) for r in range(9)]) )

        #create all succs
        return [board(repr(self))._choose(m[1], m[2], poss) for poss in grid[m[1]][m[2]][1]]

    def solve(self):
        if self._won(): 
            yield self
        #return all solutions
        for succ in self.succ():
            for soln in succ.solve():
                yield soln

    def _choose(self, r, c, val):
        self.grid[r][c][0] = val
        self.resolve_possib()
        return self

    def resolve_possib(self):
        grid = self.grid

        #set already chosen squares to empty
        for r in grid:
            for c in r:
                if c[0] != ' ': c[1] = set()

        #rows
        for r in range(0, 9):
            used = set()
            for c in range(0, 9):
                val = grid[r][c][0]
                if val != ' ':
                    if grid[r][c][0] in used: raise Illegal("row",r,c)
                    else: used.add(grid[r][c][0])
            for c in range(0, 9):
                grid[r][c][1] = grid[r][c][1].difference(used)

        #cols
        for c in range(0, 9):
            used = set()
            for r in range(0, 9):
                val = grid[r][c][0]
                if val != ' ':
                    if grid[r][c][0] in used: raise Illegal("col",r,c)
                    else: used.add(grid[r][c][0])
            for r in range(0, 9):
                grid[r][c][1] = grid[r][c][1].difference(used)

        #squares
        for rr in range(0, 3):
            for cc in range(0,3):
                used = set()
                for ro in range(0, 3):
                    for co in range(0, 3):
                        r = rr*3+ro
                        c = cc*3+co
                        val = grid[r][c][0]
                        if val != ' ':
                            if grid[r][c][0] in used: raise Illegal("box",r,c)
                            else: used.add(grid[r][c][0])
                for ro in range(0, 3):
                    for co in range(0, 3):
                        r = rr*3+ro
                        c = cc*3+co
                        grid[r][c][1] = grid[r][c][1].difference(used)

    def __repr__(self):
        s = ''
        for r in self.grid:
            for c in r:
                s += str(c[0])
            s += '|'
        return s[:-1]

    def __str__(self):
        g = self.grid
        s = f"""
{g[0][0][0]}{g[0][1][0]}{g[0][2][0]}|{g[0][3][0]}{g[0][4][0]}{g[0][5][0]}|{g[0][6][0]}{g[0][7][0]}{g[0][8][0]}
{g[1][0][0]}{g[1][1][0]}{g[1][2][0]}|{g[1][3][0]}{g[1][4][0]}{g[1][5][0]}|{g[1][6][0]}{g[1][7][0]}{g[1][8][0]}
{g[2][0][0]}{g[2][1][0]}{g[2][2][0]}|{g[2][3][0]}{g[2][4][0]}{g[2][5][0]}|{g[2][6][0]}{g[2][7][0]}{g[2][8][0]}
-----------
{g[3][0][0]}{g[3][1][0]}{g[3][2][0]}|{g[3][3][0]}{g[3][4][0]}{g[3][5][0]}|{g[3][6][0]}{g[3][7][0]}{g[3][8][0]}
{g[4][0][0]}{g[4][1][0]}{g[4][2][0]}|{g[4][3][0]}{g[4][4][0]}{g[4][5][0]}|{g[4][6][0]}{g[4][7][0]}{g[4][8][0]}
{g[5][0][0]}{g[5][1][0]}{g[5][2][0]}|{g[5][3][0]}{g[5][4][0]}{g[5][5][0]}|{g[5][6][0]}{g[5][7][0]}{g[5][8][0]}
-----------
{g[6][0][0]}{g[6][1][0]}{g[6][2][0]}|{g[6][3][0]}{g[6][4][0]}{g[6][5][0]}|{g[6][6][0]}{g[6][7][0]}{g[6][8][0]}
{g[7][0][0]}{g[7][1][0]}{g[7][2][0]}|{g[7][3][0]}{g[7][4][0]}{g[7][5][0]}|{g[7][6][0]}{g[7][7][0]}{g[7][8][0]}
{g[8][0][0]}{g[8][1][0]}{g[8][2][0]}|{g[8][3][0]}{g[8][4][0]}{g[8][5][0]}|{g[8][6][0]}{g[8][7][0]}{g[8][8][0]}
"""
        return s

import sys

def __main__():
    puzzles = [line.split() for line in open('puzzles', 'r')]
    puzzles = {p[0]: p[1].replace('.', ' ') for p in puzzles}

    with open('solutions', 'w') as outfile:
        for puzzle in puzzles.items():
            outfile.write(f'{puzzle[0]} {repr(next(board(puzzle[1]).solve(), None))}\n')

    #b = board(puzzles['easy'])
    #for sol in b.solve():
    #    print(sol)

__main__()


