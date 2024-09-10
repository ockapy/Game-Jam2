import socket


class ServerConnection:
    BUFFER_SIZE = 1024
    def __init__(self, the_server, server_addr: tuple[str, int]) -> None:
        self.the_server = the_server
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setblocking(False)
        self.udp_socket.bind(server_addr)
    
    def sendto_all_client(self, data: bytes) -> None:
        for c_addr in self.the_server.client_addr.keys():
            self.udp_socket.sendto(data, c_addr)
    
    def receive_all_packet(self) -> list[tuple[bytes, tuple[str, int]]]:
        packets = []
        
        while True:
            try:
                inc_packet = self.udp_socket.recvfrom(ServerConnection.BUFFER_SIZE)
                packets.append(inc_packet)
            except:
                break
        return packets

    def sendto(self, data: bytes, address: tuple[str, int]) -> None:
        self.udp_socket.sendto(data, address)