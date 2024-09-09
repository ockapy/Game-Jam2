import pygame, pytmx

class Map :
    def __init__(self,path) -> None:
        self.path = path
        self.name = "Unamed"
        self.colliders = []
        self.data = pytmx.load_pygame(path)

    
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