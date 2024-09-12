from enum import Enum
import json
import socket
import UI
from Connection import Connection
from Game import Game

class ClientState(Enum):
    OFFLINE= 0
    WAIT_CON= 1
    PLAYING = 2

class ClientClass():
    def __init__(self) -> None:
        self.state= ClientState.OFFLINE
        self.ui=UI.UI(self)
        self.connection = Connection()
        self.game = Game("Map/Arenas")
        self.game.connection = self.connection
        self.num_connected_player = 0
        self.max_player = 0

    def get_state(self):
        return self.state
    
    def is_connected(self):
        return self.connection.is_connected

    def run(self) -> None:
        running =True
        while running :

            packets = self.connection.receive_packets()


            # Update varié
            match self.state:
                case ClientState.OFFLINE:
                    pass
                case ClientState.WAIT_CON:
                    self.connection.has_connected(packets)
                    for packet in packets:
                        if packet.decode("utf-8").find('{"n":') != -1:
                            obj = json.loads(packet.decode("utf-8"))
                            self.num_connected_player = obj.get("n")
                            self.max_player = obj.get("m")
                            print(self.num_connected_player, self.max_player)
                        if packet.decode("utf-8").find("map") != -1:
                            print(packet)
                            obj = json.loads(packet.decode("utf-8"))
                            for mapData in self.game.maps:
                                print(obj.get("map"))
                                if mapData.name == obj.get("map"):
                                    self.game.currentMap = mapData
                                    self.game.serverSize = obj.get("size")
                                    self.state = ClientState.PLAYING
                case ClientState.PLAYING:
                    self.ui.menu = UI.Menu.GAME                      
                    self.game.update_game(packets)

            running=self.ui.handle_event()
            self.ui.render()
    
    def start_game(self):
        self.state=ClientState.PLAYING
        pass

    def connect_server(self,addr : str) ->None: 
        try:
            ip,port = addr.split(":")
            self.connection.send_connect((ip,int(port)))
            self.game.connection.server_address = (ip,int(port))
            self.state = ClientState.WAIT_CON
        except:
            pass

    def disconnect_server(self) ->None:
        if self.state!=ClientState.OFFLINE:
            pass
        self.state=ClientState.OFFLINE

class loader:
    def loadCsv(csv):
        list= []
        with open(csv, "r") as file:
            for line in file:
                row = [cell for cell in line.strip().split(',')]
                list.append(row)
        return list