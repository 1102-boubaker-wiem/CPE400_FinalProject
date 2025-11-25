class Node:   
    def __init__(self, identifier):
        self.identifier = identifier
        self.links = {}
        
    def __str__(self):
        links_str = "\n".join([f"  {node} -> {weight}" for node, weight in self.links.items()])
        return f"Node {self.identifier}:\n{links_str if links_str else '  (no links)'}"
    
    # method that is called when a packet is received by the node
    def accept_packet(packet):
        return
    
    # method that is called when a packet is to be sent from the node
    def send_packet(packet):
        return