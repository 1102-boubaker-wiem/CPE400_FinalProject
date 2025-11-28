class Packet:   
    def __init__(self, type, src, dest, data):
        self.type = type
        self.src = src
        self.dest = dest
        self.data = data
        
    def __str__(self):
        data_str = ""
        for key, value in self.data.items():
            data_str += f"    {key}:{value}\n"
        return f"Packet (type: {self.type}, src: {self.src}, dest: {self.dest})\n{data_str}"