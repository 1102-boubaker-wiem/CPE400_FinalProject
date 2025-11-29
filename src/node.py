from packet import Packet

class Node:   
    def __init__(self, identifier, network):
        self.identifier = identifier
        self.network = network
        self.links = {}
        self.sequence_number = 0
        self.routing_table = {}
        self.ogm_sequence_nums = {}
        self.ogm_counts = {} # stores the number of OGMs for each originator and neighbor combo [neighbor][originator]
        
        # add node to the network
        network.nodes.append(self)
        
    def __str__(self):
        links_str = "\n".join([f"  {node} -> {weight}" for node, weight in self.links.items()])
        return f"Node {self.identifier}:\n{links_str if links_str else '  (no links)'}"
    
    def receive_packet(self, packet):
        # append self identifier to packet's path
        packet.path.append(self.identifier)
        
        if packet.type == "ogm":
            self.process_ogm(packet)
            return
        
        if packet.dest == self.identifier or packet.dest == "FF:FF:FF:FF:FF:FF":
            self.accept_packet(packet)
        else:
            self.send_packet(packet)
        
    def accept_packet(self, packet):
        print("packet meant for me")
        return
        
    def process_ogm(self, packet):
        originator = packet.data['originator']
        sequence = packet.data['sequence']
        ttl = packet.data['ttl']
        packet.data['ttl'] -= 1
        sender = packet.src # the neighbor that is forwarding the OGM
        
        # check if we are receiving our own OGMs for some reason
        if originator == self.identifier:
            return
        
        # check if old ogm (sequence number <= last sequence number)
        if originator in self.ogm_sequence_nums and sequence <= self.ogm_sequence_nums[originator]:
            return
        else:
            self.ogm_sequence_nums[originator] = sequence
        
        if ttl <= 0:
            return
        
        if sender not in self.ogm_counts:
            self.ogm_counts[sender] = {}
            
        if originator not in self.ogm_counts[sender]:
            self.ogm_counts[sender][originator] = 0
            
        self.ogm_counts[sender][originator] += 1
        
        self.update_routing_table()
        
        # forward ogm to all neighbors w/ updated src
        packet.src = self.identifier
        self.send_packet(packet)
        
    # update routing table based on current state of ogm_counts
    def update_routing_table(self):
        for (neighbor, originators) in self.ogm_counts.items():
            best_originator = min(originators.items(), key=lambda item: item[1])[0]
            self.routing_table[best_originator] = neighbor
        
    def send_packet(self, packet):
        # check if broadcasting
        if packet.dest == "FF:FF:FF:FF:FF:FF":
            for node_ident in self.links:
                self.network.get_node(node_ident).receive_packet(packet)
                return
        
        # check if there is a way to dest
        if packet.dest not in self.routing_table:
            print(f"\x1b[1;31mNo route to {packet.dest} through {self.identifier}!\x1b[0m")
            return
        
        # find which neighbor is best for dest
        first_hop_ident = self.routing_table[packet.dest]
        
        # forward packet through that node
        self.network.get_node(first_hop_ident).receive_packet(packet)
        
    def broadcast_ogm(self):
        self.sequence_number += 1
        ogm_packet = Packet(
            type = "ogm",
            src = self.identifier,
            dest = "FF:FF:FF:FF:FF:FF",
            data = {
                "originator": self.identifier,
                "sequence": self.sequence_number,
                "ttl": 64
            }
        )
        
        self.send_packet(ogm_packet)