import socket, sys
from mes_adapter.frame_parser import FrameParser

filename = ""

if len(sys.argv) > 1 and sys.argv[1] == '--sniff':
        filename = sys.argv[2]

host, port = 'localhost', 1234

parser = FrameParser()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    data = s.recv(1024)
    if filename != "":
        with open(filename, 'wb') as f:
            f.write(data)
    else:
        parser.onFrameReceived(data)
