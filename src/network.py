from packet import Packet

class Network:
    def __init__(self):
        self.nodes = []
        
    def broadcast_ogm(self):
        for node in self.nodes:
            ogm_packet = Packet(
                type = "ogm",
                src = node.identifier,
                dest = "FF:FF:FF:FF:FF:FF",
                data = {
                    "originator": node.identifier,
                    "sequence": node.sequence_number,
                    "ttl": 500
                }
            )
            node.sequence_number += 1
            node.send_packet(ogm_packet)
    
    def get_node(self, identifier):
        return [node for node in self.nodes if node.identifier == identifier][0]