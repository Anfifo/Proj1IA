
def make_pos(l, c):
    return l, c


class Board:
    def __init__(self, board):
        self.board = board
        self.nr_lines = len(board)
        self.nr_columns = len(board)

    def __str__(self):
        buff = ''
        for line in self.board:
            buff += '|'
            for piece in line:
                buff += str(piece) + '|'
            buff += '\n'
        return buff

    def find_groups(self):
        nr_columns = self.nr_columns
        nr_lines = self.nr_lines

        groups = []
        visited = []
        for i in range(nr_lines):
            l = []
            for j in range(nr_columns):
                l.append(False)
            visited.append(l)

        for i in range(nr_lines):
            for j in range(nr_columns):
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
            if 0 <= p[0] < self.nr_lines and 0 <= p[1] < self.nr_columns and self.board[p[0]][p[1]] == color:
                adjacent_positions.append(p)
        return adjacent_positions

    def _find_group(self, pos):
        """:return a list with all the positions of the balls in the same group as the ball in the given position"""
        group = [pos]
        visited = []
        stack = [pos]
        for i in range(self.nr_lines):
            l = []
            for j in range(self.nr_columns):
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

    nr_columns = getattr(b, 'nr_columns')
    nr_lines = getattr(b, 'nr_lines')
    board = getattr(b,'board')

    # removes the balls from the positions in the group
    for pos in group:
        board[pos[0]][pos[1]] = 0

    # drops the balls
    for j in range(nr_columns):
        for i in (range(nr_lines)):
            if board[i][j] == 0:
                for k in reversed(range(i)):
                    board[k+1][j] = board[k][j]
                    board[k][j] = 0

    print (b)


b = Board([[3,2,2],[3,9,2],[3,1,2]])
print (b)

print ('------------')

groups = board_find_groups([[3,2,2],[3,9,2],[3,1,2]])
print (groups)


print ('-----------')

board_remove_group(b,groups[0])
