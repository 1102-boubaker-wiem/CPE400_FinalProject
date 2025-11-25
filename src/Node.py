class Node:
    # node identifier
    identifier = ""
    # {node: weight} pairs where the weight is the calculated "delay" of sending a packet to that node from the current
    links = {}
    
    def __init__(self, identifier):
        self.identifier = identifier
    
    # method that is called when a packet is received by the node
    def accept_packet(packet):
        return
    
    # method that is called when a packet is to be sent from the node
    def send_packet(packet):
        return