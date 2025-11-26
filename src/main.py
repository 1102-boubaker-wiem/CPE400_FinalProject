from graph_generator import generate_graph
from path_finder import find_path
from flow_simulator import FlowSimulator

def main():
    # 1. Generate random network
    nodes = generate_graph()

    # 2. Choose sender & receiver
    src = "AA:AA:AA:AA"
    dst = "AA:AA:AA:B3"

    # 3. Find path
    path = find_path(nodes, src, dst)
    print("Path:", path)

    # If no path → skip
    if not path:
        print("No path found!")
        return

    # 4. Run flow simulation
    sim = FlowSimulator(nodes)
    results = sim.simulate_flow(path, n_packets=2000)

    # 5. Show results
    print("\n=== Experiment 1 Results ===")
    for k, v in results.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
