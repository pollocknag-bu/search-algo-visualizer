import heapq

def a_star(grid_size, start, goal, weights, heuristicFuntion):
    rows, cols = grid_size
    visited = []
    pq = [(0, start)]  
    parent = {}
    cost_so_far = {start: 0}

    def heuristic_manhatton(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def heuristic_sld(a, b):
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5    

    heuristicFunctionMap = {
        "straightLine": heuristic_sld,
        "manhattan": heuristic_manhatton
    }

    while pq:
        current_priority, current_node = heapq.heappop(pq)
        x, y = current_node

        if current_node == goal:
            break

        if current_node in visited:
            continue
        visited.append(current_node)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                next_node = (nx, ny)
                new_cost = cost_so_far[current_node] + weights[nx][ny]
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristicFunctionMap[heuristicFuntion](next_node, goal)
                    heapq.heappush(pq, (priority, next_node))
                    parent[next_node] = current_node

    # Path reconstruction
    path = []
    current = goal
    while current != start:
        path.append(list(current))
        current = parent.get(current)
        if current is None:
            break
    return {'path': path[::-1], 'visited': visited}
