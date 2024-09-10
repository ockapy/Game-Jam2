"""
# Documentation du protocole de communication implémenté
## Format
Le server utilise des strings utf-8 encodé (bytes python comme b"")

## Connection
- Le client doit envoyer un string b"ping".
- Si le server a ajouter le client au server alors il renverra b"pong" pour accépté la connection

## Début du jeu
- Le server envoie un packet indiquant le début du jeu par un objet JSON contenant le nom de la map jouer
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
from ServerConnection import ServerConnection

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
        print(f"{config=}")

        self.server_connection = ServerConnection(self, config.get("address"))

        self.state = ServerState.WAIT_CON
        
        self.maps = {1: "map1"}
        self.entities: dict[int, Player] = dict()
        self.client_addr = dict()
        self.NUM_PLAYER = config.get("num_player")
        self.next_net_id = 0

        self.delta_time = 0
    
    def new_net_id(self) -> int:
        self.next_net_id += 1
        return self.next_net_id

    def create_player(self, net_id:int) -> None:
        self.entities[net_id] = Player()
    
    def run(self) -> None:
        """Boucle principale du server"""
        run = True
        compute_time = 0
        print("Start server")
        while run:
            start_delta_time = time()
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
            self.delta_time = start_delta_time - time()
    
    def connect_player(self) -> None:
        """Tente la connection de nouveau joueur"""
        incoming_packets = self.server_connection.receive_all_packet()

        for p, addr in incoming_packets:
            if p == PING:
                self.add_client(addr)
        
        if len(self.client_addr) == self.NUM_PLAYER:
            self.state = ServerState.GAME_SETUP
            print("INFO: Starting game !")
     
    def add_client(self, new_addr: tuple[str, int]) -> None:
        if self.client_addr.get(new_addr) == None: # verification si déja connecter

            player_net_id = self.new_net_id()
            self.client_addr[new_addr] = player_net_id
            self.create_player(player_net_id)

            print(f"INFO: New connection from {new_addr} with network id {self.next_net_id}")
            self.server_connection.sendto(PONG, new_addr)

    def setup_game(self) -> None:
        """Envoie le paquet pour le début de jeu"""
        packet = dict()
        packet["map"] = "Default"
        self.server_connection.sendto_all_client(json.dumps(packet).encode("utf-8"))
        self.state = ServerState.PLAYING

    def update_game(self) -> None:
        """Mise à jours de l'état du jeu"""

        inc_packet = self.server_connection.receive_all_packet()

        # Change les actions reçu 
        for data, addr in inc_packet:
            action_dict = json.loads(data.decode("utf-8"))
            net_id = self.client_addr.get(addr)
            if net_id is not None:
                self.entities[net_id].set_action(action_dict)

        for e_id in self.entities.keys():
            self.entities[e_id].update(self.delta_time)
        
        serialized_entities = self.serialize_entities()
        
        self.server_connection.sendto_all_client(serialized_entities.encode("utf-8"))
    
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
        "num_player": 1
    }
    server = Server(config)
    server.run()