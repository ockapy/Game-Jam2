import pygame, os, pytmx
from os import walk
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from Entity import Entity

class Game:

    def __init__(self,path) -> None:
        pygame.init()

        self.screen = self.init_screen(800,600)
        self.maps = self.initMaps(path)
        
        self.currentMap = self.maps["Default"]
        self.draw_map(self.screen)

        self.entity = Entity("Assets/Characters/BlowThemUp-player.png", 100, 100, 'right')

        self.running = True
        self.run()
        
        
    @staticmethod
    def init_screen(width: int, height: int) -> pygame.Surface:
        screen = pygame.display.set_mode((width, height),  pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
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
    
    def draw_map(self,screen,sX=32,sY=32) -> None:       
        

        quart = (screen.get_width()//4, screen.get_height()//4) 
        for layer in self.currentMap.visible_layers:
            scale = (screen.get_width() - screen.get_height())/100
            if scale < 1:
                scale = 1
            
            windowXlimit=screen.get_width()//2
            windowYlimit=screen.get_height() //2

            # posX = x * (self.currentMap.tilewidth*scale)
            # posY= y * (self.currentMap.tileheight*scale)
            
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():

                    scaled_tile = pygame.transform.scale(tile,((self.currentMap.tilewidth*scale),(self.currentMap.tileheight*scale)))

                    screen.blit(scaled_tile, (x * (self.currentMap.tilewidth*scale), y * (self.currentMap.tileheight*scale)))


                    # tile = self.currentMap.get_tile_image_by_gid(gid)
                    # scale = (screen.get_width() - screen.get_height())/100
                    # if scale < 1:
                    #     scale = 1
                    # if tile:
                    #     tile_size = 16*scale
                    #     scaled_tile = pygame.transform.scale(tile,(tile_size,tile_size))
                    #     # Draw the scaled tile on the screen
                    #     screen.blit((scaled_tile), quart)
                    #     print(quart)


    def run(self):
        # Main game loop
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.VIDEORESIZE:
                    self.screen.fill((0,0,0))
                    self.draw_map(self.screen, event.dict['size'][0],event.dict['size'][1])
            # Update the display
            pygame.display.update()
            clock.tick(60)
            #Update the game
            self.update()
        pygame.quit()


    def update(self)->None : 
        self.screen.fill((0,0,0))
        self.entity.update(self.screen)



game = Game("Map/Arenas")