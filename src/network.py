class Network:
    def __init__(self, nodes):
        self.nodes = nodes

    def send_packet(self, packet):
        if (packet.dest == "FF:FF:FF:FF:FF:FF"):
            for link in self.get_node(packet.src).links:
                self.get_node(link).receive_packet(packet)
        else:
            self.get_node(packet.dest).receive_packet(packet)
    
    def get_node(self, identifier):
        return [node for node in self.nodes if node.identifier == identifier][0]