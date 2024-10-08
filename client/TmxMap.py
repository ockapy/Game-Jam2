import pygame, pytmx

class Map :
    def __init__(self,path) -> None:
        self.path = path
        self.name = "Unamed"
        self.colliders = []
        self.data = pytmx.load_pygame(path)
        self.spawn_position: list[tuple[int, int]] = []
        self.ballon = pygame.transform.scale2x(pygame.transform.scale2x(pygame.image.load("Assets/Backgrounds/BlowThemUp-ballon.png").convert_alpha()))

    
    def draw_map(self,screen) -> None:       

        for layer in self.data.visible_layers:

            windowXlimit=screen.get_width() /2 - ((self.data.width / 2 )* self.data.tilewidth*2)
            windowYlimit=screen.get_height() /2 - ((self.data.height / 2 )* self.data.tilewidth*2)
            
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():

                    posX = (x*(self.data.tilewidth*2))+windowXlimit
                    posY = (y*(self.data.tileheight*2))+windowYlimit

                    

                                        
                    scaledTile =  pygame.transform.scale(tile,(self.data.tilewidth*2, self.data.tileheight*2))
                    
                    tileRect = scaledTile.get_rect()
                    tileRect.x=posX
                    tileRect.y=posY
                    
                    self.colliders.append(tileRect)

                    screen.blit(scaledTile,(posX,posY))
    
    def draw_map(self,screen,serverSize):

        for layer in self.data.visible_layers:

            clientX=screen.get_width() 
            clientY=screen.get_height()

            

            scaleX = clientX / serverSize[0]
            scaleY = clientY / serverSize[1]



            windowXLimit = clientX / 2 - ((self.data.width / 2) * self.data.tilewidth * scaleX)
            windowYLimit = clientY / 2 - ((self.data.height / 2) * self.data.tileheight * scaleY)

            
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():

                    posX = (x*self.data.tilewidth*scaleX)+windowXLimit
                    posY = (y*self.data.tileheight*scaleY)+windowYLimit

                                        
                    scaledTile =  pygame.transform.scale(tile,(self.data.tilewidth*scaleX, self.data.tileheight*scaleY))
                    
                    tileRect = scaledTile.get_rect()
                    tileRect.x=posX
                    tileRect.y=posY
                    
                    self.colliders.append(tileRect)

                    screen.blit(scaledTile,(posX,posY))
        for i in range(5):
            screen.blit(self.ballon, (i * self.ballon.get_width(), screen.get_height()-60))