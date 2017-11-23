# Grupo 02 # Andre Fonseca 84698 # Leonor Loureiro 84736
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


def aux_find_groups(pos, positions, group, board):
    top = make_pos(pos_l(pos) - 1, pos_c(pos))
    bottom = make_pos(pos_l(pos) + 1, pos_c(pos))
    right = make_pos(pos_l(pos), pos_c(pos) + 1)
    left = make_pos(pos_l(pos), pos_c(pos) - 1)

    lines, columns = board.get_dimensions()

    group.append(pos)

    if pos_l(top) >= 0 and board.get_ball(top) == board.get_ball(pos) and top not in group and top in positions:
        positions.remove(top)
        aux_find_groups(top, positions, group, board)

    if pos_l(bottom) < lines and board.get_ball(bottom) == board.get_ball(pos) and bottom not in group and bottom in positions:
        positions.remove(bottom)
        aux_find_groups(bottom, positions, group, board)

    if pos_c(right) < columns and board.get_ball(right) == board.get_ball(pos) and right not in group and right in positions:
        positions.remove(right)
        aux_find_groups(right, positions, group, board)

    if pos_c(left) >= 0 and board.get_ball(left) == board.get_ball(pos) and left not in group and left in positions:
        positions.remove(left)
        aux_find_groups(left, positions, group, board)


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

    def graphic_repr(self):
        buff = ''
        for line in self.board:
            buff += '|'
            for piece in line:
                buff += str(piece) + '|'
            buff += '\n'
        return buff

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
        return self.board == other.board

    def find_groups(self):
        """
        finds all groups of colours: a group is composed by adjacent elements with same colour
        :return: list with all groups of colours
        """
        board = self
        groups = []
        positions = []
        lines, columns = board.get_dimensions()

        for i in range(lines):
            for j in range(columns):
                if color(board.get_ball((make_pos(i, j)))):
                    positions.append(make_pos(i, j))

        while positions:
            group = []
            pos = positions.pop()
            aux_find_groups(pos, positions, group, board)
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



def board_find_groups(board):
    """
    :param board:
    :return: A List with all the groups in the given board
    """
    return Board(board).find_groups()


def board_remove_group(b, group):
    board = []
    for line in b:
        board_line = []
        for elem in line:
            board_line.append(elem)
        board.append(board_line)

    return Board(board).remove_group(group).board


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
        self.board = Board(board)

    def __lt__(self, other):
        """
        Less than operator
        :param other: stage to compare to
        :return: true if self < other, false otherwise
        """
        return True #len(self.board.find_groups()) < len(other.board.find_groups()) !!NOTE!! unused since it doesn't improve performance

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
        self.initial = sg_state(board)
        nr_lines, nr_columns = self.initial.board.get_dimensions()
        self.goal = sg_state([[0] * nr_columns] * nr_lines)

    def actions(self, state):
        actions = []
        for group in state.board.find_groups():
            if len(group) > 1:
                actions.append(group)
        return actions

    def result(self, state, action):
        return sg_state(board_remove_group(state.board.board, action))

    def goal_test(self, state):
        return no_color(state.board.get_ball(make_pos(state.board.get_dimensions()[0] - 1, 0)))

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        return len(node.state.board.find_groups())







