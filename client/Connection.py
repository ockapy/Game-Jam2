import socket
import json

class Connection:
    PING = b"ping"
    PONG = b"pong"
    BUFFER_SIZE = 1024

    def __init__(self) -> None:
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)

        self.is_connected = False
        
        self.server_address = None
        self.net_id = None
    
    def receive_packets(self) -> list[bytes]:
        incoming_packets = []

        while True:
            try:
                data, addr = self.socket.recvfrom(Connection.BUFFER_SIZE)
                if addr == self.server_address:
                    incoming_packets.append(data)
            except:
                break
        return incoming_packets

    def send_message(self, message: str) -> None:
        self.socket.sendto(message.encode("utf-8"), self.server_address)
    

    def send_connect(self, server_addr: tuple[str, int]):
        self.server_address = server_addr
        self.socket.sendto(Connection.PING, self.server_address)
    
    def has_connected(self, packets: list[bytes]) -> bool:
        if not self.is_connected and any(p.decode("utf-8").find(Connection.PONG.decode("utf-8")) != -1 for p in packets):
            self.is_connected = True
            for p in packets:
                if p.decode("utf-8").find(Connection.PONG.decode("utf-8")) != -1:
                    print(p)
                    obj = json.loads(p.decode("utf-8"))
                    self.net_id = obj.get("nid")

            print("INFO: Client connected to ", self.server_address)
    
    def get_last_replication_packets(self, packets: list[str]) -> str | None:
        """Donne le un packet de réplication valide (necessaire si d'autre type de packet arrive)"""
        i = 0
        while i < len(packets) and packets[i].find(Connection.PONG.decode("utf-8")):
            i += 1
        
        if i < len(packets):
            return packets[i]
        else:
            return None