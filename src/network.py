from packet import Packet

class Network:
    def __init__(self):
        self.nodes = []
        
    def broadcast_ogm(self):
        for node in self.nodes:
            node.broadcast_ogm()
    
    def get_node(self, identifier):
        return [node for node in self.nodes if node.identifier == identifier][0]