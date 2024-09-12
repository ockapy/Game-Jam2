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
from Vfx import Vfx

class Game:

    def __init__(self,path) -> None:
        pygame.init()

        self.connection = None

        self.screen = self.init_screen(1280,960)
        self.maps = self.initMaps(path)
        self.entities = dict()
        self.vfx = dict()
        self.isGirafe = False
      
        
        
    def init_screen(self, width: int, height: int) -> pygame.Surface:
    #    pygame.display.init()
    #    screen = pygame.display.set_mode((width, height),  pygame.RESIZABLE)
        screen =pygame.display.get_surface()
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

        for p in decoded_packets:
            if p.find("win") != -1:
                print("Number ", json.loads(p).get("win"), " win the game")
        
        repl_packet = self.connection.get_last_replication_packets(decoded_packets)
        #print(repl_packet)
        if repl_packet is not None:
            packet_data = json.loads(repl_packet).get("rep")
            self.update_entities(json.dumps(packet_data))

    def update_entities(self, replication_packet):
        for i in json.loads(replication_packet).keys():
            packet = json.loads(replication_packet)
            x = packet.get(str(i)).get("pos")[0]
            y = packet.get(str(i)).get("pos")[1]
            # l'id réseaux et str(i)
            is_attacking = packet.get(str(i)).get("att")

            if self.entities.get(i) is None:
                if self.connection.net_id == i and self.isGirafe : 
                    self.entities[i] = Entity("Assets/Characters/BlowThemUp-girafe.png",x, y,"right", "Assets/Characters/BlowThemUp-girafe-attaque.png")
                else : 
                    self.entities[i] = Entity("Assets/Characters/BlowThemUp-player.png",x, y,"right", "Assets/Characters/BlowThemUp-player-attaque.png")
            else:
                self.entities[i].set_position(x,y)

            w = self.entities[i].get_rect().w
            if self.vfx.get(str(i)) is None : 
                self.vfx[i] = Vfx("Assets/Characters/BlowThemUp-wind.png", x+w,y, 'right')
            self.vfx[i].set_visibility(is_attacking)
            self.vfx[i].set_direction(self.entities[i].get_direction())
            
            if self.vfx[i].get_direction()== 'right' : 
                self.vfx[i].set_position(x+w,y)
            elif self.vfx[i].get_direction()== 'left': 
                self.vfx[i].set_position(x-self.vfx[i].get_w(),y)

            
            
    
    def get_played_action(self):
        keycodes = [k for k in range(len(pygame.key.get_pressed())) if pygame.key.get_pressed()[k]]
        return keycodes
    
    def update_game(self,packets):

            actions = self.get_played_action()
            
            self.handle_packets(packets)

            if self.entities :
                if pygame.K_j in actions:
                    self.entities.get(str(self.connection.net_id)).set_etat('fight')
                    self.vfx.get(str(self.connection.net_id)).set_visibility(True)
                if self.entities.get(str(self.connection.net_id)).is_fighting() : 
                    self.entities.get(str(self.connection.net_id)).animation_fight()
                

            self.connection.send_message(json.dumps(actions))
            
    def render(self,screen: pygame.Surface):
        self.currentMap.draw_map(screen,self.serverSize)
        for entity in self.entities.values():
            entity.render(screen,self.serverSize)
        for vfx in self.vfx.values():
            if vfx.is_show():
                vfx.render(screen, self.serverSize)

    def get_isGirafe(self) -> bool: 
        return self.isGirafe


if __name__ == "__main__":
    game = Game("Map/Arenas")