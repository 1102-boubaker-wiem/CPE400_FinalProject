from Node import Node
import random

def main():
    # create nodes
    nodes = []
    nodes.append(Node("A"))
    nodes.append(Node("B"))
    nodes.append(Node("C"))
    nodes.append(Node("D"))
    nodes.append(Node("E"))
    
    # create links (adjacency table at first)
    links = [[0 for x in range(len(nodes))] for y in range(len(nodes))]
    
    # randomly generate links
    for i in range(0, len(nodes)-1):
        for j in range(i+1, len(nodes)):
            rand_weight = random.randint(1, 100) if random.random() > 0.5 else 0
            links[i][j] = rand_weight
            links[j][i] = rand_weight
    
    # print links
    print_grid(links)
    
def print_grid(grid):
    for row in grid:
        for element in row:
            print(f"{element:<5}", end=" ")
        print()
    
if __name__ == "__main__":
    main()