from Node import Node
import random

LINK_MIN_PERCENT = 0.5
MIN_LINK_WEIGHT = 1
MAX_LINK_WEIGHT = 1000

def main():
    # create nodes
    nodes = []
    nodes.append(Node("AA:AA:AA:AA"))
    nodes.append(Node("AA:AA:AA:AB"))
    nodes.append(Node("AA:AA:AA:AC"))
    nodes.append(Node("AA:AA:AA:AD"))
    nodes.append(Node("AA:AA:AA:AE"))
    nodes.append(Node("AA:AA:AA:AF"))
    nodes.append(Node("AA:AA:AA:B0"))
    nodes.append(Node("AA:AA:AA:B1"))
    nodes.append(Node("AA:AA:AA:B2"))
    nodes.append(Node("AA:AA:AA:B3"))
    
    generate_random_links(nodes)
    for node in nodes: 
        print(node)
    
def generate_random_links(nodes: list[Node]):
    # create links (adjacency table at first)
    links = [[0 for x in range(len(nodes))] for y in range(len(nodes))]
    
    # randomly generate links
    for i in range(0, len(nodes)-1):
        for j in range(i+1, len(nodes)):
            rand_weight = random.randint(MIN_LINK_WEIGHT, MAX_LINK_WEIGHT) if random.random() < LINK_MIN_PERCENT else 0
            links[i][j] = rand_weight
            links[j][i] = rand_weight
            
    # convert into adjacency lists in nodes
    for node_index in range(0, len(links)):
        for link_index in range(0, len(links[node_index])):
            node = nodes[node_index]
            identifier = nodes[link_index].identifier
            if (links[node_index][link_index] > 0):
                node.links[identifier] = links[node_index][link_index]
    
if __name__ == "__main__":
    main()