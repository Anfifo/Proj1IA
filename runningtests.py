import os
import time
from search import *
from utils import *
from board import *


def xx_recursive_sort(lst):
    """ Function needed to run some of the tests, that orders the groups
    according to a criteria. This is not the function used in evalutiation
    but it seems to output the same result. """
    for el in lst:
        el.sort()
    return lst

def xx_invalid_solution(item1, item2):
    print("function only defined in mooshak")

def greedy_search(problem, h=None):
    """f(n) = h(n)"""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, h)

def print_fancy_matrix(A):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in A]))

#Tabuleiro de 4x5 (linhas x colunas) com 2 cores sem solução
t4x5_2_ns = [[1,2,1,2,1],[2,1,2,1,2],[1,2,1,2,1],[2,1,2,1,2]]
#Tabuleiro de 4x5 (linhas x colunas) com 3 cores
t4x5_3 = [[1,2,2,3,3],[2,2,2,1,3],[1,2,2,2,2],[1,1,1,1,1]]
#Tabuleiro de 10x4 (linhas x colunas) com 3 cores sem solução
t10x4_3_ns = [[3,1,3,2],[1,1,1,3],[1,3,2,1],[1,1,3,3],[3,3,1,2],[2,2,2,2],[3,1,2,3],[2,3,2,3],[5,1,1,3],[4,5,1,2]]
#Tabuleiro de 10x4 (linhas x colunas) com 3 cores
t10x4_3 = [[3,1,3,2],[1,1,1,3],[1,3,2,1],[1,1,3,3],[3,3,1,2],[2,2,2,2],[3,1,2,3],[2,3,2,3],[2,1,1,3],[2,3,1,2]]
#Tabuleiro de 10x4 (linhas x colunas) com 5 cores
t10x4_5 = [[1,1,5,3],[5,3,5,3],[1,2,5,4],[5,2,1,4],[5,3,5,1], [5,3,4,4],[5,5,2,5],[1,1,3,1],[1,2,1,3],[3,3,5,5]]

problem_list = [t4x5_2_ns, t4x5_3, t10x4_3_ns, t10x4_3, t10x4_5]


def compare_board_searchers(problems, header,
                      searchers=[breadth_first_tree_search,
                                 breadth_first_search,
                                 depth_first_graph_search,
                                 iterative_deepening_search,
                                 depth_limited_search,
                                 recursive_best_first_search]):
    def do(searcher, problem):
        p = InstrumentedProblem(problem)
        start_time = time.time()
        searcher(p)
        return [p, time.time() - start_time]
    table = [[name(s)] + do(s, p) for p in problems for s in searchers]
    print_table(table, header)



def compare_board_solvers():
    problems = [same_game(problem) for problem in problem_list]
    compare_board_searchers(problems, ["searches","tests result", "time(s)"],
                            [depth_first_tree_search, greedy_search, astar_search])

def compare_board_solvers_last():
    problems = [same_game(t10x4_5)]
    compare_board_searchers(problems, ["searches", "tests result", "time(s)"],
                            [depth_first_tree_search, greedy_search, astar_search])


# print_fancy_matrix(t10x4_5)
compare_board_solvers()
#compare_board_solvers_last()


# def compare_solvers(problems, header,
#                       searchers=[breadth_first_tree_search,
#                                  breadth_first_search,
#                                  depth_first_graph_search,
#                                  iterative_deepening_search,
#                                  depth_limited_search,
#                                  recursive_best_first_search]):
#     def do(searcher, problem):
#         p = InstrumentedProblem(problem)
#         searcher(p)
#         return p
#     table = [[name(s)] + [do(s, p) for p in problems] for s in searchers]
#     print_table(table, header)


# resultados:
#     tempo de exec
#     numero de nos espandidos
#     numero de nos gerados
# targets:
#     procura em profundidade primeiro
#     procura greedy
#     procura A*






#
# directory = "tests/"
#
# folders_list = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isdir(os.path.join(directory, file))]
#
# for file_dir in folders_list:
#
#     file_list = [os.path.join(file_dir, file) for file in os.listdir(file_dir) if os.path.isfile(os.path.join(file_dir, file))]
#
#     print("test:" + file_dir + "\n\n")
#
#     for file in file_list:
#
#         f = open(file, "r")
#
#         for line in f:
#             if file[-5:] == "input":
#                 exec(line)
#             else:
#                 print("expected:\n" + line)
#
#         f.close()
#
# print(sorted(board_find_groups([[3,1,3,2],[1,1,1,3],[1,3,2,1],[1,1,3,3],[3,3,1,2],[2,2,2,2],[3,1,2,3],[2,3,2,3],[2,1,1,3],[2,3,1,2]])))
# print([[(0, 0)], [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (3, 0), (3, 1)], [(0, 2)], [(0, 3)], [(1, 3)], [(2, 1)], [(2, 2)], [(2, 3)], [(3, 2), (3, 3)], [(4, 0), (4, 1)], [(4, 2)], [(4, 3), (5, 0), (5, 1), (5, 2), (5, 3), (6, 2), (7, 2)], [(6, 0)], [(6, 1)], [(6, 3), (7, 3), (8, 3)], [(7, 0), (8, 0), (9, 0)], [(7, 1)], [(8, 1), (8, 2), (9, 2)], [(9, 1)], [(9, 3)]]
# )