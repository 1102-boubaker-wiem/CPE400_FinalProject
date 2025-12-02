import csv
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

def plot_graphs():
    link_probs, losses, delays, throughputs = load_stats("stats.csv")

    # ---- PLOT 1: Packet Loss ----
    plt.figure(figsize=(8, 5))
    plt.plot(link_probs, losses, marker='o', linewidth=2)
    plt.title("Packet Loss vs Link Probability")
    plt.xlabel("Link Probability")
    plt.ylabel("Packets Lost (%)")
    plt.grid(True)
    plt.show()

    # ---- PLOT 2: Average Travel Time ----
    plt.figure(figsize=(8, 5))
    plt.plot(link_probs, delays, marker='o', color='orange', linewidth=2)
    plt.title("Average Travel Time vs Link Probability")
    plt.xlabel("Link Probability")
    plt.ylabel("Average Travel Time (ms or weight units)")
    plt.grid(True)
    plt.show()

    # ---- PLOT 3: Throughput ----
    plt.figure(figsize=(8, 5))
    plt.plot(link_probs, throughputs, marker='o', color='green', linewidth=2)
    plt.title("Throughput vs Link Probability")
    plt.xlabel("Link Probability")
    plt.ylabel("Throughput (bps)")
    plt.grid(True)
    plt.show()

# if __name__ == "__main__":
#     plot_graphs()
