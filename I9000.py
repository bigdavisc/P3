import socket

class I9000:
    CLEAR_BUFFER = b'\x18'
    NEW_LINE = b'\x0d\x0a'
    CUT = b'\x1b\x76'

    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port
        self.buffer: bytes = b''

    def add_line(self, line: str):
        self.buffer += str.encode(line)
        self.buffer += self.NEW_LINE

    def print_buffer(self, cut: bool = True):
        # Create the connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip_address, self.port))

        # Clear the buffer before sending any data
        s.sendall(self.CLEAR_BUFFER)

        # Send the buffer and some padding on the bottom
        s.sendall(self.buffer)
        s.sendall(self.NEW_LINE * 2)

        # Cut if needed
        if cut:
            s.sendall(self.CUT)

        # Close the connection
        s.close()
