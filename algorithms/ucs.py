import heapq

def ucs(grid_size, start, goal):
    rows, cols = grid_size
    heap = []
    heapq.heappush(heap, (0, start[0], start[1]))
    parent = {}
    cost_so_far = {}
    visited = []
    
    parent[(start[0], start[1])] = None
    cost_so_far[(start[0], start[1])] = 0

    while heap:
        cost, x, y = heapq.heappop(heap)
        if (x, y) == tuple(goal):
            break
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            new_cost = cost + 1  # Uniform cost of 1 per step
            if 0 <= nx < rows and 0 <= ny < cols:
                if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_cost
                    parent[(nx, ny)] = (x, y)
                    heapq.heappush(heap, (new_cost, nx, ny))
                    if (nx, ny) not in cost_so_far:
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