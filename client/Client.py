from enum import Enum
import socket
import UI
from Connection import Connection

class ClientState(Enum):
    OFFLINE= 0
    WAIT_CON= 1
    PLAYING = 2


class ClientClass():
    def __init__(self) -> None:
        self.state= ClientState.OFFLINE
        self.ui=UI.UI(self)
        self.connection = Connection()

    def get_state(self):
        return self.state
    
    def is_connected(self):
        return self.connection.is_connected

    def run(self) -> None:
        running =True
        while running :

            match self.state:
                case ClientState.OFFLINE:
                    pass
                case ClientState.WAIT_CON:
                    packets = self.connection.receive_packets()
                    self.connection.has_connected(packets)                
                case ClientState.PLAYING:
                    pass
        
            running=self.ui.handle_event()
            self.ui.render()

    def connect_server(self,addr : str) ->None: 
        try:
            ip,port =addr.split(":")
            self.connection.send_connect((ip,int(port)))
            self.state = ClientState.WAIT_CON
        except:
            pass

    def disconnect_server(self) ->None:
        if self.state!=ClientState.OFFLINE:
            pass
        self.state=ClientState.OFFLINE

    def receive_packet(self):
        #rcv
        #data ctrl
        #match case ?  | run fctn
        pass

class loader:
    def loadCsv(csv):
        list= []
        with open(csv, "r") as file:
            for line in file:
                row = [cell for cell in line.strip().split(',')]
                list.append(row)
        return list