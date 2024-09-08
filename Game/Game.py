import pygame.display
import pygame, os, pytmx
import socket
import json
from os import walk
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from Entity import Entity

BUFFER_SIZE = 1024
PING = b"ping"
PONG = b"pong"

class Game:

    def __init__(self,path) -> None:
        pygame.init()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False) 

        self.is_connected = False
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

    def receive_packets(self) -> list[bytes]:
        incoming_packets = []

        while True:
            try:
                data, addr = self.socket.recvfrom(BUFFER_SIZE)
                if addr == self.server_address:
                    incoming_packets.append(data)
            except:
                break
        return incoming_packets
    
    def handle_packets(self, packets: list[bytes]) -> None:
        decoded_packets = [p.decode("utf-8") for p in packets] 
        if not self.is_connected and PING in packets:
            self.is_connected = True
            print("INFO: Client connected to ", self.server_address)
        
        i = 0
        while i < len(decoded_packets) and decoded_packets[i] == PONG.decode("utf-8"):
            i += 1
        
        if i < len(decoded_packets):
            self.update_entities(json.loads(decoded_packets[i]))
    
    def send_message(self, message: str) -> None:
        self.socket.sendto(message.encode("utf-8"), self.server_address)

    def update_entities(self, str_packet: dict):
        print(f"{str_packet=}")

    def connect(self, server_addr):
        self.server_address = server_addr
        self.socket.sendto(PING, server_addr)
    
    def get_played_action(self):
        keycodes = [k for k in range(len(pygame.key.get_pressed())) if pygame.key.get_pressed()[k]]
        return keycodes

    def run(self):
        # Main game loop
        self.w = 800
        self.h = 600
        clock = pygame.time.Clock()

        self.connect(self.server_address)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.VIDEORESIZE:
                    xDiff = self.w - event.dict["size"][0]
                    yDiff = self.h - event.dict["size"][1]
            
            actions = self.get_played_action()

            packets = self.receive_packets()
            self.handle_packets(packets)

            self.send_message(json.dumps(actions))
            
            #Update the game
            self.update()

            # Update the display
            self.render()

            pygame.display.update()
            clock.tick(60)

        pygame.quit()


    def update(self)->None : 
        self.entity.update()

    def render(self):
        self.screen.fill((0,0,0))
        self.draw_map(self.screen, 0,0)
        self.entity.render(self.screen)



game = Game("Map/Arenas")