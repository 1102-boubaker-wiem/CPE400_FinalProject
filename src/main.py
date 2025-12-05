from graph_generator import generate_graph, mutate_graph
from packet import Packet
from network import Network
from plot_stat import plot_graphs, load_stats
import random
import csv
MIN_PACKET_SIZE = 200    # bytes
MAX_PACKET_SIZE = 1500   # bytes

def main():
    # 1. Generate random network
    network = Network()
    
    stats = []
    num_packets = 5000
    num_nodes = 100
    for link_prob in [x / 100.0 for x in range(5, 100, 1)]:
        travel_time_sum = 0
        packets_lost = 0
        total_bytes = 0
        total_time = 0
        packet_size = random.randint(200, 1500)
        
        nodes = generate_graph(network, num_nodes, link_prob)
        network.nodes = nodes
        
        network.broadcast_ogm()
        
        for _ in range(0, num_packets):
            src_node = random.choice([n for n in nodes])
            dest_node = random.choice([n for n in nodes if n is not src_node])
            packet = Packet(
                "data",
                src_node.identifier,
                dest_node.identifier,
                {},
                size = packet_size
            )
            
            travel_time = src_node.send_packet(packet)
            if travel_time < 0:
                # print("\033[1;31mPacket Lost:\033[22m No route could be found!\033[0m")
                packets_lost += 1
            else:
                # print(f"\033[1;32mPacket Travel Time:\033[22m {travel_time}\033[0m")
                travel_time_sum += travel_time

                total_bytes+= packet.size
                total_time += travel_time     
        mutate_graph(nodes, link_prob)    
        print()
        print(f"\033[1mPackets Lost w/ {link_prob} link prob: {packets_lost} ({(packets_lost/num_packets)*100}%)\033[0m")
        
        average_travel_time = -1
        throughput = 0
        if (packets_lost != num_packets):
            average_travel_time = travel_time_sum / (num_packets - packets_lost)
            # convert time to milliseconds
            total_time_seconds = total_time / 1000 
            throughput = (total_bytes * 8) / total_time
            print(f"\033[1mAverage Travel Time w/ {link_prob} link prob: {average_travel_time}\033[0m")
            print(f"\033[1mThroughput w/ {link_prob}: {throughput} bps\033[0m")
        stats.append([link_prob, packets_lost, average_travel_time, throughput])
        
    with open("stats.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["link_prob", "packets_lost", "average_travel_time", "throughput_bps"])
        writer.writerows(stats)

    print("Data written to stats.csv successfully.")
    plot_graphs()

if __name__ == "__main__":
    main()
