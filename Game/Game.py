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

        self.screen = self.init_screen(800,600)
        self.maps = self.initMaps(path)
        
        self.currentMap = self.maps["Default"]
        self.draw_map(self.screen,0,0)

        self.entity = Entity("Assets/Characters/BlowThemUp-player.png", 100, 100, 'right')

        self.running = True
        self.run()
        
        
    @staticmethod
    def init_screen(width: int, height: int) -> pygame.Surface:
        pygame.display.init()
        screen = pygame.display.set_mode((width, height),  pygame.RESIZABLE | pygame.SCALED)
        return screen

    @staticmethod
    def initMaps(path) -> dict:
    
        maps = dict()

        dirs = os.listdir(path)

        for dir in dirs:

            filenames = next(walk(path+"/"+dir), (None, None, []))[2]

            for file in filenames:
                if file.endswith(".tmx"):
                    tmxData = load_pygame(path+"/"+dir+"/"+file)
                    mapName = file.removesuffix(".tmx")
                    maps[mapName] = tmxData

        return maps
    
    def draw_map(self,screen,xDiff,yDiff) -> None:       
        
        scaleX = 1 - (xDiff / 100)
        scaleY = 1 - (yDiff / 100)

        quart = ((screen.get_width()//4),(screen.get_height()//4))

        for layer in self.currentMap.visible_layers:
            scale = (screen.get_width() - screen.get_height())/100
            if scale < 1:
                scale = 1
            
            windowXlimit=screen.get_width() /2 - ((self.currentMap.width / 2 )* self.currentMap.tilewidth)
            windowYlimit=screen.get_height() /2 - ((self.currentMap.height / 2 )* self.currentMap.tilewidth)
            
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():

                    scaled_tile = pygame.transform.scale(tile,((self.currentMap.tilewidth*scale),(self.currentMap.tileheight*scale)))

                    # screen.blit(scaled_tile, (quart[0] * (self.currentMap.tilewidth*scaleX), quart[1] * (self.currentMap.tileheight*scaleY)))
                    screen.blit(tile, ((x * (self.currentMap.tilewidth))+windowXlimit, (y * (self.currentMap.tileheight))+windowYlimit))

    
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
            
            if K_LEFT:
                self.update('right')

            #Update the game
            #self.update()



            # Update the display
            self.render()

            pygame.display.update()
            clock.tick(60)

        pygame.quit()


    def update(self,direction)->None : 
        self.entity.set_direction(direction)
        self.entity.update((self.x, self.y))
        self.x += 1 * self.entity.get_velocity()
        

    def render(self):
        self.screen.fill((0,0,0))
        self.draw_map(self.screen, 0,0)
        self.entity.render(self.screen)



game = Game("Map/Arenas")