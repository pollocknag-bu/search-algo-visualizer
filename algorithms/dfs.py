def dfs(grid_size, start, goal):
    rows, cols = grid_size
    stack = [(start[0], start[1])]
    parent = {}
    visited = []
    parent[(start[0], start[1])] = None

    while stack:
        x, y = stack.pop()
        if (x, y) == tuple(goal):
            break
        # Explore neighbors in reverse order (up, left, down, right)
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in parent:
                parent[(nx, ny)] = (x, y)
                stack.append((nx, ny))
                visited.append([nx, ny])

    # Path reconstruction
    path = []
    current = tuple(goal)
    while current != tuple(start):
        path.append(list(current))
        current = parent.get(current, None)
        if current is None: 
            path = []
            break
    return {'path': path[::-1], 'visited': visited}