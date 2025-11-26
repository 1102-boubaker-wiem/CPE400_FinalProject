import random

class FlowSimulator:
    def __init__(self, nodes):
        # Convert list → lookup dict
        self.nodes = {node.identifier: node for node in nodes}

    def simulate_flow(
        self,
        path,
        n_packets=1000,
        send_interval=0.01,
        error_prob=0.02,          # default link error probability
        packet_size_bytes=1000
    ):
        send_times = []
        arrival_times = []
        lost_packets = 0

        for i in range(n_packets):
            send_time = i * send_interval
            time = send_time
            lost = False

            for u, v in zip(path[:-1], path[1:]):
                # Link weight from node.links dictionary
                weight = self.nodes[u].links[v]

                # Convert weight into delay (you can adjust later)
                delay = weight / 100000.0

                # Apply error probability per hop
                if random.random() < error_prob:
                    lost = True
                    break

                time += delay

            if lost:
                lost_packets += 1
            else:
                send_times.append(send_time)
                arrival_times.append(time)

        # Metrics
        n_recv = len(arrival_times)
        loss_rate = lost_packets / n_packets

        if n_recv > 0:
            delays = [arr - snd for arr, snd in zip(arrival_times, send_times)]
            avg_delay = sum(delays) / len(delays)
            max_delay = max(delays)
            min_delay = min(delays)
            total_time = max(arrival_times) - min(send_times)
            throughput = (n_recv * packet_size_bytes * 8) / total_time
        else:
            avg_delay = max_delay = min_delay = throughput = None

        return {
            "path": path,
            "sent": n_packets,
            "received": n_recv,
            "loss_rate": loss_rate,
            "avg_delay": avg_delay,
            "min_delay": min_delay,
            "max_delay": max_delay,
            "throughput_bps": throughput
        }
