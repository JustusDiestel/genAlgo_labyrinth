import numpy as np

class Maze:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = np.ones((height, width), dtype=int)

        # carve maze using DFS
        def carve(x, y):
            dirs = [(0,1),(1,0),(0,-1),(-1,0)]
            np.random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx*2, y + dy*2
                if 0 <= nx < height and 0 <= ny < width and self.grid[nx, ny] == 1:
                    self.grid[x+dx, y+dy] = 0
                    self.grid[nx, ny] = 0
                    carve(nx, ny)

        # start DFS from (1,1)
        self.grid[1,1] = 0
        carve(1,1)


        # Create some additional random connections to allow multiple paths
        extra_tunnels = (width * height) // 20
        for _ in range(extra_tunnels):
            rx, ry = np.random.randint(1, height-1), np.random.randint(1, width-1)
            if self.grid[rx, ry] == 1:
                self.grid[rx, ry] = 0


        self.START = (1,1)
        self.GOAL = (height-2, width-2)
        # make sure goal is on a free cell
        gr, gc = self.GOAL
        if self.grid[gr, gc] == 1:
            # search backwards until walkable
            for r in range(self.height - 2, 0, -1):
                for c in range(self.width - 2, 0, -1):
                    if self.grid[r, c] == 0:
                        self.GOAL = (r, c)
                        break
                else:
                    continue
                break

        # movement: right, down, left, up
        self.MOVES = [(0,1),(1,0),(0,-1),(-1,0)]

    def move(self, pos, move_idx):
        r, c = pos
        dr, dc = self.MOVES[move_idx]
        nr, nc = r + dr, c + dc

        # prevent out-of-bounds
        if nr < 0 or nr >= self.height or nc < 0 or nc >= self.width:
            return pos

        # check wall
        if self.grid[nr, nc] == 1:
            return pos

        return nr, nc