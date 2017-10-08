from cStringIO import StringIO


def make_pos(l, c):
    return l, c

class Board:
    def __init__(self, board):
        self.board = board
        self.nrLines = len(board)
        self.nrColumns = len(board)

    def __str__(self):
        buff = ''
        for line in self.board:
            buff += '|'
            for piece in line:
                buff += str(piece) + '|'
            buff += '\n'
        return buff

    # Private methods: prefixed by "underscore"
    def adjacent(self, pos):
        positions = [make_pos(pos[0] - 1, pos[1]), make_pos(pos[0] + 1, pos[1]), make_pos(pos[0], pos[1] - 1),
                     make_pos(pos[0], pos[1] + 1)]
        adjacent_positions = []
        color = self.board[pos[0]][pos[1]]
        for p in positions:
            if 0 <= p[0] < self.nrLines and 0 <= p[1] < self.nrColumns and self.board[p[0]][p[1]] == color:
                adjacent_positions.append(p)
        return adjacent_positions

    def find_group(self, pos):
        """:return a list with all the positions of the balls in the same group as the ball in the given position"""
        group = [pos]
        visited = []
        stack = [pos]
        for i in xrange(self.nrLines):
            l = []
            for j in xrange(self.nrColumns):
                l.append(False)
            visited.append(l)

        visited[pos[0]][pos[1]] = True
        while stack:
            pos = stack.pop()
            for p in self.adjacent(pos):
                (x,y) = p
                if not visited[x][y]:
                    stack.append(p)
                    group.append(p)
                    visited[x][y] = True
        return group






b = Board([[1,1,2],[0,1,2],[1,3,2]])
print b
print b.find_group((0,0))
