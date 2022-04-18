import socket


class SimpleSocket:

    def __init__(self, port):
        self.port = port
        self.ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_addr = socket.gethostname()
        self.ssock.bind((ip_addr, port))

    def read(self):
        data = self.ssock.recvfrom(8096)

        return data

    def send(self, msg, dst):
        self.ssock.sendto(msg, dst)
