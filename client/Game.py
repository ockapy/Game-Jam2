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

        self.connection = Connection()

        self.server_address = ("127.0.0.1", 9999)

        self.screen = self.init_screen(1280,960)
        self.maps = self.initMaps(path)
        
        
        
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
    
    def  loadChar(self,path,x,y,direction):
        self.entity = Entity(path,x,y,direction)
        
    
    
    

    
    def handle_packets(self, packets: list[bytes]) -> None:
        decoded_packets = [p.decode("utf-8") for p in packets] 
        self.connection.has_connected(packets)
        
        repl_packet = self.connection.get_last_replication_packets(decoded_packets)
        if repl_packet is not None:
            self.update_entities(repl_packet)

    def update_entities(self, replication_packet: dict):
        print(f"{replication_packet=}")
    
    def get_played_action(self):
        keycodes = [k for k in range(len(pygame.key.get_pressed())) if pygame.key.get_pressed()[k]]
        return keycodes
    
    def update_game(self):

            actions = self.get_played_action()
            
            packets = self.connection.receive_packets()
            self.handle_packets(packets)

            self.connection.send_message(json.dumps(actions))
            
            #Update the game
            self.update()

    def run(self):
        # Main game loop
        clock = pygame.time.Clock()

        self.loadChar("Assets/Characters/BlowThemUp-player.png",250,500,'right')

#        self.connection.send_connect(self.server_address)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                            
        
            # actions = self.get_played_action()
            

            
    

#            packets = self.connection.receive_packets()
#           self.handle_packets(packets)

#            self.connection.send_message(json.dumps(keys))


            
            #Update the game
            self.update()

            # Update the display
            self.render()

            pygame.display.update()
            clock.tick(60)

        pygame.quit()


    def update(self)->None : 
        keys = pygame.key.get_pressed()
        movement = keys[pygame.K_d] - keys[pygame.K_q]
        if (movement != 0):
            self.entity.add_x(movement)

    def render(self):
        self.screen.fill((0,0,0))
        self.currentMap.draw_map(self.screen)
        self.entity.render(self.screen)



if __name__ == "__main__":
    game = Game("Map/Arenas")