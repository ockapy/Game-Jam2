import pygame.display
import pygame, os, pytmx
import socket
import json
from os import walk
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from Connection import Connection
from TmxMap import Map
from Entity import Entity

class Game:

    def __init__(self,path) -> None:
        pygame.init()

        self.connection = None

        self.screen = self.init_screen(1280,960)
        self.maps = self.initMaps(path)
        self.entities = dict()
        
        
        
    def init_screen(self, width: int, height: int) -> pygame.Surface:
        pygame.display.init()
        screen = pygame.display.set_mode((width, height),  pygame.RESIZABLE)
        return screen

    def initMaps(self,path) -> list:
    
        maps = list()

        directories = os.listdir(path)

        for directory in directories:

            filenames = next(walk(path+"/"+directory), (None, None, []))[2]

            for file in filenames:
                if file.endswith(".tmx"):
                    
                    tmxMap = Map(path+"/"+directory+"/"+file)
                    tmxMap.name = file.removesuffix(".tmx")
                    maps.append(tmxMap)

        return maps    

    
    def handle_packets(self, packets: list[bytes]) -> None:
        decoded_packets = [p.decode("utf-8") for p in packets] 
        self.connection.has_connected(packets)
        
        repl_packet = self.connection.get_last_replication_packets(decoded_packets)
        if repl_packet is not None:
            self.update_entities(repl_packet)

    def update_entities(self, replication_packet):
        print(f"{replication_packet=}")
        for i in json.loads(replication_packet).keys():
            if self.entities.get(i) is None:
                packet = json.loads(replication_packet)
                print(packet)
                self.entities[i] = Entity("Assets/Characters/BlowThemUp-player.png",packet.get(str(i)).get("pos")[0], packet.get(str(i)).get("pos")[1],"right")
    
    def get_played_action(self):
        keycodes = [k for k in range(len(pygame.key.get_pressed())) if pygame.key.get_pressed()[k]]
        return keycodes
    
    def update_game(self,packets):

            actions = self.get_played_action()
            
            self.handle_packets(packets)


            self.connection.send_message(json.dumps(actions))
            
    def render(self,screen):
        screen.fill((0,0,0))
        self.currentMap.draw_map(screen)
        for entity in self.entities.values():
            entity.render(screen)



if __name__ == "__main__":
    game = Game("Map/Arenas")