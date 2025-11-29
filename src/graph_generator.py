from node import Node
import random

LINK_PROBABILITY = 0.5
MIN_LINK_WEIGHT = 1
MAX_LINK_WEIGHT = 1000

def generate_graph(network, num_nodes):
    macs = [":".join(f'{i:012X}'[j:j+2] for j in range(0, 12, 2)) for i in range(num_nodes)]
    
    nodes = [Node(mac, network) for mac in macs]
    n = len(nodes)

    # generate adjacency matrix
    matrix = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(i+1, n):
            if random.random() < LINK_PROBABILITY:
                w = random.randint(MIN_LINK_WEIGHT, MAX_LINK_WEIGHT)
                matrix[i][j] = w
                matrix[j][i] = w

    # convert matrix → adjacency lists
    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                nodes[i].links[nodes[j].identifier] = matrix[i][j]

    return nodes
