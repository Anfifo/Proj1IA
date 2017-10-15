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
        buff = ''
        for line in self.board:
            buff += '|'
            for piece in line:
                buff += str(piece) + '|'
            buff += '\n'
        return buff

    def get_dimensions(self):
        return self.nr_lines , self.nr_columns

    def get_board(self):
        return  self.board

    def get_ball(self, pos):
        return self.board[pos_l(pos)][pos_c(pos)]

    def set_ball_color(self, pos, color):
        self.board[pos_l(pos)][pos_c(pos)] = color

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
            self.set_ball_color(pos, 0)

        # drops the balls
        for j in range(self.nr_columns):
            empty_column = True  # empty column flag

            for i in range(self.nr_lines):

                if no_color(self.get_ball(make_pos(i,j))):

                    for k in reversed(range(i)):
                        self.set_ball_color(make_pos(k+1,j), self.get_ball(make_pos(k,j)))
                        self.set_ball_color(make_pos(k, j), 0)

                else:
                    empty_column = False

            # removes the empty column and pushes all elements to the left
            if empty_column:
                for k in range(j, self.nr_columns - 1):
                    for i in range(self.nr_lines):
                        self.set_ball_color(make_pos(i, k), self.get_ball(make_pos(i, k + 1)))
                        self.set_ball_color(make_pos(i, k + 1), 0)

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
            l = []
            for j in range(self.nr_columns):
                l.append(False)
            visited.append(l)

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
    for line in b.get_board():
        board_line = []
        for elem in line:
            board_line.append(elem)
        board.append(board_line)
    return Board(board).remove_group(group)

class sg_stage:
    """
    Represent a stage in the game
    """
    def __init__(self, board):

        """
        Constructor
        :param board:
        :type: board: Board
        """
        self.board = board
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
        self.initial = sg_stage(Board(board))
        nr_lines, nr_columns = self.initial.get_board().get_dimensions()
        self.goal = sg_stage(Board([[0] * nr_columns] * nr_lines))

    def actions(self, state):
        actions = []
        for group in state.get_groups():
            if len(group) > 1:
                actions.append(group)
        return actions

    def result(self, state, action):
        return sg_stage(board_remove_group(state.get_board(),action))


    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        state2.set_cost(c+1)
        return c + 1

    def h(self, node):
        pass

"""
b1_list= [[2,2,2],[1,1,1],[1,1,1]]
b1 = Board(b1_list)
game = same_game(b1_list)
"""

"""
state1 = sg_stage(b1)
print("State 1:")
print(state1)
print(game.h(state1))

#print(game.goal_test(state1))

actions1 = game.actions(state1)
#print (actions1)

state2 = game.result(state1, actions1[0])
print("State 2:")
print(state2)
print(game.h(state2))

#print(game.goal_test(state2))

actions2 = game.actions(state2)
#print (actions2)

state3 = game.result(state2, actions2[0])
print("State 3:")
print(state3)
print(game.h(state3))


"""

#print(game.goal_test(state3))


