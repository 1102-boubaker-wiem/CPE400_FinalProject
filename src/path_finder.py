from collections import deque

def find_path(nodes, src_id, dst_id):
    lookup = {n.identifier: n for n in nodes}
    queue = deque([src_id])
    visited = {src_id: None}

    while queue:
        current = queue.popleft()
        if current == dst_id:
            break
        for neigh in lookup[current].links:
            if neigh not in visited:
                visited[neigh] = current
                queue.append(neigh)

    if dst_id not in visited:
        return None

    path = []
    curr = dst_id
    while curr is not None:
        path.append(curr)
        curr = visited[curr]

    return path[::-1]
