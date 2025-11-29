class Packet:   
    def __init__(self, type, src, dest, data):
        self.type = type
        self.src = src
        self.dest = dest
        self.data = data
        self.path = [src]
        
    def __str__(self):
        return f"Packet(type={self.type!r}, src={self.src}, dest={self.dest}, data={self.data!r}, path={self.path})"