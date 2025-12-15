# a090/__init__.py

EMPTY = 0
BLACK = 1
WHITE = -1

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
]

def opponent(p):
    return -p

def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def valid_move(board, x, y, player):
    if not in_bounds(x, y):
        return False
    if board[y][x] != EMPTY:
        return False

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while in_bounds(nx, ny) and board[ny][nx] == opponent(player):
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and in_bounds(nx, ny) and board[ny][nx] == player:
            return True

    return False

def valid_moves(board, player):
    return [(x, y) for y in range(8) for x in range(8)
            if valid_move(board, x, y, player)]

def evaluate(board, player):
    score = 0

    # 角重視
    corners = [(0,0),(7,0),(0,7),(7,7)]
    for x, y in corners:
        if board[y][x] == player:
            score += 30
        elif board[y][x] == opponent(player):
            score -= 30

    # モビリティ
    score += 2 * (len(valid_moves(board, player))
                  - len(valid_moves(board, opponent(player))))

    return score

def myai(board, player):
    moves = valid_moves(board, player)
    if not moves:
        return None

    best_score = -10**9
    best_move = moves[0]

    for x, y in moves:
        temp = [row[:] for row in board]
        temp[y][x] = player
        score = evaluate(temp, player)
        if score > best_score:
            best_score = score
            best_move = (x, y)

    return best_move
