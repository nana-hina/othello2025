# Hutch-based Othello AI (sakura compatible)
# Entry function: myai

EMPTY = 0
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

CORNERS = [(0,0), (7,0), (0,7), (7,7)]
X_SQUARES = [(1,1), (6,1), (1,6), (6,6)]

# -------------------------
def opponent(p):
    return -p

def in_bounds(board, x, y):
    return 0 <= y < len(board) and 0 <= x < len(board[0])

def get(board, x, y):
    return board[y][x]

def valid_move(board, x, y, player):
    if not in_bounds(board, x, y):
        return False
    if get(board, x, y) != EMPTY:
        return False

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        found = False
        while in_bounds(board, nx, ny):
            v = get(board, nx, ny)
            if v == opponent(player):
                found = True
                nx += dx
                ny += dy
                continue
            if found and v == player:
                return True
            break
    return False

def valid_moves(board, player):
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if valid_move(board, x, y, player):
                moves.append((x, y))
    return moves

def apply_move(board, x, y, player):
    new_board = [row[:] for row in board]
    new_board[y][x] = player

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        flip = []
        while in_bounds(board, nx, ny) and new_board[ny][nx] == opponent(player):
            flip.append((nx, ny))
            nx += dx
            ny += dy
        if flip and in_bounds(board, nx, ny) and new_board[ny][nx] == player:
            for fx, fy in flip:
                new_board[fy][fx] = player
    return new_board

# -------------------------
# Hutch heuristic
def heuristic(board, player):
    score = 0

    # Corner priority
    for x, y in CORNERS:
        if in_bounds(board, x, y):
            if get(board, x, y) == player:
                score += 100
            elif get(board, x, y) == opponent(player):
                score -= 100

    # X-square penalty
    for x, y in X_SQUARES:
        if in_bounds(board, x, y) and get(board, x, y) == player:
            score -= 30

    # Mobility
    score += 5 * (len(valid_moves(board, player)) -
                  len(valid_moves(board, opponent(player))))

    # Disc count
    my = sum(row.count(player) for row in board)
    opp = sum(row.count(opponent(player)) for row in board)
    score += my - opp

    return score

# -------------------------
# Entry point
def myai(board, p
