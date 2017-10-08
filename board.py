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

    def find_groups(self):
        nrColumns = self.nrColumns
        nrLines = self.nrLines

        groups = []
        visited = []
        for i in xrange(nrLines):
            l = []
            for j in xrange(nrColumns):
                l.append(False)
            visited.append(l)

        for i in xrange(nrLines):
            for j in xrange(nrColumns):
                if not visited[i][j]:
                    group = self._find_group(make_pos(i, j))
                    for x, y in group:
                        visited[x][y] = 'True'
                    if len(group) > 1:
                        groups.append(group)
        return groups

    # Private methods: prefixed by "underscore"
    def _adjacent(self, pos):
        positions = [make_pos(pos[0] - 1, pos[1]), make_pos(pos[0] + 1, pos[1]), make_pos(pos[0], pos[1] - 1),
                     make_pos(pos[0], pos[1] + 1)]
        adjacent_positions = []
        color = self.board[pos[0]][pos[1]]
        for p in positions:
            if 0 <= p[0] < self.nrLines and 0 <= p[1] < self.nrColumns and self.board[p[0]][p[1]] == color:
                adjacent_positions.append(p)
        return adjacent_positions

    def _find_group(self, pos):
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
            for p in self._adjacent(pos):
                (x,y) = p
                if not visited[x][y]:
                    stack.append(p)
                    group.append(p)
                    visited[x][y] = True
        return group

#getattr(<object>,<name>) - retorna o valor do atributo <name> do <object>


def board_find_groups(board):
        return Board(board).find_groups()


def board_remove_group(b, group):

    nrColumns = getattr(b, 'nrColumns')
    nrLines = getattr(b, 'nrLines')
    board = getattr(b,'board')

    # removes the balls from the positions in the group
    for pos in group:
        board[pos[0]][pos[1]] = 0

    # drops the balls
    for j in xrange(nrColumns):
        for i in (xrange(nrLines)):
            if board[i][j] == 0:
                for k in reversed(xrange(i)):
                    board[k+1][j] = board[k][j]
                    board[k][j] = 0

    print b


b = Board([[3,2,2],[3,9,2],[3,1,2]])
print b

print '------------'

groups = board_find_groups([[3,2,2],[3,9,2],[3,1,2]])
print groups


print '-----------'

board_remove_group(b,groups[0])
