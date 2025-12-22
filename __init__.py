import random

# 石の定義（hachi仕様）
EMPTY = 0
BLACK = 1
WHITE = -1

# 8方向
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

# 角・安定度重視の評価マップ
EVAL = [
    [120, -40,  20,   5,   5,  20, -40, 120],
    [-40, -80,  -5,  -5,  -5,  -5, -80, -40],
    [ 20,  -5,  15,   3,   3,  15,  -5,  20],
    [  5,  -5,   3,   3,   3,   3,  -5,   5],
    [  5,  -5,   3,   3,   3,   3,  -5,   5],
    [ 20,  -5,  15,   3,   3,  15,  -5,  20],
    [-40, -80,  -5,  -5,  -5,  -5, -80, -40],
    [120, -40,  20,   5,   5,  20, -40, 120],
]

# -------------------------
# 合法手判定
# -------------------------
def inside(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def can_put(board, color, x, y):
    if board[x][y] != EMPTY:
        return False
    opp = -color
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        found = False
        while inside(nx, ny) and board[nx][ny] == opp:
            nx += dx
            ny += dy
            found = True
        if found and inside(nx, ny) and board[nx][ny] == color:
            return True
    return False

def legal_moves(board, color):
    return [(x, y) for x in range(8) for y in range(8) if can_put(board, color, x, y)]

# -------------------------
# 石を置く
# -------------------------
def put(board, color, x, y):
    new = [row[:] for row in board]
    new[x][y] = color
    opp = -color
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        path = []
        while inside(nx, ny) and new[nx][ny] == opp:
            path.append((nx, ny))
            nx += dx
            ny += dy
        if path and inside(nx, ny) and new[nx][ny] == color:
            for px, py in path:
                new[px][py] = color
    return new

# -------------------------
# 評価関数（角＋安定度）
# -------------------------
def evaluate(board, color):
    score = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == color:
                score += EVAL[x][y]
            elif board[x][y] == -color:
                score -= EVAL[x][y]
    return score

# -------------------------
# 1手先読み（軽量）
# -------------------------
def myai(board, color):
    moves = legal_moves(board, color)
    if not moves:
        return None

    best_score = -10**9
    best_move = None

    for x, y in moves:
        b2 = put(board, color, x, y)
        score = evaluate(b2, color)

        # 相手の返し手を少しだけ考慮
        opp_moves = legal_moves(b2, -color)
        if opp_moves:
            worst = 10**9
            for ox, oy in opp_moves:
                b3 = put(b2, -color, ox, oy)
                worst = min(worst, evaluate(b3, color))
            score = (score + worst) // 2

        if score > best_score:
            best_score = score
            best_move = (x, y)

    return best_move

