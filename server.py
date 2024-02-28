class Server:

    def __init__(self, server_address):
        self.address = server_address
        self.objects = []
        self.virtual_addresses = []

    def get_load(self):
        return len(self.objects)

    def get_address(self):
        return self.address

    def get_virtual_addresses(self):
        return self.virtual_addresses

    def get_objects(self):
        return self.objects

    def set_virtual_addresses(self, vir_ads):
        self.virtual_addresses = list(vir_ads)
