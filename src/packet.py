class Packet:   
    def __init__(self, type, src, dest, data,size):
        self.type = type
        self.src = src
        self.dest = dest
        self.data = data
        self.path = [src]
        self.size = size                # packet size in bytes (default = 1024 bytes)
        
    def __str__(self):
        return f"Packet(type={self.type!r}, src={self.src}, dest={self.dest}, data={self.data!r}, size={self.size} bytes, path={self.path})"