import pygame.display
import pygame, os, pytmx
import socket
import json
from os import walk
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from Entity import Entity
from Connection import Connection


class Game:

    x = 1
    y = 1

    def __init__(self,path) -> None:
        pygame.init()

        self.connection = Connection()

        self.server_address = ("127.0.0.1", 9999)

        self.screen = self.init_screen(1280,960)
        self.maps = self.initMaps(path)
        
        # Maybe change it
        self.currentMap = self.maps["Default"]
        self.draw_map(self.screen)
        
        #self.entity = Entity("Assets/Characters/BlowThemUp-player.png", 100, 100, 'right')

        self.running = True
        self.run()
        
        
    def init_screen(self, width: int, height: int) -> pygame.Surface:
        pygame.display.init()
        screen = pygame.display.set_mode((width, height),  pygame.RESIZABLE | pygame.SCALED)
        return screen

    def initMaps(self,path) -> dict:
    
        maps = dict()

        directories = os.listdir(path)

        for directory in directories:

            filenames = next(walk(path+"/"+directory), (None, None, []))[2]

            for file in filenames:
                if file.endswith(".tmx"):
                    tmxData = load_pygame(path+"/"+directory+"/"+file)
                    mapName = file.removesuffix(".tmx")
                    maps[mapName] = tmxData

        return maps
    
    def loadChar(self,path,x,y,direction):
        self.entity = Entity(path,x,y,direction)
        
    
    
    def draw_map(self,screen) -> None:       

        for layer in self.currentMap.visible_layers:

            windowXlimit=screen.get_width() /2 - ((self.currentMap.width / 2 )* self.currentMap.tilewidth*2)
            windowYlimit=screen.get_height() /2 - ((self.currentMap.height / 2 )* self.currentMap.tilewidth*2)
            
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():
                    
                    scaledTile = pygame.transform.scale(tile,(self.currentMap.tilewidth*2, self.currentMap.tileheight*2))
                    screen.blit(scaledTile, ((x * (self.currentMap.tilewidth*2))+windowXlimit, (y * (self.currentMap.tileheight*2))+windowYlimit))

    
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

    def run(self):
        # Main game loop
        self.w = 800
        self.h = 600
        clock = pygame.time.Clock()

        self.loadChar("Assets/Characters/BlowThemUp-player.png",100,100,'right')

        self.connection.send_connect(self.server_address)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.VIDEORESIZE:
                    xDiff = self.w - event.dict["size"][0]
                    yDiff = self.h - event.dict["size"][1]
            
            actions = self.get_played_action()

            packets = self.connection.receive_packets()
            self.handle_packets(packets)

            self.connection.send_message(json.dumps(actions))
            
            #Update the game
            self.update()

            # Update the display
            self.render()

            pygame.display.update()
            clock.tick(60)

        pygame.quit()


    def update(self,direction)->None : 
        self.entity.set_direction(direction)
        self.entity.update((self.x, self.y))
        self.x += 1 * self.entity.get_velocity()
        

    def update(self,direction)->None : 
        self.entity.set_direction(direction)
        self.entity.update((self.x, self.y))
        self.x += 1 * self.entity.get_velocity()
        

    def render(self):
        self.screen.fill((0,0,0))
        self.draw_map(self.screen)
        self.entity.render(self.screen)



game = Game("Map/Arenas")