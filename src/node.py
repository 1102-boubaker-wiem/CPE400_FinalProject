from packet import Packet
BANDWIDTH = 1_000_000

class Node:   
    def __init__(self, identifier, network):
        self.identifier = identifier
        self.network = network
        self.links = {}
        self.sequence_number = 0
        self.routing_table = {}
        self.ogm_sequence_nums = {}
        self.ogm_counts = {} # stores the number of OGMs for each originator and neighbor combo [originator][neighbor]
        
        # add node to the network
        network.nodes.append(self)
        
    def __str__(self):
        links_str = "\n".join([f"  {node} -> {weight}" for node, weight in self.links.items()])
        return f"Node {self.identifier}:\n{links_str if links_str else '  (no links)'}"
    
    def receive_packet(self, packet):
        # append self identifier to packet's path
        # packet.path.append(self.identifier)
        
        if packet.type != "ogm":
            packet.path.append(self.identifier)

        if packet.type == "ogm":
            self.process_ogm(packet)
            return 0
        
        if packet.dest == self.identifier or packet.dest == "FF:FF:FF:FF:FF:FF":
            self.accept_packet(packet)
            return 0
        else:
            return self.send_packet(packet)
        
    def accept_packet(self, packet):
        return
        
    def process_ogm(self, packet):
        sender = packet.src # the neighbor that is forwarding the OGM
        originator = packet.data['originator']
        sequence = packet.data['sequence']
        
        # get link weight (representing time for packet to cross that link) and subtract from ttl
        weight = self.links[sender]
        ttl = packet.data['ttl']
        # ttl -= weight
        if originator == self.identifier or sender == self.identifier:
            return
        # drop expired OGM
        ttl -= weight
        if ttl <= 0:
            return
    
        
         # Initialize per-originator tracking structures
        counts_for_originator = self.ogm_counts.setdefault(originator, {})
        seqs_for_originator = self.ogm_sequence_nums.setdefault(originator, {})

        # Global duplicate suppression:
        # If we've already seen this sequence (from ANY neighbor), drop it.
        max_seen = max(seqs_for_originator.values(), default=-1)
        if sequence <= max_seen:
            return

        # Update per-neighbor last sequence
        last_seq_from_sender = seqs_for_originator.get(sender, -1)
        if sequence <= last_seq_from_sender:
            return
        seqs_for_originator[sender] = sequence

        # Increment count of OGMs from this neighbor for this originator
        counts_for_originator[sender] = counts_for_originator.get(sender, 0) + 1
        
        self.update_routing_table()
        # Re-broadcast OGM to neighbors except the one we received it from
        for neighbor in self.links:
            if neighbor == sender:
                continue
        
        # forward ogm to all neighbors w/ updated src
            rebroadcast_packet = Packet(
                type="ogm",
                src=self.identifier,
                dest="FF:FF:FF:FF:FF:FF",
                data={
                    "originator": originator,
                    "sequence": sequence,
                 "ttl": ttl
             },
                size=128
            )
        # self.send_packet(rebroadcast_packet)
            self.network.get_node(neighbor).receive_packet(rebroadcast_packet)

        
    # update routing table based on current state of ogm_counts
    def update_routing_table(self):
        for (originator, neighbors) in self.ogm_counts.items():
            best_neighbor = max(neighbors.items(), key=lambda item: item[1])[0]
            self.routing_table[originator] = best_neighbor
            # avoid misrouting loops
        self.routing_table[self.identifier] = self.identifier
        
    def send_packet(self, packet):
        # prevent infinite routing loops
        if len(packet.path) > len(self.network.nodes):
            return -1
        # check if broadcasting
        if packet.dest == "FF:FF:FF:FF:FF:FF":
            for node_ident in self.links:
                self.network.get_node(node_ident).receive_packet(packet)
            return 0
        
        # check if there is a way to dest
        if packet.dest not in self.routing_table:
            return -1
        
        # find which neighbor is best for dest
        # first_hop_ident = self.routing_table[packet.dest]
        # Determine next hop  
        next_hop = self.routing_table[packet.dest]
         # Next-hop must still be a neighbor in the *current* topology  
        if next_hop not in self.links:
            return -1   # the link disappeared after mutate_graph()


        # another check: if link no longer exists due to network mutation
        # if first_hop_ident not in self.links:
        #     return -1
        
        # forward packet through that node
        # return weight of link to first_hop and the recursive call
        # return self.links[first_hop_ident] + self.network.get_node(first_hop_ident).receive_packet(packet)

        # Forward packet
        # Packet size influences travel time 
        transmission_delay = (packet.size * 8) / BANDWIDTH
        propagation_delay = self.links[next_hop] / 1000    

        hop_delay = transmission_delay+ propagation_delay

        # forward packet and return total delay
        return hop_delay + self.network.get_node(next_hop).receive_packet(packet)