import pygame, pytmx

class Map:
    def __init__(self,path) -> None:
        self.path = path
        self.colliders = []

    
    def draw_map(self,screen) -> None:       

        for layer in self.currentMap.visible_layers:

            windowXlimit=screen.get_width() /2 - ((self.currentMap.width / 2 )* self.currentMap.tilewidth*2)
            windowYlimit=screen.get_height() /2 - ((self.currentMap.height / 2 )* self.currentMap.tilewidth*2)
            
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():

                    posX = (x*(self.currentMap.tilewidth*2))+windowXlimit
                    posY = (y*(self.currentMap.tileheight*2))+windowYlimit

                                        
                    scaledTile =  pygame.transform.scale(tile,(self.currentMap.tilewidth*2, self.currentMap.tileheight*2))
                    
                    tileRect = scaledTile.get_rect()
                    tileRect.x=posX
                    tileRect.y=posY
                    
                    self.colliders.append(tileRect)

                    screen.blit(scaledTile,(posX,posY))