import socket
from time import sleep


class I9000:
    # Printer Control Commands
    CLEAR_BUFFER = b'\x18'
    CUT = b'\x1b\x76'

    # Horizontal Control Commands
    RESET_PRINT_POS = b'\x1b\x6e\x00\x00'

    # Vertical Control Commands
    FINE_LINE_FEED = b'\x1b\x4a\x1b' + RESET_PRINT_POS
    NEW_LINE = b'\x0d\x0a'

    LINE_WIDTH = 42

    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port
        self.buffer: bytes = b''

    def add_line(self, line: str):
        while len(line) > self.LINE_WIDTH:
            self.buffer += str.encode(line[:self.LINE_WIDTH-1] + "-")
            self.buffer += self.FINE_LINE_FEED
            line = line[self.LINE_WIDTH - 1:]

        if len(line) > 0:
            self.buffer += str.encode(line)

        self.buffer += self.NEW_LINE

        return self

    def add_header(self, t_type: str = "TRANSMISSION", t_from: str = None, t_to: str = None, t_datetime: str = None):
        available_width = self.LINE_WIDTH - 2
        start_padding = (available_width - len(t_type)) // 2
        end_padding = start_padding + (0 if len(t_type) % 2 == 0 else 1)

        top = b'\xC9' + str.encode("=" * available_width) + b'\xBB'
        empty = b'\xBA' + str.encode(" " * available_width) + b'\xBA'
        bottom = b'\xC8' + str.encode("=" * (self.LINE_WIDTH - 2)) + b'\xBC'

        self.buffer += top + self.FINE_LINE_FEED
        self.buffer += b'\xBA' + str.encode(" " * start_padding) + str.encode(t_type) + str.encode(" " * end_padding) + b'\xBA'
        self.buffer += self.FINE_LINE_FEED
        self.buffer += empty + self.FINE_LINE_FEED

        if t_to:
            self.buffer += b'\xBA' + str.encode("      TO: " + t_to) + str.encode(" " * (available_width - len(t_to) - 10)) + b'\xBA'
            self.buffer += self.FINE_LINE_FEED

        if t_from:
            self.buffer += b'\xBA' + str.encode("    FROM: " + t_from) + str.encode(" " * (available_width - len(t_from) - 10)) + b'\xBA'
            self.buffer += self.FINE_LINE_FEED

        if t_datetime:
            self.buffer += b'\xBA' + str.encode("    DATE: " + t_datetime) + str.encode(" " * (available_width - len(t_datetime) - 10)) + b'\xBA'
            self.buffer += self.FINE_LINE_FEED

        self.buffer += bottom + self.NEW_LINE

        return self

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

        sleep(1)

        # Close the connection
        s.close()
