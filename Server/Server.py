from enum import Enum
from time import sleep, time
import socket
import json

TARGET_TPS = 30
BUFFER_SIZE = 1024

PING = b"ping"
PONG = b"pong"

class ServerState(Enum):
    WAIT_PLAYER = 0
    PLAYING = 1
    END_GAME = 2

class Server:
    def __init__(self, config: dict) -> None:
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setblocking(False)
        print(f"{config=}")
        self.udp_socket.bind(config.get("address"))

        self.state = ServerState.WAIT_PLAYER
        self.client_addr = dict() # dictionnaire faisant la correspondance entre le client et le id réseaux 
        self.next_net_id = 0
    
    def new_net_id(self) -> int:
        self.next_net_id += 1
        return self.next_net_id
    
    def run(self) -> None:
        """Boucle principale du server"""
        run = True
        compute_time = 0
        print("Start server")
        while run:
            start_compute_time = time()
            match self.state:
                case ServerState.WAIT_PLAYER:
                    self.connect_player()
                case ServerState.PLAYING:
                    self.update_game()
                case ServerState.END_GAME:
                    self.end_game()
            
            compute_time = start_compute_time - time()
            sleep(max((1/TARGET_TPS) - compute_time, 0))
    
    def connect_player(self) -> None:
        """Tente la connection de nouveau joueur"""
        incoming_packets = self.receive_all_packet()

        for p, addr in incoming_packets:
            if p == PING:
                self.add_client(addr)
    
    def receive_all_packet(self) -> list[tuple[bytes, tuple[str, int]]]:
        packets = []
        
        while True:
            try:
                inc_packet = self.udp_socket.recvfrom(BUFFER_SIZE)
                packets.append(inc_packet)
            except:
                break
        return packets
    
    def add_client(self, new_addr: tuple[str, int]) -> None:
        if self.client_addr.get(new_addr) == None: # verification si déja connecter
            self.client_addr[new_addr] = self.new_net_id()
            print(f"INFO: New connection from {new_addr} with network id {self.next_net_id}")
            self.udp_socket.sendto(PONG, new_addr)


    def update_game(self) -> None:
        """Mise à jours de l'état du jeu"""
        pass

    def end_game(self) -> None:
        """Fini une partie avant d'en commencé une nouvelle"""
        pass

if __name__ == "__main__":
    config = {
        "address": ("127.0.0.1", 9999)
    }
    server = Server(config)
    server.run()