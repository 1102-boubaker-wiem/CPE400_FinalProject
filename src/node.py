from packet import Packet

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
        packet.path.append(self.identifier)
        
        if packet.type == "ogm":
            self.process_ogm(packet)
            return self.links[packet.src] # return weight of link between this node and sender
        
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
        ttl -= weight
        
        # check if ttl has expired
        if ttl <= 0:
            return
        
        # check if we are receiving our own OGMs
        if originator == self.identifier or sender == self.identifier:
            return
        
        # initialize tracking structures
        if originator not in self.ogm_counts:
            self.ogm_counts[originator] = {}
        if originator not in self.ogm_sequence_nums:
            self.ogm_sequence_nums[originator] = {}
        
        if sender not in self.ogm_counts[originator]:
            self.ogm_counts[originator][sender] = 0
        if sender not in self.ogm_sequence_nums[originator]:
            self.ogm_sequence_nums[originator][sender] = -1
        
        # check if we've seen this sequence from this neighbor
        if sequence <= self.ogm_sequence_nums[originator][sender]:
            return
        self.ogm_sequence_nums[originator][sender] = sequence
            
        # increment ogm_counts
        self.ogm_counts[originator][sender] += 1
        
        self.update_routing_table()
        
        # forward ogm to all neighbors w/ updated src
        rebroadcast_packet = Packet(
            type="ogm",
            src=self.identifier,
            dest="FF:FF:FF:FF:FF:FF",
            data={
                "originator": originator,
                "sequence": sequence,
                "ttl": ttl
            }
        )
        self.send_packet(rebroadcast_packet)
        
    # update routing table based on current state of ogm_counts
    def update_routing_table(self):
        for (originator, neighbors) in self.ogm_counts.items():
            best_neighbor = max(neighbors.items(), key=lambda item: item[1])[0]
            self.routing_table[originator] = best_neighbor
        
    def send_packet(self, packet):
        # check if broadcasting
        if packet.dest == "FF:FF:FF:FF:FF:FF":
            for node_ident in self.links:
                self.network.get_node(node_ident).receive_packet(packet)
            return 0
        
        # check if there is a way to dest
        if packet.dest not in self.routing_table:
            return -1
        
        # find which neighbor is best for dest
        first_hop_ident = self.routing_table[packet.dest]
        
        # forward packet through that node
        # return weight of link to first_hop and the recursive call
        return self.links[first_hop_ident] + self.network.get_node(first_hop_ident).receive_packet(packet)