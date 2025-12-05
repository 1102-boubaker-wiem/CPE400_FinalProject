import csv
import os
import matplotlib.pyplot as plt

def load_stats(csv_file):
    link_probs = []
    losses = []
    delays = []
    throughputs = []

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            link_probs.append(float(row["link_prob"]))
            losses.append(float(row["packets_lost"]))
            delays.append(float(row["average_travel_time"]))
            throughputs.append(float(row["throughput_bps"]))

    return link_probs, losses, delays, throughputs

def plot_graphs(num_nodes, link_probs, losses, delays, throughputs):
    #  link_probs, losses, delays, throughputs = load_stats("stats.csv")
    
    # # create the output directory if doesn't already exist
    # output_dir = f"figures/{num_nodes}-nodes" 
    # os.makedirs(output_dir, exist_ok=True)

    # ---- PLOT 1: Packet Loss ----
    plt.figure("PacketLossFigure", figsize=(8, 5))
    plt.plot(link_probs, losses, label=f"{num_nodes} Nodes", marker='o', linewidth=2)
    # plt.savefig(f"{output_dir}/packet_loss.png")
    # plt.close()

    # ---- PLOT 2: Average Travel Time ----
    plt.figure("TravelTimeFigure", figsize=(8, 5))
    plt.plot(link_probs, delays, label=f"{num_nodes} Nodes", marker='o', linewidth=2)
    # plt.savefig(f"{output_dir}/travel_time.png")
    # plt.close()

    # ---- PLOT 3: Throughput ----
    plt.figure("ThroughputFigure", figsize=(8, 5))
    plt.plot(link_probs, throughputs, label=f"{num_nodes} Nodes", marker='o', linewidth=2)
    # plt.savefig(f"{output_dir}/throughput.png")
    # plt.close()
    
    # print(f"Plots saved to \"{output_dir}\"")

def save_graphs():
    # ---- PLOT 1: Packet Loss ----
    plt.figure("PacketLossFigure", figsize=(8, 5))
    plt.title(f"Packet Loss vs Link Probability")
    plt.xlabel("Link Probability")
    plt.ylabel("Packets Lost")
    plt.grid(True)
    plt.legend()
    plt.savefig("figures/packet_loss.png")
    plt.close()

    # ---- PLOT 2: Average Travel Time ----
    plt.figure("TravelTimeFigure", figsize=(8, 5))
    plt.title(f"Average Travel Time vs Link Probability")
    plt.xlabel("Link Probability")
    plt.ylabel("Average Travel Time (ms or weight units)")
    plt.grid(True)
    plt.legend()
    plt.savefig("figures/travel_time.png")
    plt.close()

    # ---- PLOT 3: Throughput ----
    plt.figure("ThroughputFigure", figsize=(8, 5))
    plt.title(f"Throughput vs Link Probability)")
    plt.xlabel("Link Probability")
    plt.ylabel("Throughput (bps)")
    plt.grid(True)
    plt.legend()
    plt.savefig("figures/throughput.png")
    plt.close()