import binascii

import dnslib

from dnsiplocator import IpLocator
from simplesocket import SimpleSocket


class dnsservermanager:

    def __init__(self, network, port):
        self.network = network
        self.port = port
        self.socket = SimpleSocket(port)
        self.dnsiplocator = IpLocator()

    def listen(self):
        while True:
            data, clientinfo = self.socket.read()
            request = dnslib.DNSRecord.parse(data)
            # @TODO  verify cdn name is correct in record

            cdn_ip = self.dnsiplocator.get_closest_ip(clientinfo[0])

            response = dnslib.DNSRecord(dnslib.DNSHeader(qr=1, aa=1, ra=1, id=request.header.id),
                                        q=dnslib.DNSQuestion("cs5700cdn.example.com"),
                                        a=dnslib.RR("cs5700cdn.example.com", rdata=dnslib.A(cdn_ip)))

            response = response.pack()
            self.socket.send(response, clientinfo)
