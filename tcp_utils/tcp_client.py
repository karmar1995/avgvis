import socket, select, sys, os

if len(sys.argv) != 5:
    print("Usage:python tcp_client.py {server ip} {server port} {number of packets to dump} {directory}")
    sys.exit(1)

server_address = (sys.argv[1], int(sys.argv[2]))
count = int(sys.argv[3])
directory = sys.argv[4]

try:
    os.makedirs(directory)
except FileExistsError:
    pass

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('connecting to {} port {}'.format(server_address[0],server_address[1]))
sock.connect(server_address)

try:

    packetsReceived = 0
    while packetsReceived < count:
        ready = select.select([sock], [], [], 0.25)
        if ready[0]:
            data = sock.recv(1024)
            if len(data) > 0:
                packetsReceived += 1
                file = os.path.join(directory, 'packet_{}'.format(packetsReceived))
                print ("Writing: {} \n to file: {}".format(data, file))
                with open(file, 'wb') as f:
                    f.write(data)

finally:
    print ('closing socket')
    sock.close()