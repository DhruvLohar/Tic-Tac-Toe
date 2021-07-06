def win_indexes(n):
    for r in range(n):
        yield [(r, c) for c in range(n)]
    for c in range(n):
        yield [(r, c) for r in range(n)]

    yield [(i, i) for i in range(n)]
    yield [(i, n - 1 - i) for i in range(n)]

def is_winner(layout, current):
    n = len(layout)
    for indexes in win_indexes(n):
        if all(layout[r][c] == current for r, c in indexes):
            return True
    return False

def is_tie(layout):
    common = list(set([alias for sublist in layout for alias in sublist]))
    return True if ('X' or 'O') and not '-' in common else False

def get_location(pos):
    x, y = pos
    if 0 < x < 200 and 100 < y < 300:
        return (1, 1, 70, 150)
    elif 200 < x < 400 and 100 < y < 300:
        return (1, 2, 270, 150)
    elif 400 < x < 600 and 100 < y < 300:
        return (1, 3, 470, 150)
    elif 0 < x < 200 and 300 < y < 500:
        return (2, 1, 70, 350)
    elif 200 < x < 400 and 300 < y < 500:
        return (2, 2, 270, 350)
    elif 400 < x < 600 and 300 < y < 500:
        return (2, 3, 470, 350)
    elif 0 < x < 200 and 500 < y < 700:
        return (3, 1, 70, 550)
    elif 200 < x < 400 and 500 < y < 700:
        return (3, 2, 270, 550)
    elif 400 < x < 600 and 500 < y < 700:
        return (3, 3, 470, 550)
