class Node:   
    def __init__(self, identifier):
        self.identifier = identifier
        self.links = {}
        
    def __str__(self):
        links_str = "\n".join([f"  {node} -> {weight}" for node, weight in self.links.items()])
        return f"Node {self.identifier}:\n{links_str if links_str else '  (no links)'}"
    
    def receive_packet(self, packet):
        print(f"Node {self.identifier} has received a packet from {packet.src}!")
        if (self.identifier == packet.dest or packet.dest == "FF:FF:FF:FF:FF:FF"):
            self.accept_packet(packet)
        
    def accept_packet(self, packet):
        print(f"Node {self.identifier} accepting from {packet.src}!")