

class IpLocator:

    def __init__(self):
        self.http_ip = "1.2.3.4"

    def get_closest_ip(self, client_ip):
        return self.http_ip