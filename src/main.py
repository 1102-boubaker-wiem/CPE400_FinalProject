from graph_generator import generate_graph
from path_finder import find_path
from flow_simulator import FlowSimulator
from packet import Packet
from network import Network
import random

def main():
    # 1. Generate random network
    network = Network()
    nodes = generate_graph(network, 25)
    
    for i in range(0, 10):
        network.broadcast_ogm()
    
    num_packets = 100
    travel_time_sum = 0
    packets_lost = 0
    for i in range(0, num_packets):
        src_node = random.choice([n for n in nodes])
        dest_node = random.choice([n for n in nodes if n is not src_node])
        packet = Packet(
            "data",
            src_node.identifier,
            dest_node.identifier,
            {}
        )
        
        travel_time = src_node.send_packet(packet)
        if travel_time < 0:
            print("\033[1;31mPacket Lost:\033[22m No route could be found!\033[0m")
            packets_lost += 1
        else:
            print(f"\033[1;32mPacket Travel Time:\033[22m {travel_time}\033[0m")
            travel_time_sum += travel_time
                        
    print()
    print(f"\033[1mPackets Lost: {packets_lost} ({(packets_lost/num_packets)*100}%)\033[0m")
    
    if (packets_lost != num_packets):
        average_travel_time = travel_time_sum / (num_packets - packets_lost)
        print(f"\033[1mAverage Travel Time: {average_travel_time}\033[0m")

if __name__ == "__main__":
    main()
