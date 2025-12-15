# AI Othello player using Hutch-based heuristics
# Entry function name: myai

BOARD_SIZE = 8
EMPTY = 0
BLACK = 1
WHITE = -1

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

CORNERS = [(0,0), (0,7), (7,0), (7,7)]
X_SQUARES = [(1,1), (1,6), (6,1), (6,6)]

# -------------------------------
# Utility functions
# -------------------------------
def in_bounds(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def opponent(player):
    return -player

def valid_move(board, x, y, player):
    if board[x][y] != EMPTY:
        return False
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        found = False
        while in_bounds(nx, ny) and board[nx][ny] == opponent(player):
            found = True
            nx += dx
            ny += dy
        if found and in_bounds(nx, ny) and board[nx][ny] == player:
            return True
    return False

def valid_moves(board, player):
    return [(i, j) for i in range(8) for j in range(8)
            if valid_move(board, i, j, player)]

def apply_move(board, x, y, player):
    new_board = [row[:] for row in board]
    new_board[x][y] = player
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        flip = []
        while in_bounds(nx, ny) and new_board[nx][ny] == opponent(player):
            flip.append((nx, ny))
            nx += dx
            ny += dy
        if flip and in_bounds(nx, ny) and new_board[nx][ny] == player:
            for fx, fy in flip:
                new_board[fx][fy] = player
    return new_board

# -------------------------------
# Hutch-based heuristic
# -------------------------------
def heuristic(board, player):
    score = 0

    # Corner priority
    for x, y in CORNERS:
        if board[x][y] == player:
            score += 100
        elif board[x][y] == opponent(player):
            score -= 100

    # X-square penalty
    for x, y in X_SQUARES:
        if board[x][y] == player:
            score -= 30

    # Mobility
    score += 5 * (len(valid_moves(board, player))
                  - len(valid_moves(board, opponent(player))))

    # Disc count (late game effect)
    my_discs = sum(row.count(player) for row in board)
    opp_discs = sum(row.count(opponent(player)) for row in board)
    score += my_discs - opp_discs

    return score

# -------------------------------
# Entry AI function
# -------------------------------
def myai(board, player):
    moves = valid_moves(board, player)
    if not moves:
        return None

    best_score = -10**9
    best_move = moves[0]

    for x, y in moves:
        next_board = apply_move(board, x, y, player)
        s = heuristic(next_board, player)
        if s > best_score:
            best_score = s
            best_move = (x, y)

    return best_move

