from search import *


# TAI color
# sem cor = 0
# com cor > 0
def get_no_color():
    return 0


def no_color(c):
    return c == 0


def color(c):
    return c > 0


# TAI pos
# Tuple (l, c)
def make_pos(l, c):
    return (l, c)


def pos_l(pos):
    return pos[0]


def pos_c(pos):
    return pos[1]


class Board:
    """
    Represents a Same Game board
    """
    def __init__(self, board):
        """
        Constructor
        :param board:
        """
        self.board = board
        self.nr_lines = len(board)
        self.nr_columns = len(board[0])

    def __str__(self):
        """
        :return: String representation of the board
        """
        return str(self.board)

    def get_dimensions(self):
        return self.nr_lines, self.nr_columns

    def get_board(self):
        return self.board

    def get_ball(self, pos):
        return self.board[pos_l(pos)][pos_c(pos)]

    def set_ball_color(self, pos, ball_color):
        self.board[pos_l(pos)][pos_c(pos)] = ball_color

    def move_ball_to(self, to_pos, from_pos):
        value = self.get_ball(from_pos)
        self.set_ball_color(to_pos, value)
        self.set_ball_color(from_pos, get_no_color())

    def __eq__(self, other):
        return self.board == other.get_board()

    def find_groups(self):
        """
        :return: A list with all the groups in the board
        """
        nr_columns = self.nr_columns
        nr_lines = self.nr_lines

        groups = []
        visited = []
        for i in range(nr_lines):
            visited.append([False]*nr_columns)

        for i in range(nr_lines):
            for j in range(nr_columns):
                if not visited[i][j] and self.get_ball(make_pos(i, j)):
                    group = self._find_group(make_pos(i, j))
                    for x, y in group:
                        visited[x][y] = True
                    groups.append(group)
        return groups

    def remove_group(self, group):

        # removes the balls from the positions in the group
        for pos in group:
            self.set_ball_color(pos, get_no_color())

        # drops the balls
        for j in reversed(range(self.nr_columns)):
            empty_column = True  # empty column flag

            for i in range(self.nr_lines):
                if no_color(self.get_ball(make_pos(i, j))):
                    for line in reversed(range(i)):
                        upper_pos = make_pos(line, j)
                        lower_pos = make_pos(line + 1, j)
                        self.move_ball_to(lower_pos, upper_pos)

                else:
                    empty_column = False

            # removes the empty column and pushes all elements to the left
            if empty_column:
                for column in range(j, self.nr_columns - 1):
                    for line in range(self.nr_lines):
                        right_column = make_pos(line, column + 1)
                        left_column = make_pos(line, column)
                        self.move_ball_to(left_column, right_column)

        return self

    def _adjacent(self, pos):
        """
        :param pos:
        :return: A list with the positions of the adjacent pieces of the same color of the pice in the given position
        """
        positions = [make_pos(pos_l(pos) - 1, pos_c(pos)), make_pos(pos_l(pos) + 1, pos_c(pos)), make_pos(pos_l(pos), pos_c(pos) - 1),
                     make_pos(pos_l(pos), pos_c(pos) + 1)]
        adjacent_positions = []
        c = self.get_ball(pos)
        for p in positions:
            if 0 <= pos_l(p) < self.nr_lines and 0 <= pos_c(p) < self.nr_columns and self.get_ball(p) == c:
                adjacent_positions.append(p)
        return adjacent_positions

    def _find_group(self, pos):
        """
        :param pos:
        :return a list with all the positions of the balls in the same group as the ball in the given position
        """
        group = [pos]
        visited = []
        stack = [pos]
        for i in range(self.nr_lines):
            lst = []
            for j in range(self.nr_columns):
                lst.append(False)
            visited.append(lst)

        visited[pos_l(pos)][pos_c(pos)] = True
        while stack:
            pos = stack.pop()
            for p in self._adjacent(pos):
                (x, y) = p
                if not visited[x][y]:
                    stack.append(p)
                    group.append(p)
                    visited[x][y] = True
        return group


def board_find_groups(board):
    """
    :param board:
    :return: A List with all the groups in the given board
    """
    return Board(board).find_groups()


def board_remove_group(b, group):
    board = []
    if isinstance(b, Board):
        old_board = b.get_board()
    else:
        old_board = b

    for line in old_board:
        board_line = []
        for elem in line:
            board_line.append(elem)
        board.append(board_line)
    return Board(board).remove_group(group)


class sg_state:
    """
    Represent a stage in the game
    """
    def __init__(self, board):

        """
        Constructor
        :param board:
        :type: board: Board
        """
        if isinstance(board, Board):
            self.board = board
        else:
            self.board = Board(board)
        self.cost = 0

    def set_cost(self, cost):
        self.cost = cost

    def get_cost(self):
        return self.cost

    def get_board(self):
        """
        :return:
        :rtype:
        """
        return self.board

    def get_groups(self):
        return self.board.find_groups()

    def __eq__(self, other):
        """
        :param: other: board to compare to
        :rtype: bool
        """
        return self.board == other.get_board()

    def __lt__(self, other):
        """
        Less than operator
        :param other: stage to compare to
        :return: true if self < other, false otherwise
        """
        return self.cost < other.get_cost()

    def __str__(self):
        return str(self.board)


class same_game(Problem):  # class <class_name>(<super_class>):
    """
    Models a Same Game problem as a satisfaction problem.
    A solution cannot have pieces left on the board.
    """
    def __init__(self, board):
        """
        :param board: [a lista of lists]
        """
        self.initial = sg_state(Board(board))
        nr_lines, nr_columns = self.initial.get_board().get_dimensions()
        self.goal = sg_state(Board([[0] * nr_columns] * nr_lines))

    def actions(self, state):
        actions = []
        for group in state.get_groups():
            if len(group) > 1:
                actions.append(group)
        return actions

    def result(self, state, action):
        return sg_state(board_remove_group(state.get_board(), action))

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        state2.set_cost(c+1)
        return c + 1

    def h(self, node):
        print(isinstance(node, sg_state))
        # return len(node.get_groups())
        return 0




#print(board_remove_group([[4,4,4,2],[4,4,4,3],[4,4,4,1],[4,4,4,4],[4,4,4,2],[4,4,4,4],[4,4,4,3],[4,4,4,3],[4,4,4,4],[4,4,4,2]], [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (8, 3), (5, 3), (3, 3)]))

print(astar_search(same_game([[1,1,5,3],[5,3,5,3],[1,2,5,4],[5,2,1,4],[5,3,5,1],[5,3,4,4],[5,5,2,5],[1,1,3,1],[1,2,1,3],[3,3,5,5]])))