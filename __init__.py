import copy
import math

EMPTY = 0
BLACK = 1
WHITE = -1

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

WEIGHT = [
    [1000, -300, 100, 50, 50, 100, -300, 1000],
    [-300, -500, -50, -50, -50, -50, -500, -300],
    [100, -50, 30, 10, 10, 30, -50, 100],
    [50, -50, 10, 5, 5, 10, -50, 50],
    [50, -50, 10, 5, 5, 10, -50, 50],
    [100, -50, 30, 10, 10, 30, -50, 100],
    [-300, -500, -50, -50, -50, -50, -500, -300],
    [1000, -300, 100, 50, 50, 100, -300, 1000],
]

def initial_board():
    board = [[EMPTY]*8 for _ in range(8)]
    board[3][3] = WHITE
    board[4][4] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    return board

def in_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def get_valid_moves(board, player):
    moves = []
    for x in range(8):
        for y in range(8):
            if board[x][y] == EMPTY and can_flip(board, x, y, player):
                moves.append((x, y))
    return moves

def can_flip(board, x, y, player):
    for dx, dy in DIRECTIONS:
        nx, ny = x+dx, y+dy
        found = False
        while in_board(nx, ny) and board[nx][ny] == -player:
            found = True
            nx += dx
            ny += dy
        if found and in_board(nx, ny) and board[nx][ny] == player:
            return True
    return False

def apply_move(board, x, y, player):
    new_board = copy.deepcopy(board)
    new_board[x][y] = player
    for dx, dy in DIRECTIONS:
        nx, ny = x+dx, y+dy
        flip = []
        while in_board(nx, ny) and new_board[nx][ny] == -player:
            flip.append((nx, ny))
            nx += dx
            ny += dy
        if flip and in_board(nx, ny) and new_board[nx][ny] == player:
            for fx, fy in flip:
                new_board[fx][fy] = player
    return new_board

def evaluate(board, player):
    score = 0

    for x in range(8):
        for y in range(8):
            if board[x][y] == player:
                score += WEIGHT[x][y]
            elif board[x][y] == -player:
                score -= WEIGHT[x][y]

    # 機動力（控えめ）
    mobility = len(get_valid_moves(board, player)) - len(get_valid_moves(board, -player))
    score += mobility * 2

    return score

def minimax(board, depth, alpha, beta, player, maximizing):
    moves = get_valid_moves(board, player)
    if depth == 0 or not moves:
        return evaluate(board, player), None

    best_move = None

    if maximizing:
        best_val = -math.inf
        for move in moves:
            new_board = apply_move(board, move[0], move[1], player)
            val, _ = minimax(new_board, depth-1, alpha, beta, -player, False)
            if val > best_val:
                best_val = val
                best_move = move
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return best_val, best_move
    else:
        best_val = math.inf
        for move in moves:
            new_board = apply_move(board, move[0], move[1], player)
            val, _ = minimax(new_board, depth-1, alpha, beta, -player, True)
            if val < best_val:
                best_val = val
                best_move = move
            beta = min(beta, val)
            if beta <= alpha:
                break
        return best_val, best_move

def ai_move(board, player, depth=5):
    _, move = minimax(board, depth, -math.inf, math.inf, player, True)
    return move

