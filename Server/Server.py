"""
# Documentation du protocole de communication implémenté
## Format
Le server utilise des strings utf-8 encodé (bytes python comme b"")

## Connection
- Le client doit envoyer un string b"ping".
- Si le server a ajouter le client au server alors il renverra b"pong" pour accépté la connection

## Transmition en jeu
- Le Client doit envoyer les keycodes pygame pour les touches dans un array JSON. Exemple: touche 'd' appuyer -> message envoyer: b"[100]"
- Le server envoye les informations du monde dans un objet JSON.
Exemple: 
{
    1: {"pos": [45, 387]},
    2: {"pos": [847, 29]}
}
"""

import socket
import json
from enum import Enum
from time import sleep, time
from Player import Player

TARGET_TPS = 30
BUFFER_SIZE = 1024

PING = b"ping"
PONG = b"pong"

class ServerState(Enum):
    WAIT_CON = 0
    GAME_SETUP = 1
    PLAYING = 2
    END_GAME = 3

class Server:
    def __init__(self, config: dict) -> None:
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setblocking(False)
        print(f"{config=}")
        self.udp_socket.bind(config.get("address"))

        self.state = ServerState.WAIT_CON
        self.client_addr = dict() # dictionnaire faisant la correspondance entre le client et le id réseaux
        
        self.maps = {1: "map1"}
        self.entities: dict[int, Player] = dict()

        self.NUM_PLAYER = config.get("num_player")
        self.next_net_id = 0
    
    def new_net_id(self) -> int:
        self.next_net_id += 1
        return self.next_net_id

    def create_player(self, net_id:int) -> None:
        self.entities[net_id] = Player()
    
    def sendto_all_client(self, data: bytes) -> None:
        for c_addr in self.client_addr.keys():
            self.udp_socket.sendto(data, c_addr)
    
    def run(self) -> None:
        """Boucle principale du server"""
        run = True
        compute_time = 0
        print("Start server")
        while run:
            start_compute_time = time()
            match self.state:
                case ServerState.WAIT_CON:
                    self.connect_player()
                case ServerState.GAME_SETUP:
                    self.setup_game()
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
        
        if len(self.client_addr) == self.NUM_PLAYER:
            self.state = ServerState.PLAYING
            print("INFO: Starting game !")
    
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

            player_net_id = self.new_net_id()
            self.client_addr[new_addr] = player_net_id
            self.create_player(player_net_id)

            print(f"INFO: New connection from {new_addr} with network id {self.next_net_id}")
            self.udp_socket.sendto(PONG, new_addr)

    def setup_game(self) -> None:
        pass

    def update_game(self) -> None:
        """Mise à jours de l'état du jeu"""

        inc_packet = self.receive_all_packet()

        for data, addr in inc_packet:
            action_dict = json.loads(data.decode("utf-8"))
            net_id = self.client_addr.get(addr)
            self.entities[net_id].set_action(action_dict)

        for e_id in self.entities.keys():
            self.entities[e_id].update()
        
        serialized_entities = self.serialize_entities()
        
        self.sendto_all_client(serialized_entities.encode("utf-8"))
    
    def serialize_entities(self) -> str:
        entities_dict = dict()
        
        for e in self.entities.keys():
            entities_dict[e] = self.entities[e].serialize()
        
        return json.dumps(entities_dict)

    def end_game(self) -> None:
        """Fini une partie avant d'en commencé une nouvelle"""
        pass

if __name__ == "__main__":
    config = {
        "address": ("127.0.0.1", 9999),
        "num_player": 2
    }
    server = Server(config)
    server.run()