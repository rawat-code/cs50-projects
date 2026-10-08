"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """Returns starting state of the board."""
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """Returns player who has the next turn on a board."""
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    # X always goes first, so X moves whenever counts are equal
    return X if x_count <= o_count else O


def actions(board):
    """Returns set of all possible actions (i, j) available on the board."""
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """Returns the board that results from making move (i, j) on the board."""
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid action")
    new_board = copy.deepcopy(board)  # never mutate the original board
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """Returns the winner of the game, if there is one."""
    lines = []
    lines.extend(board)                                              # rows
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])  # columns
    lines.append([board[i][i] for i in range(3)])                    # diagonal
    lines.append([board[i][2 - i] for i in range(3)])                # anti-diagonal

    for line in lines:
        if line[0] is not EMPTY and line[0] == line[1] == line[2]:
            return line[0]
    return None


def terminal(board):
    """Returns True if game is over, False otherwise."""
    if winner(board) is not None:
        return True
    return all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """Returns 1 if X has won, -1 if O has won, 0 otherwise."""
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0


def minimax(board):
    """Returns the optimal action for the current player on the board."""
    if terminal(board):
        return None

    if player(board) == X:
        # X is the maximizer
        best_value = -math.inf
        best_move = None
        for action in actions(board):
            value = min_value(result(board, action), best_value, math.inf)
            if value > best_value:
                best_value = value
                best_move = action
        return best_move
    else:
        # O is the minimizer
        best_value = math.inf
        best_move = None
        for action in actions(board):
            value = max_value(result(board, action), -math.inf, best_value)
            if value < best_value:
                best_value = value
                best_move = action
        return best_move


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:  # alpha-beta pruning: O would never allow this branch
            break
    return v


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if alpha >= beta:  # X would never allow this branch
            break
    return v