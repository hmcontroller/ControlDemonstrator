import socket
import signal
import sys


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    s.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.1.1', 7))

print 'TCP Server Running at ', socket.gethostbyname(socket.gethostname())
s.listen(1)

while True:
    conn, addr = s.accept()
    print 'Connected by', addr
    while True:
        data = conn.recv(1024)
        if not data: break
        conn.sendall(data)
    conn.close()
