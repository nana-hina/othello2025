import copy

EMPTY = 0
DIR = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

# 角重視テーブル
WEIGHT = [
    [100, -30, 10, 5, 5, 10, -30, 100],
    [-30, -50, -5, -5, -5, -5, -50, -30],
    [10, -5, 5, 3, 3, 5, -5, 10],
    [5, -5, 3, 1, 1, 3, -5, 5],
    [5, -5, 3, 1, 1, 3, -5, 5],
    [10, -5, 5, 3, 3, 5, -5, 10],
    [-30, -50, -5, -5, -5, -5, -50, -30],
    [100, -30, 10, 5, 5, 10, -30, 100],
]

def in_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def valid(board, x, y, color):
    if board[x][y] != EMPTY:
        return False
    for dx, dy in DIR:
        nx, ny = x+dx, y+dy
        found = False
        while in_board(nx, ny) and board[nx][ny] == -color:
            found = True
            nx += dx
            ny += dy
        if found and in_board(nx, ny) and board[nx][ny] == color:
            return True
    return False

def moves(board, color):
    return [(x,y) for x in range(8) for y in range(8) if valid(board,x,y,color)]

def put(board, x, y, color):
    b = copy.deepcopy(board)
    b[x][y] = color
    for dx, dy in DIR:
        nx, ny = x+dx, y+dy
        tmp = []
        while in_board(nx, ny) and b[nx][ny] == -color:
            tmp.append((nx, ny))
            nx += dx
            ny += dy
        if tmp and in_board(nx, ny) and b[nx][ny] == color:
            for tx, ty in tmp:
                b[tx][ty] = color
    return b

def eval_board(board, color):
    score = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == color:
                score += WEIGHT[x][y]
            elif board[x][y] == -color:
                score -= WEIGHT[x][y]
    return score

def minimax(board, color, depth):
    ms = moves(board, color)
    if depth == 0 or not ms:
        return eval_board(board, color), None

    best = -10**9
    best_move = ms[0]

    for m in ms:
        b2 = put(board, m[0], m[1], color)
        val, _ = minimax(b2, -color, depth-1)
        val = -val
        if val > best:
            best = val
            best_move = m

    return best, best_move

def myai(board, color):
    ms = moves(board, color)

    # 角があれば即取る
    for c in [(0,0),(0,7),(7,0),(7,7)]:
        if c in ms:
            return c

    _, move = minimax(board, color, depth=2)
    return move
