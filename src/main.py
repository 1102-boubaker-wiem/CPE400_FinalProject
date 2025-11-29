from graph_generator import generate_graph
from path_finder import find_path
from flow_simulator import FlowSimulator
from packet import Packet
from network import Network
import random

def main():
    # 1. Generate random network
    network = Network()
    nodes = generate_graph(network, 100)
    
    for i in range(0, 10):
        network.broadcast_ogm()
    
    src_node = random.choice([n for n in nodes])
    dest_node = random.choice([n for n in nodes if n is not src_node])
    packet = Packet(
        "data",
        src_node.identifier,
        dest_node.identifier,
        {
            "something important" : "goes here"
        }
    )
    
    nodes[0].send_packet(packet)
    
    print(packet)

if __name__ == "__main__":
    main()
