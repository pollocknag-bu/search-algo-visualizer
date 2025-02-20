from collections import deque

def bfs(grid_size, start, goal):
    rows, cols = grid_size
    visited = []
    queue = deque([(start[0], start[1])])
    parent = {}
    
    while queue:
        x, y = queue.popleft()
        if (x, y) == tuple(goal):
            break
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in parent:
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))
                visited.append([nx, ny])
    
    # Path reconstruction
    path = []
    current = tuple(goal)
    while current != tuple(start):
        path.append(list(current))
        current = parent.get(current, None)
        if current is None: break
    return {'path': path[::-1], 'visited': visited}